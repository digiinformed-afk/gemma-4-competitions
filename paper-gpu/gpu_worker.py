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
    server = VllmServer(VllmConfig(model=str(model), port=8000, host='127.0.0.1',
        tensor_parallel_size=4 if gpu_count>=4 else (2 if gpu_count>=2 else 1),
        reasoning_parser='gemma4', max_model_len=32768,
        dtype='bfloat16' if torch.cuda.is_bf16_supported() else 'auto',
        gpu_memory_utilization=0.90, scheduler_reserve_full_isl=False,
        enable_auto_tool_choice=False, enable_lora=False, startup_timeout=1200))
    try:
        server.start()
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
        # Disjoint synthetic calibration; no benchmark target is used here.
        messages = [{'role':'system','content':'Reply with exactly {"pick":0}.'},
                    {'role':'user','content':'Synthetic transport check. Output the required JSON.'}]
        request = pilot.model_request(messages, info)
        with opener.open(Request(endpoint+'/v1/chat/completions', data=pilot.encode(request).encode(),
                                 headers={'Content-Type':'application/json'}), timeout=180) as response:
            raw = json.load(response)
        local_count = pilot.count_tokens(tokenizer, messages, info)
        pilot.save_json(evidence/'CALIBRATION.json', {'request':request, 'response':raw, 'local_prompt_tokens':local_count})
        actual = raw.get('usage',{}).get('prompt_tokens')
        if actual is None or actual != local_count:
            raise RuntimeError(f'Calibration token count differs: local={local_count}, server={actual}; preserve calibration and fix template before scored run')
        pilot.parse_action(raw['choices'][0]['message']['content'])
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
        pilot.run(evidence/'plan.json',data,endpoint,model,evidence/'sessions')
        pilot.save_json(evidence/'REPLAY.json',pilot.replay(evidence/'sessions',data))
        print((evidence/'REPLAY.json').read_text(),flush=True)
    finally:
        server.stop()
        archive = shutil.make_archive(str(evidence), 'zip', evidence)
        Path(archive+'.sha256').write_text(pilot.sha(Path(archive).read_bytes())+'\n')
        print('Evidence archive:',archive,flush=True)


if __name__ == '__main__':
    main()
