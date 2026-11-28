import unittest
from generic_references import extract_references


class GenericReferencesTest(unittest.TestCase):
    def test_reference_keeps_raw_marker_and_generic_levels(self):
        raw = 'ā // rcint_1.2 // and // rcint_1.1.2 //'.encode()
        refs = extract_references(raw)
        self.assertEqual([r['levels'] for r in refs], [[{'label': 'level_1', 'value': '1'}, {'label': 'level_2', 'value': '2'}], [{'label': 'level_1', 'value': '1'}, {'label': 'level_2', 'value': '1'}, {'label': 'level_3', 'value': '2'}]])
        for r in refs:
            self.assertEqual(raw[r['byte_start']:r['byte_end']].decode(), r['raw_marker'])
            self.assertEqual(r['label_status'], 'unverified')

    def test_does_not_treat_prose_numbers_as_references(self):
        self.assertEqual(extract_references(b'Version 1.2 and date 2020.01.02'), [])

    def test_preserves_duplicate_references(self):
        refs = extract_references(b'// ms_1,1.2 //\n// ms_1,1.2 //')
        self.assertEqual([r['occurrence'] for r in refs], [1, 2])

    def test_bare_number_markers_preserve_digits_and_source_bytes(self):
        raw = 'ś || 76 || next ॥ २ ॥'.encode()
        refs = extract_references(raw)
        self.assertEqual([r['raw_path'] for r in refs], ['76', '२'])
        for ref in refs:
            self.assertEqual(raw[ref['byte_start']:ref['byte_end']].decode(), ref['raw_marker'])

    def test_madurai_line_counter_not_general_ellipsis(self):
        refs = extract_references('...10\nprose ... 20\n'.encode(), source_type='project-madurai')
        self.assertEqual([r['raw_path'] for r in refs], ['10', '20'])
        self.assertTrue(all(r['marker_kind'] == 'line_counter_candidate' for r in refs))
        self.assertEqual(extract_references(b'...10'), [])

    def test_gretil_unclosed_marker_is_line_end_candidate(self):
        raw = b'text || PS_1,1.1\ntext || PS_1,1.2 ||\n'
        refs = extract_references(raw, source_type='gretil')
        self.assertEqual([r['raw_path'] for r in refs], ['1,1.1', '1,1.2'])
        self.assertEqual(refs[0]['marker_kind'], 'unclosed_prefixed_reference_candidate')
        self.assertTrue(all(raw[r['byte_start']:r['byte_end']].decode() == r['raw_marker'] for r in refs))

    def test_suttacentral_line_id_does_not_match_web_urls(self):
        raw = b'https://example.com/1.2\nmn1:0.1\tText\nmn1:0.2\tMore\n'
        refs = extract_references(raw, source_type='suttacentral')
        self.assertEqual([r['raw_marker'] for r in refs], ['mn1:0.1', 'mn1:0.2'])
        self.assertEqual(refs[0]['marker_kind'], 'line_identifier_candidate')

    def test_source_specific_markers_without_closing_bars(self):
        refs = extract_references('text // tśpk_29\ntext // tśpk_30\n'.encode(), source_type='gretil')
        self.assertEqual([r['raw_path'] for r in refs], ['29', '30'])
        self.assertEqual([r['prefix'] for r in refs], ['tśpk', 'tśpk'])

    def test_madurai_indented_double_dot_number(self):
        refs = extract_references(' 521..\n 522..text\n'.encode(), source_type='project-madurai')
        self.assertEqual([r['raw_path'] for r in refs], ['521', '522'])

    def test_titus_named_units(self):
        refs = extract_references('Paragraph: 20\nVerse: 1\nSentence: 3 text\n'.encode(), source_type='titus')
        self.assertEqual([r['raw_path'] for r in refs], ['20', '1', '3'])
        self.assertEqual([r['source_label'] for r in refs], ['Paragraph', 'Verse', 'Sentence'])

    def test_overlapping_candidates_keep_exact_utf8_positions(self):
        raw = 'ā || PS_1.2\n|| 13 ||'.encode()
        refs = extract_references(raw, source_type='gretil')
        self.assertGreaterEqual(len(refs), 2)
        for ref in refs:
            self.assertEqual(raw[ref['byte_start']:ref['byte_end']].decode(), ref['raw_marker'])


if __name__ == '__main__':
    unittest.main()
