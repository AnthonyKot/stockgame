"""Round-trip valuation modes and multi-file failure recovery on disposable fixtures."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import merge_presentation as merger

ROOT = Path(__file__).resolve().parent.parent


def block(cid=None, mode='omitted'):
    pr = {
        'intro': 'Starting evidence.',
        'groups': [{'title': 'Business', 'metrics': [0, 1]}, {'title': 'Cash', 'metrics': [2, 3]}],
        'metrics': [{'metric': str(i), 'label': str(i), 'context': 'Reported measure.'} for i in range(4)],
        'valuation_context': 'The input dates differ.',
    }
    if cid is not None:
        pr['candidate_id'] = cid
    if mode != 'omitted':
        pr['valuation_mode'] = mode
    return pr


def player_fixture(existing_mode=None, with_stored=False, cid=None):
    snapshot = {'headline': [{'label': str(i)} for i in range(4)]}
    if with_stored:
        stored = block(mode=existing_mode if existing_mode is not None else 'omitted')
        snapshot['presentation'] = stored
    elif existing_mode:
        snapshot['presentation'] = {'valuation_mode': existing_mode}
    return {'financial_snapshot': snapshot}


class PresentationMergeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='stockgame-presentation-batch-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'cases').mkdir()
        self.before = {}
        for cid in ['one', 'two']:
            folder = self.root / 'cases' / cid
            folder.mkdir()
            (folder / 'presentation.json').write_text(json.dumps(block(cid=cid, mode='revenue')))
            pj = folder / 'player.json'
            pj.write_text(json.dumps(player_fixture(existing_mode='pipeline', with_stored=True)))
            self.before[cid] = pj.read_bytes()

    def source(self, cid='one'):
        return self.root / 'cases' / cid / 'presentation.json'

    def destination(self, cid='one'):
        return self.root / 'cases' / cid / 'player.json'

    def change(self, fn, cid='two'):
        value = json.loads(self.source(cid).read_text())
        fn(value)
        self.source(cid).write_text(json.dumps(value))

    def assert_preserved(self):
        for cid in ['one', 'two']:
            self.assertEqual(self.destination(cid).read_bytes(), self.before[cid])
            self.assertTrue(self.source(cid).exists())
            self.assertEqual(list((self.root / 'cases' / cid).glob('*.tmp')), [])

    def run_fixture(self, mode, existing=None):
        with tempfile.TemporaryDirectory(prefix='stockgame-presentation-test-') as folder:
            root = Path(folder)
            (root / 'scripts').mkdir()
            target = root / 'cases/sample'
            target.mkdir(parents=True)
            (root / 'scripts/merge_presentation.py').write_text((ROOT / 'scripts/merge_presentation.py').read_text())
            source = target / 'presentation.json'
            source.write_text(json.dumps(block(mode=mode)))
            destination = target / 'player.json'
            destination.write_text(json.dumps(player_fixture(existing_mode=existing)))
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

    def test_mixed_invalid_batch_does_not_write_or_delete(self):
        self.change(lambda d: d.update(valuation_context=' '.join(['word'] * 46)))
        errors, count = merger.merge(self.root)
        self.assertTrue(errors)
        self.assertEqual(count, 0)
        self.assert_preserved()

    def test_unknown_candidate_and_mismatch_rejected(self):
        extra = self.root / 'cases/unknown'
        extra.mkdir()
        (extra / 'presentation.json').write_text(json.dumps(block(cid='unknown')))
        self.change(lambda d: d.update(candidate_id='one'))
        errors, count = merger.merge(self.root)
        self.assertTrue(any('unknown candidate writer input' in e for e in errors))
        self.assertTrue(any('candidate_id' in e for e in errors))
        self.assertEqual(count, 0)
        self.assert_preserved()

    def test_bad_json_rejected(self):
        self.source('two').write_text('{')
        errors, count = merger.merge(self.root)
        self.assertTrue(any('invalid input' in e for e in errors))
        self.assertEqual(count, 0)
        self.assert_preserved()

    def test_check_only_keeps_everything(self):
        self.assertEqual(merger.merge(self.root, True), ([], 0))
        self.assert_preserved()

    def test_failed_flush_preserves_inputs_and_destinations(self):
        with patch.object(merger.os, 'fsync', side_effect=OSError('disk full')):
            errors, count = merger.merge(self.root)
        self.assertTrue(any('save failed' in e for e in errors))
        self.assertEqual(count, 0)
        self.assert_preserved()

    def test_mid_batch_replace_failure_rolls_back_first_file_and_retains_inputs(self):
        original_replace = merger.os.replace
        target_two = self.destination('two')

        def fail_on_second(src, dst, *args, **kwargs):
            if Path(dst) == target_two:
                raise OSError('replace blocked on second case')
            return original_replace(src, dst, *args, **kwargs)

        with patch.object(merger.os, 'replace', side_effect=fail_on_second):
            errors, count = merger.merge(self.root)
        self.assertTrue(any('save failed' in e for e in errors))
        self.assertEqual(count, 0)
        self.assert_preserved()

    def test_success_and_stored_validation_rerun(self):
        self.change(lambda d: d.update(intro='Updated starting evidence.'))
        self.assertEqual(merger.merge(self.root), ([], 2))
        self.assertEqual(
            json.loads(self.destination('two').read_text())['financial_snapshot']['presentation']['intro'],
            'Updated starting evidence.',
        )
        self.assertFalse(self.source('one').exists())
        self.assertFalse(self.source('two').exists())
        after_one = self.destination('one').read_bytes()
        after_two = self.destination('two').read_bytes()
        self.assertEqual(merger.merge(self.root), ([], 0))
        self.assertEqual(self.destination('one').read_bytes(), after_one)
        self.assertEqual(self.destination('two').read_bytes(), after_two)

    def test_cleanup_failure_is_recoverable(self):
        original = Path.unlink
        source_one = self.source('one')

        def fail_one(path, *args, **kwargs):
            if path == source_one:
                raise OSError('cleanup blocked')
            return original(path, *args, **kwargs)

        with patch.object(Path, 'unlink', fail_one):
            errors, count = merger.merge(self.root)
        self.assertEqual(count, 2)
        self.assertTrue(any('cleanup failed' in e for e in errors))
        self.assertTrue(source_one.exists())
        self.assertFalse(self.source('two').exists())
        after_one = self.destination('one').read_bytes()
        self.assertEqual(merger.merge(self.root), ([], 1))
        self.assertEqual(self.destination('one').read_bytes(), after_one)


if __name__ == '__main__':
    unittest.main()
