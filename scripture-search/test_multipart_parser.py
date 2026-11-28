import hashlib
import unittest
import passage_parser


def volume(ident, verse):
    return ('```text\n' + '#'*25 + '\nMUKTABODHA INDOLOGICAL RESEARCH INSTITUTE\nCatalog number : '+ident+'\n'+'#'*25+'\n\n'+verse+'\n```\n').encode()


class MultipartTest(unittest.TestCase):
    def test_parts_preserve_both_source_urls_and_exact_combined_offsets(self):
        first=volume('M00001a','first || 1 ||'); second=volume('M00001b','second || 2 ||')
        raw=b'# book\n'+first+b'\n# part two\n'+second
        positions=[raw.index(first),raw.index(second)]
        parts=[{'source_id':'muktabodha-'+ident.lower(),'source_url':'https://example.org/'+ident,'sha256':hashlib.sha256(data).hexdigest(),'combined_byte_start':pos,'combined_byte_end':pos+len(data)} for ident,data,pos in zip(['M00001a','M00001b'],[first,second],positions)]
        rows=passage_parser.parse_multipart_muktabodha(raw,'book','title',parts)
        self.assertEqual([x['source_url'] for x in rows],['https://example.org/M00001a','https://example.org/M00001b'])
        self.assertTrue(all(raw[x['byte_start']:x['byte_end']].decode()==x['text'] for x in rows))
        self.assertEqual(len({x['chunk_id'] for x in rows}),2)
        parts[1]['sha256']='wrong'
        with self.assertRaises(ValueError): passage_parser.parse_multipart_muktabodha(raw,'book','title',parts)
