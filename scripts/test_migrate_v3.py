import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('migrate_v3', Path(__file__).with_name('migrate-v3.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class MigrationTests(unittest.TestCase):
    def test_retains_original_values_and_marks_source_labels_proposed(self):
        source = {'schema_version': '2.0', 'catalog_items': [{'id': 'x', 'traditions': ['A', 'B'], 'author': 'unknown'}],
                  'works': [], 'editions': [], 'work_targets': [],
                  'metadata_coverage': {'catalog_items': {'total': 99, 'traditions': 0}}}
        result = module.migrate(source)
        self.assertEqual(source['schema_version'], '2.0')
        self.assertEqual(result['catalog_items'][0]['traditions'], ['A', 'B'])
        self.assertEqual(result['metadata_coverage']['catalog_items']['total'], 1)
        self.assertEqual([a['source_label'] for a in result['facet_assertions']], ['A', 'B', 'unknown'])
        self.assertTrue(all(a['status'] == 'proposed' and a['normalized_value'] is None for a in result['facet_assertions']))

    def test_rejects_wrong_source_version(self):
        with self.assertRaises(ValueError):
            module.migrate({'schema_version': '3.0'})


if __name__ == '__main__':
    unittest.main()
