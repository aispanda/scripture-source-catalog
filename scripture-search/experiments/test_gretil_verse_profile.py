import unittest

from gretil_verse_profile import parse


class VerseProfileTest(unittest.TestCase):
    def test_multiline_verse_and_source_offsets(self):
        raw = '# Text\ncanto i\n\nśloka first /\nśloka second // saund_1.1 //\n\nunknown prose\n'.encode()
        spans = parse(raw, {'siglum': 'saund'})
        verses = [s for s in spans if s['role'] == 'verse']
        self.assertEqual(len(verses), 1)
        self.assertEqual(verses[0]['text'], 'śloka first /\nśloka second // saund_1.1 //')
        self.assertTrue(any(s['role'] == 'unclassified' for s in spans))
        self.assertTrue(all(raw[s['start']:s['end']].decode() == s['text'] for s in spans))

    def test_inline_reference_not_a_verse(self):
        raw = b'# Text\nA prose quote // saund_1.1 // continues.\n'
        self.assertFalse(any(s['role'] == 'verse' for s in parse(raw, {'siglum': 'saund'})))

    def test_adjacent_verses_split_at_each_complete_reference(self):
        raw = b'# Text\nfirst /\nend // saund_1.1 //\nnext /\nend // saund_1.2 //\n'
        verses = [s for s in parse(raw, {'siglum': 'saund'}) if s['role'] == 'verse']
        self.assertEqual([s['reference'] for s in verses], ['saund_1.1', 'saund_1.2'])
        self.assertEqual(verses[1]['text'], 'next /\nend // saund_1.2 //')

    def test_explicit_single_closer_option_keeps_marker_visible(self):
        raw = b'# Text\nfirst // saund_2.33 / \nnext // saund_2.34 //\n'
        spans = parse(raw, {'siglum': 'saund', 'allow_single_closing_slash': True})
        verses = [s for s in spans if s['role'] == 'verse']
        self.assertEqual([s['reference'] for s in verses], ['saund_2.33', 'saund_2.34'])
        self.assertTrue(verses[0]['irregular_marker'])
