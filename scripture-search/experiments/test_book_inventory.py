import hashlib
import unittest

from book_inventory import parse_record


class InventoryParserTest(unittest.TestCase):
    def test_book_settings_supply_reference_prefix(self):
        raw = '# Text\nśloka /\nsecond // example_1.1 //\n'.encode()
        record = {'id': 'example', 'source_sha256': hashlib.sha256(raw).hexdigest(),
                  'parser_profile': 'numbered-multiline-verse',
                  'parser_settings': {'siglum': 'example'}}
        result = parse_record(record, raw)
        self.assertEqual(result['passages'][0]['reference'], 'example_1.1')
        self.assertEqual(result['profile'], 'numbered-multiline-verse')

    def test_changed_book_is_rejected(self):
        record = {'id': 'example', 'source_sha256': '0' * 64,
                  'parser_profile': 'numbered-multiline-verse', 'parser_settings': {'siglum': 'example'}}
        with self.assertRaisesRegex(ValueError, 'hash'):
            parse_record(record, b'# Text\nverse // example_1.1 //\n')

    def test_unknown_profile_is_rejected(self):
        raw = b'data'
        record = {'id': 'example', 'source_sha256': hashlib.sha256(raw).hexdigest(),
                  'parser_profile': 'unknown', 'parser_settings': {}}
        with self.assertRaisesRegex(ValueError, 'profile'):
            parse_record(record, raw)

    def test_common_markers_are_observations_not_guaranteed_boundaries(self):
        raw = '# Text\nअर्ध । पूर्ण ॥\n'.encode()
        record = {'id': 'example', 'source_sha256': hashlib.sha256(raw).hexdigest(),
                  'parser_profile': 'numbered-multiline-verse', 'parser_settings': {'siglum': 'example'}}
        result = parse_record(record, raw)
        self.assertEqual(result['observed_markers']['devanagari_double_danda'], 1)
        self.assertFalse(any(p['role'] == 'verse' for p in result['passages']))
