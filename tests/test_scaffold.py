"""Scaffold smoke tests: every module imports and the entry points answer. No product behaviour."""

import importlib
import subprocess
import sys
import unittest

MODULES = [
    "retail_pos", "retail_pos.cli", "retail_pos.http_common", "retail_pos.money",
    "retail_pos.contract", "retail_pos.faultlink", "retail_pos.faults",
    "retail_pos.demo", "retail_pos.evidence", "retail_pos.evidence_check",
    "retail_pos.store", "retail_pos.store.db", "retail_pos.store.checkout",
    "retail_pos.store.shifts", "retail_pos.store.refunds", "retail_pos.store.outbox",
    "retail_pos.store.sync", "retail_pos.store.routes",
    "retail_pos.head_office", "retail_pos.head_office.db", "retail_pos.head_office.ingest",
    "retail_pos.head_office.reports", "retail_pos.head_office.routes",
]


def run(*args):
    return subprocess.run([sys.executable, "-m", *args], capture_output=True, text=True, timeout=30)


class ImportSmoke(unittest.TestCase):
    def test_every_module_imports_and_has_a_docstring(self):
        for name in MODULES:
            with self.subTest(module=name):
                self.assertTrue(importlib.import_module(name).__doc__)


class EntryPointSmoke(unittest.TestCase):
    def test_help_and_version(self):
        self.assertIn("--role", run("retail_pos", "--help").stdout)
        result = run("retail_pos", "--version")
        self.assertEqual(result.returncode, 0)
        self.assertIn("retail_pos", result.stdout)

    def test_unbuilt_commands_exit_non_zero_with_ticket(self):
        for module, ticket in [("retail_pos", 11), ("retail_pos.demo", 15),
                               ("retail_pos.evidence", 35), ("retail_pos.evidence_check", 35)]:
            with self.subTest(module=module):
                result = run(module)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"not implemented yet: see #{ticket}", result.stderr)


if __name__ == "__main__":
    unittest.main()
