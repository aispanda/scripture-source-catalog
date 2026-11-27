import unittest
import passage_parser

class PassageParserTests(unittest.TestCase):
    def test_preserves_utf8_and_duplicate_markers(self):
        raw = '# Book\n\n```text\nśruti || 4 ||\n\nśakti || 4 ||\n\nunnumbered\n```\n'.encode()
        rows = passage_parser.parse(raw, 'example', 'Book', 'https://example.org')
        self.assertEqual(len(rows), 3)
        for row in rows:
            self.assertEqual(raw[row['byte_start']:row['byte_end']].decode(), row['text'])
        self.assertEqual([r['source_marker'] for r in rows], ['4', '4', None])
        self.assertEqual(len(set(r['chunk_id'] for r in rows)), 3)
        self.assertTrue(all('repeated_marker' in r['flags'] for r in rows[:2]))
        self.assertTrue(all(r['parser_id'] == 'fenced-paragraph' for r in rows))

    def test_rejects_missing_fence(self):
        with self.assertRaises(ValueError):
            passage_parser.parse(b'# Metadata only\n', 'x', 'Title', 'url')

    def test_lookup_keeps_duplicate_occurrences(self):
        raw = b'```text\nfirst || 4 ||\n\nsecond || 4 ||\n```\n'
        rows = passage_parser.parse(raw, 'example', 'Book', 'url')
        result = passage_parser.lookup_marker(rows, 'example', '4')
        self.assertEqual(result['status'], 'ambiguous')
        self.assertEqual(len(result['matches']), 2)
        self.assertEqual(passage_parser.lookup_marker(rows, 'example', '9')['status'], 'not_found')

    def test_rejects_multiple_fences_instead_of_silent_loss(self):
        raw = b'```text\nfirst\n```\n\n```text\nsecond\n```\n'
        with self.assertRaises(ValueError):
            passage_parser.parse(raw, 'example', 'Book', 'url')

if __name__ == '__main__': unittest.main()
