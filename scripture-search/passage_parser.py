"""Extract source-identical paragraphs from Markdown text fences (pilot)."""
import argparse
import collections
import hashlib
import json
import re
from pathlib import Path

PARSER_ID = 'fenced-paragraph'
PARSER_VERSION = '0.1.0'
FENCE = re.compile(rb'^```(?:text)?[ \t]*\r?\n(.*?)^```[ \t]*$', re.M | re.S)
PARAGRAPH = re.compile(rb'\S[^\n]*(?:\n(?![ \t]*\n)[^\n]+)*')
MARKER = re.compile(r'\|\|\s*(\d+)\s*\|\|\s*$')

def parse(raw, edition_id, title, source_url):
    fences = list(FENCE.finditer(raw))
    if len(fences) != 1:
        raise ValueError('Expected exactly one supported text fence; another parser is needed')
    fence = fences[0]
    sha = hashlib.sha256(raw).hexdigest()
    passage_set_version = hashlib.sha256(f'{sha}:{PARSER_ID}:{PARSER_VERSION}'.encode()).hexdigest()
    rows = []
    for match in PARAGRAPH.finditer(raw, fence.start(1), fence.end(1)):
        start, end = match.span()
        text = raw[start:end].decode('utf-8')
        marker = MARKER.search(text)
        number = marker.group(1) if marker else None
        seq = len(rows) + 1
        rows.append({'document_id': edition_id, 'title': title, 'text': text,
                     'locator': f'source paragraph {seq}' + (f'; source marker {number}' if number else ''),
                     'source_url': source_url, 'source_version': 'sha256:' + sha,
                     'chunk_id': f'{edition_id}:seq{seq:04d}', 'byte_start': start, 'byte_end': end,
                     'source_marker': number, 'parser_id': PARSER_ID, 'parser_version': PARSER_VERSION,
                     'content_role': 'unclassified', 'passage_set_version': passage_set_version,
                     'flags': [] if number else ['unnumbered_or_irregular']})
    counts = collections.Counter(r['source_marker'] for r in rows if r['source_marker'])
    for row in rows:
        if row['source_marker'] and counts[row['source_marker']] > 1:
            row['flags'].append('repeated_marker')
    return rows

def lookup_marker(rows, edition_id, marker):
    matches = [r for r in rows if r['document_id'] == edition_id and r['source_marker'] == marker]
    return {'status': 'not_found' if not matches else 'unique' if len(matches) == 1 else 'ambiguous',
            'matches': matches}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('markdown', type=Path); p.add_argument('--edition-id', required=True)
    p.add_argument('--title', required=True); p.add_argument('--source-url', required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    rows = parse(args.markdown.read_bytes(), args.edition_id, args.title, args.source_url)
    if args.output.exists(): raise FileExistsError('Refusing to overwrite output')
    args.output.write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows), encoding='utf-8')
    print(json.dumps({'passages': len(rows), 'parser_id': PARSER_ID, 'parser_version': PARSER_VERSION}))

if __name__ == '__main__': main()
