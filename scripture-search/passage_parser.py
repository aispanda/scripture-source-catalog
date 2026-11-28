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

def parse_muktabodha(raw, edition_id, title, source_url):
    """Experimental header-aware paragraphs; this is not a verse classifier."""
    raw.decode('utf-8')
    fences = list(FENCE.finditer(raw))
    if len(fences) != 1:
        raise ValueError('Expected one text fence')
    fence = fences[0]
    delimiters = list(re.finditer(rb'^#{20,}[ \t]*\r?$', raw[fence.start(1):fence.end(1)], re.M))
    if len(delimiters) != 2:
        raise ValueError('Missing or ambiguous publisher header delimiters')
    start = fence.start(1) + delimiters[0].start()
    end = fence.start(1) + delimiters[1].end()
    header = raw[start:end]
    catalog = re.search(rb'(?im)^Catalog number[ \t]*:[ \t]*([A-Z][0-9]+[a-z]?)\s*$', header)
    if b'MUKTABODHA INDOLOGICAL RESEARCH INSTITUTE' not in header or not catalog:
        raise ValueError('Unrecognized publisher header')
    if edition_id.rsplit('-', 1)[-1].lower() != catalog.group(1).decode('ascii').lower():
        raise ValueError('Publisher and requested catalogue IDs differ')
    rows = [row for row in parse(raw, edition_id, title, source_url) if row['byte_start'] >= end]
    if not rows:
        raise ValueError('No text after publisher header')
    parser_id, version = 'muktabodha-header-paragraph', '0.1.0'
    counts = collections.Counter(r['source_marker'] for r in rows if r['source_marker'])
    for seq, row in enumerate(rows, 1):
        marker = row['source_marker']
        row['chunk_id'] = f'{edition_id}:seq{seq:04d}'
        row['locator'] = f'source paragraph {seq}' + (f'; source marker {marker}' if marker else '')
        row['flags'] = ([] if marker else ['unnumbered_or_irregular']) + (['repeated_marker'] if marker and counts[marker] > 1 else [])
        row['parser_id'], row['parser_version'] = parser_id, version
        row['passage_set_version'] = hashlib.sha256(f"{row['source_version'][7:]}:{parser_id}:{version}".encode()).hexdigest()
    return rows

def parse_multipart_muktabodha(raw, edition_id, title, parts):
    """Parse each verified embedded source volume and retain exact combined offsets."""
    combined_hash = hashlib.sha256(raw).hexdigest()
    rows = []
    previous_end = 0
    for part in parts:
        start, end = part['combined_byte_start'], part['combined_byte_end']
        if not isinstance(start, int) or not isinstance(end, int) or start < previous_end or end <= start or end > len(raw):
            raise ValueError('Invalid or overlapping part range')
        source = raw[start:end]
        if hashlib.sha256(source).hexdigest() != part['sha256']:
            raise ValueError('Source part checksum mismatch')
        extracted = parse_muktabodha(source, part['source_id'], title, part['source_url'])
        for row in extracted:
            row['source_document_id'] = part['source_id']
            row['source_byte_start'], row['source_byte_end'] = row['byte_start'], row['byte_end']
            row['byte_start'] += start
            row['byte_end'] += start
            row['document_id'] = edition_id
            row['source_version'] = 'sha256:' + combined_hash
            row['chunk_id'] = f"{edition_id}:seq{len(rows)+1:06d}"
            row['parser_id'] = 'multipart-muktabodha-header-paragraph'
            row['passage_set_version'] = hashlib.sha256((combined_hash + ':multipart-muktabodha-header-paragraph:0.1.0').encode()).hexdigest()
            rows.append(row)
        previous_end = end
    if not rows:
        raise ValueError('No source parts')
    return rows

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('markdown', type=Path); p.add_argument('--edition-id', required=True)
    p.add_argument('--title', required=True); p.add_argument('--source-url', required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--profile', choices=['fenced-paragraph', 'muktabodha-header-paragraph'], default='fenced-paragraph')
    args = p.parse_args()
    parser = parse if args.profile == 'fenced-paragraph' else parse_muktabodha
    rows = parser(args.markdown.read_bytes(), args.edition_id, args.title, args.source_url)
    if args.output.exists(): raise FileExistsError('Refusing to overwrite output')
    args.output.write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows), encoding='utf-8')
    print(json.dumps({'passages': len(rows), 'parser_id': rows[0]['parser_id'] if rows else args.profile, 'parser_version': rows[0]['parser_version'] if rows else None}))

if __name__ == '__main__': main()
