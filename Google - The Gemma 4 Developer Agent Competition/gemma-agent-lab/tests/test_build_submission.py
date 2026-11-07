import hashlib
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'build-submission.py'
spec = importlib.util.spec_from_file_location('pack_agent', SCRIPT)
pack = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pack)


class BuildTests(unittest.TestCase):
    def setUp(self):
        workspace = tempfile.TemporaryDirectory()
        self.addCleanup(workspace.cleanup)
        self.base = Path(workspace.name)
        self.sample = self.base / 'sample'
        (self.sample / 'prompts').mkdir(parents=True)
        self.config = self.sample / 'agent.yaml'
        self.config.write_bytes(b'name: repair\r\nmodel: sample\r\ninstruction: !include "prompts/base.md"  # preserve issue\r\ntools:\r\n- submit_patch\r\n')
        (self.sample / 'prompts/base.md').write_bytes(b'Repair {problem_description}.\r\n')
        self.policy = self.base / 'policy.md'
        self.policy.write_text('Check nearby tests.\nKeep time for submission.\n', encoding='utf-8')
        self.zip = self.base / 'candidate.zip'

    def build_local(self, policy):
        with patch.object(pack, 'validate_official', return_value='unavailable'):
            return pack.build(self.sample, self.zip, policy)

    def test_control_preserves_members_and_is_reproducible(self):
        (self.sample / 'adapter_model.safetensors').write_bytes(b'fixture')
        result = self.build_local(None)
        self.assertEqual(result['variant'], 'baseline')
        self.assertEqual(result['sha256'], hashlib.sha256(self.zip.read_bytes()).hexdigest())
        with zipfile.ZipFile(self.zip) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(archive.namelist(), ['adapter_model.safetensors', 'agent.yaml', 'prompts/base.md'])
            for name in archive.namelist():
                self.assertEqual(archive.read(name), (self.sample / name).read_bytes())
        os.utime(self.config, (1_700_000_000, 1_700_000_000))
        self.assertEqual(self.build_local(None), result)

    def test_overlay_keeps_issue_template_and_other_agents(self):
        (self.sample / 'sub_agents').mkdir()
        other = self.sample / 'sub_agents/analysis.yaml'
        other.write_bytes(b'name: analyzer\ninstruction: original\n')
        original = self.config.read_bytes()
        self.build_local(self.policy)
        with zipfile.ZipFile(self.zip) as archive:
            self.assertEqual(archive.read('sub_agents/analysis.yaml'), other.read_bytes())
            self.assertEqual(archive.read('prompts/base.md'), (self.sample / 'prompts/base.md').read_bytes())
            self.assertIn(b'instruction: !include prompts/root-repair-policy.md\r\ntools:', archive.read('agent.yaml'))
            self.assertEqual(archive.read(pack.POLICY_MEMBER), b'Repair {problem_description}.\r\n\n\nCheck nearby tests.\nKeep time for submission.\n')
        self.assertEqual(self.config.read_bytes(), original)

    def test_inline_scalars(self):
        for value, expected in [ ('Fix the issue # note', 'Fix the issue'),
                                 ("'Fix user''s issue'", "Fix user's issue"),
                                 ('"Fix the issue\\n{hints}"', 'Fix the issue\n{hints}') ]:
            with self.subTest(value=value):
                self.config.write_text('instruction: ' + value + '\ntools: []\n', encoding='utf-8')
                self.build_local(self.policy)
                with zipfile.ZipFile(self.zip) as archive:
                    self.assertTrue(archive.read(pack.POLICY_MEMBER).decode('utf-8').startswith(expected + '\n\n'))

    def test_literal_and_folded_blocks_keep_other_root_fields(self):
        for style, policy_indent in [('|-', '  '), ('>2-', '    ')]:
            with self.subTest(style=style):
                original = f'instruction: {style}\n  Repair\n  {{problem_description}}.'
                self.config.write_bytes((original + '\ntools:\n- submit_patch\n').encode())
                self.build_local(self.policy)
                with zipfile.ZipFile(self.zip) as archive:
                    self.assertEqual(archive.read('agent.yaml').decode(), original + '\n\n' + policy_indent + 'Check nearby tests.\n' + policy_indent + 'Keep time for submission.\ntools:\n- submit_patch\n')

    def test_invalid_include_or_conflicting_overlay_preserves_previous_zip(self):
        self.build_local(None)
        previous = self.zip.read_bytes()
        for path in ['../outside.md', '/outside.md', 'C:/outside.md', 'prompts/data.yaml', 'prompts/missing.md']:
            with self.subTest(path=path):
                self.config.write_text('instruction: !include ' + path, encoding='utf-8')
                with self.assertRaises((ValueError, FileNotFoundError)):
                    self.build_local(self.policy)
                self.assertEqual(previous, self.zip.read_bytes())
        self.config.write_text('instruction: fix this', encoding='utf-8')
        (self.sample / pack.POLICY_MEMBER).touch()
        with self.assertRaisesRegex(ValueError, 'overlay file'):
            self.build_local(self.policy)

    def test_layout_and_size_guards(self):
        with self.assertRaisesRegex(ValueError, 'outside'):
            pack.build(self.sample, self.sample / 'bad.zip', None)
        alternate = self.sample / 'root_agent.yml'
        alternate.touch()
        with self.assertRaisesRegex(ValueError, 'one root'):
            self.build_local(None)
        alternate.unlink()
        with patch.object(pack, 'MAX_BYTES', 1), self.assertRaisesRegex(ValueError, '3 GiB'):
            self.build_local(None)
        (self.sample / 'private.zip').touch()
        with self.assertRaisesRegex(ValueError, 'Unsupported sample member'):
            self.build_local(None)

    def test_rejects_link_before_copy(self):
        try:
            (self.sample / 'linked.md').symlink_to(self.policy)
        except OSError as error:
            if getattr(error, 'winerror', None) != 1314:
                raise
            import _winapi
            # Directory junctions need no Windows symlink-creation privilege.
            target = self.base / 'outside'
            target.mkdir()
            _winapi.CreateJunction(str(target), str(self.sample / 'linked-directory'))
        with self.assertRaisesRegex(ValueError, 'Links and reparse'):
            self.build_local(None)

    def test_failed_official_validation_cannot_replace_previous_archive(self):
        self.build_local(None)
        previous = self.zip.read_bytes()
        def reject(stage, required):
            self.assertTrue(required)
            self.assertTrue((stage / pack.POLICY_MEMBER).is_file())
            raise ValueError('official validator rejected fixture')
        with patch.object(pack, 'validate_official', side_effect=reject), self.assertRaisesRegex(ValueError, 'rejected fixture'):
            pack.build(self.sample, self.zip, self.policy, require_official=True)
        self.assertEqual(previous, self.zip.read_bytes())


if __name__ == '__main__':
    unittest.main()
