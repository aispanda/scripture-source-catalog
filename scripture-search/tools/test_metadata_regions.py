import unittest
from metadata_regions import classify_metadata, overlaps_metadata

class MetadataRegionsTest(unittest.TestCase):
    def test_delimited_publisher_header_and_source_body(self):
        raw = 'ā\n# Header\nPublisher data\n# Text\nactual text'.encode()
        result = classify_metadata(raw)
        self.assertEqual(len(result['metadata_spans']), 1)
        s = result['metadata_spans'][0]
        self.assertEqual(raw[s['start']:s['end']].decode(), '# Header\nPublisher data\n')
        self.assertTrue(overlaps_metadata(s['start'], s['end'], result))
        self.assertFalse(overlaps_metadata(s['end'], len(raw), result))

    def test_unknown_format_not_claimed_as_body(self):
        self.assertEqual(classify_metadata(b'loose prose')['status'], 'no_recognized_header')

    def test_unclosed_header_is_not_auto_classified(self):
        self.assertEqual(classify_metadata(b'# Header\nPublisher details')['status'], 'incomplete_header')

    def test_muktabodha_hash_header(self):
        raw = ('###'*15+'\nPublisher\n'+'###'*15+'\nText').encode()
        result = classify_metadata(raw)
        self.assertEqual(result['status'], 'classified_explicit')
        self.assertTrue(overlaps_metadata(3, 10, result))
        self.assertFalse(overlaps_metadata(len(raw)-4, len(raw), result))
