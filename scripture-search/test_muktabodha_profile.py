import unittest
import passage_parser


class MuktabodhaProfileTest(unittest.TestCase):
    def test_header_separated_and_source_spans_retained(self):
        raw = ('# Title\n\n```text\n' + '#'*25 + '\nMUKTABODHA INDOLOGICAL RESEARCH INSTITUTE\nCatalog number : M00271\n' + '#'*25 + '\n\nॐ नमः |\n\nअग्निः || १ ||\n\nपुनः || १ ||\n```\n').encode()
        rows = passage_parser.parse_muktabodha(raw, 'm00271', 'Title', 'https://example.org')
        self.assertEqual(len(rows), 3)
        self.assertTrue(all(raw[r['byte_start']:r['byte_end']].decode() == r['text'] for r in rows))
        self.assertEqual([r['source_marker'] for r in rows], [None, '१', '१'])
        self.assertTrue(all('repeated_marker' in r['flags'] for r in rows[1:]))
        self.assertNotIn('MUKTABODHA', ''.join(r['text'] for r in rows))

    def test_missing_or_ambiguous_header_fails(self):
        with self.assertRaises(ValueError):
            passage_parser.parse_muktabodha(b'```text\nNo verified header\n```', 'x', 'x', 'x')

    def test_mismatched_catalogue_id_is_rejected(self):
        raw = ('```text\n' + '#'*25 + '\nMUKTABODHA INDOLOGICAL RESEARCH INSTITUTE\nCatalog number : M00271\n' + '#'*25 + '\n\nverse || 1 ||\n```\n').encode()
        with self.assertRaises(ValueError):
            passage_parser.parse_muktabodha(raw, 'muktabodha-m00347', 'x', 'x')

if __name__ == '__main__':
    unittest.main()
