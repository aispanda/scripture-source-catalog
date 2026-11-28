import unittest

from gretil_profile import parse


class GretilProfileTest(unittest.TestCase):
    def test_preserves_boundaries_and_source_bytes(self):
        raw = ('# Text\nadhyāya 1:\nathāto dharmajijñāsā // ms_1,1.1 //\n'
               'Commentary with ms_1,1.1 in prose.\n\nnotes: *{1/1: note}*\n'
               'codanā // ms_1,1.2 //\n').encode()
        spans = parse(raw, {'siglum': 'ms'})
        sutras = [s for s in spans if s['role'] == 'root_sutra']
        self.assertEqual([s['reference'] for s in sutras], ['ms_1,1.1', 'ms_1,1.2'])
        self.assertTrue(any(s['role'] == 'notes' for s in spans))
        self.assertTrue(any(s['role'] == 'heading' for s in spans))
        self.assertTrue(any(s['role'] == 'unclassified' for s in spans))
        self.assertTrue(all(raw[s['start']:s['end']].decode() == s['text'] for s in spans))

    def test_marker_quoted_within_prose_is_not_sutra(self):
        raw = b'# Text\nA citation // ms_1,1.1 // inside commentary.\n'
        self.assertFalse(any(s['role'] == 'root_sutra' for s in parse(raw, {'siglum': 'ms'})))


if __name__ == '__main__':
    unittest.main()
