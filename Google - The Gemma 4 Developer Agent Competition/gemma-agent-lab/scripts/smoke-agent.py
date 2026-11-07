"""CPU integration smoke for the candidate using the organizer compiler and ADK Runner.

The model is scripted. SWEGemma supplies the tools and competition limits.
A local transport maps the fixture's file and command operations into a temporary
repository. A second repository checks the captured patch independently.
"""

import argparse
import asyncio
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

from adk_submission import ModelRegistry, compile_submission, discover_declared_models
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from swegemma.config import build_submission_limits
from swegemma.context import SwegemmaContext
from swegemma.sandbox.base import ExecResult
import yaml


MODEL = 'gemma-4-31b-it-qat-w4a16-ct'
ISSUE = 'clip(value, upper) should clamp at both zero and the supplied upper bound.'
COMMAND = 'python -m unittest -q test_bounds'
OLD = 'return max(value, 0)'
NEW = 'return min(max(value, 0), upper)'
STEPS = [
    ('get_status', {}),
    ('read_file', {'filepath': 'bounds.py'}),
    ('run_command', {'command': COMMAND}),
    ('edit_file', {'filepath': 'bounds.py', 'old_string': OLD, 'new_string': NEW}),
    ('run_command', {'command': COMMAND}),
    ('submit_patch', {}),
]
TESTS = '''import unittest
from bounds import clip

class Bounds(unittest.TestCase):
    def test_upper_bound(self):
        self.assertEqual(clip(7, 5), 5)
    def test_neighbors(self):
        self.assertEqual(clip(-2, 5), 0)
        self.assertEqual(clip(3, 5), 3)
'''


class ScriptedModel(BaseLlm):
    async def generate_content_async(self, llm_request, stream=False):
        parts = [part for content in llm_request.contents for part in content.parts or []]
        if not any(ISSUE in (part.text or '') for part in parts):
            raise RuntimeError('Issue was missing from the model request')
        completed = [part.function_response.name for part in parts if part.function_response]
        if completed != [name for name, _ in STEPS[:len(completed)]]:
            raise RuntimeError(f'Unexpected tool responses: {completed}')
        if len(completed) < len(STEPS):
            name, args = STEPS[len(completed)]
            part = types.Part.from_function_call(name=name, args=args)
        else:
            part = types.Part.from_text(text='Captured the upper-bound repair and ran the fixture tests.')
        yield LlmResponse(content=types.Content(role='model', parts=[part]))


def git(directory, *args, data=None):
    return subprocess.run(['git', '-c', 'core.autocrlf=false', *args], cwd=directory, input=data,
                          capture_output=True, check=True, timeout=20).stdout


def fixture(directory):
    directory.mkdir()
    git(directory, 'init', '--quiet', '--template=')
    (directory / 'bounds.py').write_bytes(f'def clip(value, upper):\n    {OLD}\n'.encode())
    (directory / 'test_bounds.py').write_bytes(TESTS.encode())
    git(directory, 'add', '--', 'bounds.py', 'test_bounds.py')
    git(directory, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@localhost',
        'commit', '--quiet', '--no-gpg-sign', '-m', 'Fixture baseline')
    git(directory, 'tag', '_swegemma_baseline')


def regression(directory):
    result = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-q', 'test_bounds'],
                            cwd=directory, capture_output=True, text=True, timeout=20)
    if 'Ran 2 tests' not in result.stderr:
        raise RuntimeError(f'The two regression tests did not run: {result.stderr}')
    return result


class FixtureTransport:
    """The three sandbox operations exercised by the pinned tool sequence."""

    def __init__(self, work):
        self.work = work
        self.test_exits = []

    def copy_from(self, container_id, source, destination):
        path = Path(source)
        if not path.root or path.parts[1:] != ('workspace', 'bounds.py'):
            raise ValueError(f'Unexpected fixture source {source}')
        shutil.copyfile(self.work / 'bounds.py', destination)

    def copy_to(self, container_id, source, destination):
        path = Path(destination)
        if not path.root or path.parts[1:] != ('workspace',) or Path(source).name != 'bounds.py':
            raise ValueError(f'Unexpected fixture destination {destination}')
        shutil.copyfile(source, self.work / 'bounds.py')

    def exec(self, container_id, command, timeout=None):
        if command == COMMAND:
            result = regression(self.work)
            self.test_exits.append(result.returncode)
            return ExecResult(exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr)
        if command == 'cd /workspace && git add -N .':
            git(self.work, 'add', '-N', '.')
            return ExecResult()
        if command == 'cd /workspace && (git diff --binary _swegemma_baseline 2>/dev/null || git diff --binary HEAD)':
            diff = git(self.work, 'diff', '--binary', '_swegemma_baseline')
            return ExecResult(stdout=diff.decode('utf-8'))
        raise ValueError(f'Unexpected fixture command {command}')


