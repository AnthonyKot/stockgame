"""Failure-path checks on disposable fixtures; never edits repository case data."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import merge_dated_debrief as merger


def block(cid):
    return {'candidate_id': cid, 'baseline': {'narrative': 'Starting record.', 'checks': {'a1': 'Unresolved. No result yet.'}},
            'updates': [{'event_ids': [f'e{i}'], 'checks': {'a1': 'Supported. Evidence supports the effect.'}} for i in range(4)]}


class MergeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='stockgame-merge-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'cases').mkdir()
        self.scenes = self.root / 'cases/scenes.json'
        data = {'scenes': {}}
        for cid in ['one', 'two']:
            folder = self.root / 'cases' / cid
            folder.mkdir()
            data['scenes'][cid] = {'assumptions': [{'id': 'a1'}], 'dated_debrief': block(cid)}
            (folder / 'dated_debrief.json').write_text(json.dumps(block(cid)))
            (folder / 'aftermath.json').write_text(json.dumps({'events': [
                {'id': f'e{i}', 'date': f'2020-01-0{i+1}', 'source': {'published': f'2020-02-0{i+1}'}} for i in range(4)]}))
        self.scenes.write_text(json.dumps(data))
        self.before = self.scenes.read_bytes()

    def source(self, cid='one'):
        return self.root / 'cases' / cid / 'dated_debrief.json'

    def change(self, fn, cid='two'):
        value = json.loads(self.source(cid).read_text())
        fn(value)
        self.source(cid).write_text(json.dumps(value))

    def assert_preserved(self):
        self.assertEqual(self.scenes.read_bytes(), self.before)
        self.assertTrue(self.source('one').exists())
        self.assertTrue(self.source('two').exists())
        self.assertEqual(list(self.scenes.parent.glob('*.tmp')), [])

    def test_mixed_invalid_batch_does_not_write_or_delete(self):
        self.change(lambda d: d['updates'][0].update(narrative=' '.join(['word'] * 46)))
        errors, count = merger.merge(self.root)
        self.assertTrue(errors)
        self.assertEqual(count, 0)
        self.assert_preserved()

    def test_unknown_event_is_a_validation_error_including_check_only(self):
        self.change(lambda d: d['updates'][0].update(event_ids=['missing']))
        for check_only in [True, False]:
            errors, count = merger.merge(self.root, check_only)
            self.assertTrue(any('unknown event missing' in e for e in errors))
            self.assertEqual(count, 0)
            self.assert_preserved()

    def test_bad_date_rejected(self):
        path = self.root / 'cases/two/aftermath.json'
        data = json.loads(path.read_text())
        data['events'][0]['source']['published'] = '2020-02-30'
        path.write_text(json.dumps(data))
        errors, _ = merger.merge(self.root)
        self.assertTrue(errors)
        self.assert_preserved()

    def test_bad_json_rejected(self):
        self.source('two').write_text('{')
        errors, _ = merger.merge(self.root)
        self.assertTrue(any('invalid input' in e for e in errors))
        self.assert_preserved()

    def test_candidate_identity_rejected(self):
        self.change(lambda d: d.update(candidate_id='one'))
        errors, _ = merger.merge(self.root)
        self.assertTrue(any('candidate_id' in e for e in errors))
        self.assert_preserved()

    def test_bad_baseline_and_unknown_assumption_rejected(self):
        self.change(lambda d: d['baseline']['checks'].update(a1=None, extra='Unresolved. Unknown assumption.'))
        errors, _ = merger.merge(self.root)
        self.assertTrue(any('exactly' in e for e in errors))
        self.assert_preserved()

    def test_check_only_keeps_everything(self):
        self.assertEqual(merger.merge(self.root, True), ([], 0))
        self.assert_preserved()

    def test_failed_flush_preserves_inputs_and_destination(self):
        with patch.object(merger.os, 'fsync', side_effect=OSError('disk full')):
            errors, count = merger.merge(self.root)
        self.assertTrue(any('save failed' in e for e in errors))
        self.assertEqual(count, 0)
        self.assert_preserved()

    def test_failed_replace_preserves_inputs_and_destination(self):
        with patch.object(merger.os, 'replace', side_effect=OSError('replace blocked')):
            errors, count = merger.merge(self.root)
        self.assertTrue(any('save failed' in e for e in errors))
        self.assertEqual(count, 0)
        self.assert_preserved()

    def test_success_and_rerun(self):
        self.change(lambda d: d['baseline'].update(narrative='Updated record.'))
        self.assertEqual(merger.merge(self.root), ([], 2))
        self.assertEqual(json.loads(self.scenes.read_text())['scenes']['two']['dated_debrief']['baseline']['narrative'], 'Updated record.')
        self.assertFalse(self.source().exists())
        after = self.scenes.read_bytes()
        self.assertEqual(merger.merge(self.root), ([], 0))
        self.assertEqual(self.scenes.read_bytes(), after)

    def test_cleanup_failure_is_recoverable(self):
        original = Path.unlink
        source = self.source('one')
        def fail_one(path, *args, **kwargs):
            if path == source:
                raise OSError('cleanup blocked')
            return original(path, *args, **kwargs)
        with patch.object(Path, 'unlink', fail_one):
            errors, count = merger.merge(self.root)
        self.assertEqual(count, 2)
        self.assertTrue(any('cleanup failed' in e for e in errors))
        self.assertTrue(source.exists())
        after = self.scenes.read_bytes()
        self.assertEqual(merger.merge(self.root), ([], 1))
        self.assertEqual(self.scenes.read_bytes(), after)

    def test_month_precision_and_valid_reassessment(self):
        self.assertEqual(merger.last_day('2020-02'), '2020-02-29')
        self.change(lambda d: d['updates'][1]['checks'].update(a1='Unresolved. Replication withdrew support for the initial effect.'))
        self.assertEqual(merger.merge(self.root), ([], 2))


if __name__ == '__main__':
    unittest.main()
