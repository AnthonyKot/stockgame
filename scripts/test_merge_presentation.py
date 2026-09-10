"""Round-trip valuation modes through the actual CLI in a disposable checkout."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


class PresentationMergeTests(unittest.TestCase):
    def run_fixture(self, mode, existing=None):
        with tempfile.TemporaryDirectory(prefix='stockgame-presentation-test-') as folder:
            root = Path(folder)
            (root / 'scripts').mkdir()
            target = root / 'cases/sample'
            target.mkdir(parents=True)
            (root / 'scripts/merge_presentation.py').write_text((ROOT / 'scripts/merge_presentation.py').read_text())
            pr = {'intro': 'Starting evidence.', 'groups': [{'title': 'Business', 'metrics': [0, 1]}, {'title': 'Cash', 'metrics': [2, 3]}],
                  'metrics': [{'metric': str(i), 'label': str(i), 'context': 'Reported measure.'} for i in range(4)], 'valuation_context': 'The input dates differ.'}
            if mode != 'omitted':
                pr['valuation_mode'] = mode
            source = target / 'presentation.json'
            source.write_text(json.dumps(pr))
            player = {'financial_snapshot': {'headline': [{'label': str(i)} for i in range(4)]}}
            if existing:
                player['financial_snapshot']['presentation'] = {'valuation_mode': existing}
            destination = target / 'player.json'
            destination.write_text(json.dumps(player))
            before = destination.read_bytes()
            result = subprocess.run(['python3', str(root / 'scripts/merge_presentation.py')], capture_output=True, text=True)
            return result.returncode, json.loads(destination.read_text()), source.exists(), destination.read_bytes() == before

    def test_explicit_modes_survive(self):
        for mode in ['pipeline', 'bank', 'revenue']:
            with self.subTest(mode=mode):
                code, player, remains, _ = self.run_fixture(mode)
                self.assertEqual(code, 0)
                self.assertEqual(player['financial_snapshot']['presentation']['valuation_mode'], mode)
                self.assertFalse(remains)

    def test_omitted_mode_keeps_existing(self):
        code, player, _, _ = self.run_fixture('omitted', existing='pipeline')
        self.assertEqual(code, 0)
        self.assertEqual(player['financial_snapshot']['presentation']['valuation_mode'], 'pipeline')

    def test_omitted_mode_defaults_without_inventing_field(self):
        code, player, _, _ = self.run_fixture('omitted')
        self.assertEqual(code, 0)
        self.assertNotIn('valuation_mode', player['financial_snapshot']['presentation'])

    def test_invalid_mode_preserves_input_and_destination(self):
        for mode in ['typo', None]:
            code, _, remains, unchanged = self.run_fixture(mode)
            self.assertEqual(code, 1)
            self.assertTrue(remains)
            self.assertTrue(unchanged)


if __name__ == '__main__':
    unittest.main()
