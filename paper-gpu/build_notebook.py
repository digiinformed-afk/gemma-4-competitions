from pathlib import Path
import base64,gzip,json
repo=Path(__file__).resolve().parents[1];d=repo/'paper-gpu';project=repo/'Google - The Gemma 4 Developer Agent Paper Track/PatchQuestions_Local/public/project'
files={name:base64.b64encode((project/name).read_bytes()).decode() for name in ('pilot.py','frozen_cases.jsonl.gz')}
for name in ('gpu_worker.py','offline_install.py'):
 files[name]=base64.b64encode((d/name).read_bytes()).decode()
payload=base64.b64encode(gzip.compress(json.dumps(files).encode(),mtime=0)).decode()
extract=f'''import sys
assert sys.version_info[:2] == (3, 12), 'Fork the working Python 3.12 notebook and pin its original environment'
print('Python runtime:', sys.version)
import base64, gzip, json, os
from pathlib import Path
root = Path('/kaggle/working/patchquestions-code')
root.mkdir(exist_ok=True)
files = json.loads(gzip.decompress(base64.b64decode({payload!r})))
for name, encoded in files.items():
    (root/name).write_bytes(base64.b64decode(encoded))
print('Extracted', len(files), 'versioned files')
'''
def cell(source,kind='code'):
 c={'cell_type':kind,'metadata':{},'source':source.splitlines(True)}
 if kind=='code':c.update(execution_count=None,outputs=[])
 return c
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'}},'cells':[
cell('# PatchQuestions — Gemma GPU pilot\n\n64 sessions, including 16 named/masked pairs and two controls. Attach the organizer wheelhouse and Gemma 4 31B QAT model version 2. Select an eligible GPU. Internet must be disabled on L4. Save version with outputs.\n','markdown'),cell(extract),
cell("import subprocess, sys\nsubprocess.run([sys.executable, str(root/'offline_install.py')], check=True)\n"),
cell("with (root/'worker.log').open('w') as log:\n    process = subprocess.Popen([sys.executable, '-u', str(root/'gpu_worker.py')], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)\n    for line in process.stdout:\n        log.write(line); log.flush(); print(line, end='', flush=True)\n    returncode = process.wait()\nif returncode:\n    raise subprocess.CalledProcessError(returncode, process.args)\n")]}
(d/'PatchQuestions_GPU_Pilot.ipynb').write_text(json.dumps(nb,indent=1)+'\n')
# Refresh embedded evaluator in the canonical CPU notebook without claiming old outputs apply to new source.
p=project/'PatchQuestions.ipynb';cpu=json.loads(p.read_text());
for c in cpu['cells']:
 src=''.join(c['source'])
 if "Path('pilot.py').write_text(" in src:
  c['source']=["Path('pilot.py').write_text("+repr((project/'pilot.py').read_text())+", encoding='utf-8')\n"]
for c in cpu['cells']:
 if c['cell_type']=='code':c['execution_count']=None;c['outputs']=[]
p.write_text(json.dumps(cpu,indent=1)+'\n')