async def smoke(candidate, root):
    work, fresh = root / 'agent-work', root / 'fresh-grade'
    fixture(work)
    fixture(fresh)
    transport = FixtureTransport(work)
    budget = yaml.safe_load((candidate / 'eval_config.yaml').read_text(encoding='utf-8'))['evaluation']
    context = SwegemmaContext(docker_manager=transport, container_id='fixture',
                              problem_statement=ISSUE, repo='fixture/bounds', task_id='clamp',
                              max_tool_calls=budget['max_tool_calls'], max_time_minutes=budget['max_time_minutes'])
    limits, generation = build_submission_limits()
    if discover_declared_models(candidate) != {MODEL}:
        raise ValueError('Expected one 31B model in the candidate')
    registry = ModelRegistry()
    registry.register(MODEL, ScriptedModel(model='offline-scripted-fixture'))
    agent = compile_submission(candidate, tool_registry=context.create_tools(), model_registry=registry,
                               limits=limits, generation_constraints=generation)
    service = InMemorySessionService()
    runner = Runner(agent=agent, app_name='repair_smoke', session_service=service)
    session = await service.create_session(app_name='repair_smoke', user_id='fixture',
                                           state={'problem_description': ISSUE, 'hints': ''})
    observed = []
    final = ''
    async for event in runner.run_async(user_id='fixture', session_id=session.id,
                                        new_message=types.Content(role='user', parts=[types.Part.from_text(text=ISSUE)])):
        observed.extend(call.name for call in event.get_function_calls())
        for response in event.get_function_responses():
            payload = response.response or {}
            if response.name != 'run_command' and payload.get('status') == 'error':
                raise RuntimeError(f'{response.name} failed in fixture: {payload}')
        if event.is_final_response() and event.content:
            final = ''.join(part.text or '' for part in event.content.parts or [])
    codes = transport.test_exits
    if observed != [name for name, _ in STEPS] or not final or codes != [1, 0] or not context.patch_submitted:
        raise RuntimeError(f'Incomplete ADK loop: calls={observed}, test exits={codes}, submitted={context.patch_submitted}')

    diff = (context.submitted_patch or '').encode('utf-8')
    if diff.count(b'diff --git ') != 1 or not diff.startswith(b'diff --git a/bounds.py b/bounds.py\n'):
        raise RuntimeError('Expected a single source-file patch')
    if regression(fresh).returncode != 1:
        raise RuntimeError('Fresh fixture failed to reproduce the defect')
    git(fresh, 'apply', '--check', '--whitespace=error', '-', data=diff)
    git(fresh, 'apply', '--whitespace=error', '-', data=diff)
    if regression(fresh).returncode != 0:
        raise RuntimeError('Regression failed after fresh application')
    return {'kind': 'scripted CPU fixture', 'model': 'scripted BaseLlm', 'tools': 'organizer SWEGemma tools',
            'sandbox': 'local fixture transport', 'swegemma': version('swegemma'),
            'charged_tool_calls': context.tool_calls_used,
            'adk_submission': version('adk-submission'), 'google_adk': version('google-adk'),
            'agent': agent.name, 'calls': observed, 'agent_test_exit_codes': codes,
            'patch_bytes': len(diff), 'patch_sha256': hashlib.sha256(diff).hexdigest(),
            'fresh_test_exit_codes': [1, 0], 'fresh_tests_passed': 2, 'final_response': final}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group()
    inputs.add_argument('--candidate', type=Path, default=Path(__file__).resolve().parents[1] / 'candidate')
    inputs.add_argument('--archive', type=Path, help='check the exact three-file standalone candidate ZIP')
    parser.add_argument('--report', type=Path, help='also save the JSON report at this path')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        candidate = args.candidate.resolve()
        if args.archive:
            candidate = root / 'unpacked'
            candidate.mkdir()
            with zipfile.ZipFile(args.archive) as archive:
                expected = ['agent.yaml', 'eval_config.yaml', 'instruction.md']
                if sorted(archive.namelist()) != expected:
                    raise ValueError('Expected exactly the three standalone candidate files at the archive root')
                for name in expected:
                    if archive.getinfo(name).file_size > 1024 * 1024:
                        raise ValueError(f'Unexpectedly large standalone fixture member {name}')
                    (candidate / name).write_bytes(archive.read(name))
        result = asyncio.run(smoke(candidate, root))
        if args.archive:
            result['archive_sha256'] = hashlib.sha256(args.archive.read_bytes()).hexdigest()
        report = json.dumps(result, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=args.report.parent, mode='w', encoding='utf-8', delete=False) as f:
            f.write(report + '\n')
        Path(f.name).replace(args.report)
    print(report)
