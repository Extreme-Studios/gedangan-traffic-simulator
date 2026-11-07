import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from backend.gedangan import m08_workflow as workflow


class BrowserRebuildTests(unittest.TestCase):
    def cases(self, legacy=None, extra=None):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name, value in [('browser-run-request.json', legacy),
                                ('browser-run-requests.json', extra)]:
                if value is not None:
                    (root / name).write_text(json.dumps(value), encoding='utf-8')
            with patch.object(workflow, 'DOC', root):
                return workflow.browser_validation_cases()

    def valid(self, solution='S03'):
        return dict(solution=solution, year=2035, growth='REFERENCE',
                    seed=42, family='pilot-provisional')

    def test_legacy_and_additional_actual_browser_cases_both_replayed(self):
        first, second = self.valid('S04'), self.valid()
        self.assertEqual(self.cases(first, [second]), [first, second])

    def test_concepts_and_incompatible_parent_rejected_before_execution(self):
        for case in [self.valid('S06'), {**self.valid(), 'family': 'pilot-strict'}]:
            with self.assertRaises(ValueError):
                self.cases(extra=[case])

    def test_unbounded_or_invalid_request_rejected(self):
        for cases in [[self.valid()] * 5,
                      [{**self.valid(), 'year': True}],
                      [{**self.valid(), 'seed': 11}],
                      [{**self.valid(), 'unexpected': 1}]]:
            with self.assertRaises(ValueError):
                self.cases(extra=cases)

    def test_no_browser_cases_is_valid_for_offline_rebuild(self):
        self.assertEqual(self.cases(), [])
