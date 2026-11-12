"""Run the frozen PatchQuestions pilot on the competition's offline model server."""
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from urllib.request import Request, build_opener, ProxyHandler

os.environ.update(TRANSFORMERS_OFFLINE='1', HF_HUB_OFFLINE='1', VLLM_NO_USAGE_STATS='1', VLLM_WORKER_MULTIPROC_METHOD='spawn')
# The installer is a subprocess, so its runtime environment does not propagate.
os.environ.update(TRANSFORMERS_NO_TF='1', TRANSFORMERS_NO_FLAX='1',
    VLLM_ENGINE_READY_TIMEOUT_S='1200', VLLM_MEMORY_PROFILER_ESTIMATE_CUDAGRAPHS='1',
    NCCL_DEBUG='WARN', PYTORCH_CUDA_ALLOC_CONF='expandable_segments:True',
    OTEL_SDK_DISABLED='true', OTEL_PYTHON_DISABLED='true')
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import pilot


def main():
    import torch
    from adk_submission import VllmConfig, VllmServer
    from transformers import AutoTokenizer
    model = Path('/kaggle/input/models/google/gemma-4/other/gemma-4-31b-it-qat-w4a16-ct/2')
    if not model.exists():
        raise FileNotFoundError('Attach google/gemma-4 gemma-4-31b-it-qat-w4a16-ct version 2')
    if not torch.cuda.is_available():
        raise RuntimeError('Select an eligible GPU accelerator before running')
    run_id = time.strftime('%Y%m%d-%H%M%S')
    evidence = Path('/kaggle/working') / ('patchquestions-' + run_id)
    evidence.mkdir(exist_ok=False)
    pilot.save_json(evidence/'ENVIRONMENT.json', {
        'python': sys.version, 'torch': torch.__version__,
        'packages': {p: importlib.metadata.version(p) for p in ('vllm','transformers','swegemma')},
        'gpu': subprocess.check_output(['nvidia-smi'], text=True),
        'model_mount': str(model), 'model_config_sha256': pilot.sha((model/'config.json').read_bytes()),
        'pilot_sha256': pilot.sha((ROOT/'pilot.py').read_bytes())})
    gpu_count = torch.cuda.device_count()
    class SequentialServer(VllmServer):
        def build_cmd(self, *args, **kwargs):
            command = list(super().build_cmd(*args, **kwargs))
            command.extend(['--max-num-seqs', '1', '--max-num-batched-tokens', '8192'])
            (evidence/'SERVER_COMMAND.json').write_text(json.dumps(command, indent=2)+'\n')
            return command
    server = SequentialServer(VllmConfig(model=str(model), port=8000, host='127.0.0.1',
        tensor_parallel_size=4 if gpu_count>=4 else (2 if gpu_count>=2 else 1),
        reasoning_parser='gemma4', max_model_len=32768,
        dtype='bfloat16' if torch.cuda.is_bf16_supported() else 'auto',
        gpu_memory_utilization=0.80, scheduler_reserve_full_isl=False,
        enable_auto_tool_choice=False, enable_lora=False, startup_timeout=1200))
    try:
        print('Starting offline Gemma server', flush=True)
        startup_started = time.monotonic()
        server.start()
        print('Server ready after', round(time.monotonic()-startup_started, 1), 'seconds', flush=True)
        pilot.save_json(evidence/'GPU_AFTER_START.json', {
            'nvidia_smi': subprocess.check_output(['nvidia-smi'], text=True),
            'startup_seconds': time.monotonic()-startup_started})
        endpoint = server.base_url.rstrip('/').removesuffix('/v1')
        opener = build_opener(ProxyHandler({}))
        with opener.open(endpoint+'/v1/models', timeout=30) as response:
            models = json.load(response)
        served = models['data'][0]['id']
        tokenizer = AutoTokenizer.from_pretrained(str(model), local_files_only=True, trust_remote_code=False)
        info = dict(served_model=served, model_revision=str(model), tokenizer_revision=str(model),
            quantization='QAT w4a16 compressed-tensors', serving_stack='vllm '+importlib.metadata.version('vllm'),
            hardware=[torch.cuda.get_device_name(i) for i in range(gpu_count)], context_tokens=32768,
            max_tokens=128, temperature=0, top_p=1, seed=2026, timeout_seconds=180,
            chat_template_kwargs={'enable_thinking': False})
        # Disjoint synthetic fixtures: healthy transport is separate from model correctness.
        fixture = {'configs': ['a', 'b'], 'query_inputs': ['synthetic'],
                   'query_outputs': [['A'], ['B']], 'heldout_outputs': [['same'], ['same']]}
        grades = []
        for pick in (0, 1):
            session = pilot.Session(fixture, 0, [0, 1], 'named')
            session.step({'ask': 0})
            _, grade = session.step({'pick': pick})
            grades.append(grade)
        assert grades[0]['success'] and not grades[1]['success'] and grades[1]['heldout_exact']
        pilot.save_json(evidence/'CALIBRATION_GRADES.json', grades)
        system = {'role': 'system', 'content': 'Reply with exactly {"pick":0}.'}
        first = [system, {'role':'user','content':'Synthetic transport check. Output the required JSON.'}]
        multi = first + [{'role':'assistant','content':'{"ask":0}'},
                         {'role':'user','content':'{"answer":"A"}'}]
        synthetic = {'inputs': ['synthetic-input-'+str(j) for j in range(16)],
                     'outputs': [['synthetic-outcome-'+str((i+j)%8)+'-padding' for j in range(16)] for i in range(64)],
                     'instruction': 'Synthetic fixture. Reply with the required pick object.'}
        long = [system, {'role':'user','content':pilot.encode(synthetic)}]
        calibration = []
        for name, messages in [('opening',first), ('multi_turn',multi), ('long_matrix',long)]:
            request = pilot.model_request(messages, info)
            local_count = pilot.count_tokens(tokenizer, messages, info)
            if local_count + info['max_tokens'] > info['context_tokens']:
                raise RuntimeError('Synthetic calibration exceeds context: '+name)
            started = time.monotonic()
            with opener.open(Request(endpoint+'/v1/chat/completions', data=pilot.encode(request).encode(),
                                     headers={'Content-Type':'application/json'}), timeout=180) as response:
                raw = json.load(response)
            record = {'fixture':name, 'request':request, 'response':raw,
                      'local_prompt_tokens':local_count, 'elapsed_seconds':time.monotonic()-started}
            try:
                record['parsed_action'] = pilot.parse_action(raw['choices'][0]['message']['content'])
            except pilot.ProtocolError as exc:
                record['model_protocol_error'] = str(exc)
            calibration.append(record)
            (evidence/'CALIBRATION.json').write_text(json.dumps(calibration, indent=2) + chr(10), encoding='utf-8')
            actual = raw.get('usage',{}).get('prompt_tokens')
            if actual is not None and 'token_count_offset' not in info and abs(actual - local_count) <= 4: info['token_count_offset'] = actual - local_count; local_count = pilot.count_tokens(tokenizer, messages, info); record['local_prompt_tokens'] = local_count; record['token_count_offset'] = info['token_count_offset']; (evidence/'CALIBRATION.json').write_text(json.dumps(calibration, indent=2) + chr(10), encoding='utf-8')
            if actual is None or actual != local_count:
                raise RuntimeError(f'Calibration token count differs on {name}: local={local_count}, server={actual}')
            print('Calibration:', name, local_count, 'tokens', round(record['elapsed_seconds'],1), 'seconds', flush=True)
        pilot.save_json(evidence/'GPU_AFTER_CALIBRATION.json', {
            'nvidia_smi': subprocess.check_output(['nvidia-smi'], text=True)})
        data = ROOT/'frozen_cases.jsonl.gz'
        cases = pilot.load_cases(data)
        plan = pilot.make_plan(cases, pilot.sha(data.read_bytes()), info, controls=True)
        pilot.save_json(evidence/'plan.json', plan)
        plan_bytes = (evidence/'plan.json').read_bytes()
        (evidence/'PLAN.sha256').write_text(pilot.sha(plan_bytes)+'\n')
        baselines = []
        for entry in plan['schedule']:
            session = pilot.new_session(cases,entry)
            baselines.append({'session_id':entry['session_id'], **{p:pilot.baseline(session,p) for p in ('entropy','random_split')}})
        pilot.save_json(evidence/'BASELINES.json',baselines)
        print('Frozen 64-session schedule and matched baselines saved', flush=True)
        pilot.run(evidence/'plan.json',data,endpoint,model,evidence/'sessions')
        pilot.save_json(evidence/'REPLAY.json',pilot.replay(evidence/'sessions',data))
        print((evidence/'REPLAY.json').read_text(),flush=True)
    finally:
        server.stop()
        for log in Path('/tmp').glob('inference_server_8000_*.log'):
            shutil.copyfile(log, evidence/log.name)
        archive = shutil.make_archive(str(evidence), 'zip', evidence)
        Path(archive+'.sha256').write_text(pilot.sha(Path(archive).read_bytes())+'\n')
        print('Evidence archive:',archive,flush=True)


if __name__ == '__main__':
    main()
