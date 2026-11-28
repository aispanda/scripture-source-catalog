"""Identify explicitly delimited publisher headers without altering source text."""
import argparse
import collections
import hashlib
import json
import re
from pathlib import Path

HEADER = re.compile(rb'^# Header[ \t]*\r?$', re.M)
BODY = re.compile(rb'^# Text[ \t]*\r?$', re.M)
HASH_DELIMITER = re.compile(rb'^#{20,}[ \t]*\r?$', re.M)


def classify_metadata(raw):
    spans = []
    incomplete = False
    for h in HEADER.finditer(raw):
        b = BODY.search(raw, h.end())
        next_h = HEADER.search(raw, h.end())
        if b and (not next_h or b.start() < next_h.start()):
            spans.append({'start':h.start(), 'end':b.start(), 'kind':'publisher_header', 'evidence':'explicit # Header / # Text delimiters'})
        else:
            incomplete = True
    delimiters = list(HASH_DELIMITER.finditer(raw))
    for i in range(0, len(delimiters)-1, 2):
        a, b = delimiters[i], delimiters[i+1]
        if not any(a.start() < s['end'] and b.end() > s['start'] for s in spans):
            spans.append({'start':a.start(), 'end':b.end(), 'kind':'publisher_header', 'evidence':'paired hash header delimiters'})
    if len(delimiters) % 2:
        incomplete = True
    status = 'incomplete_header' if incomplete else ('classified_explicit' if spans else 'no_recognized_header')
    return {'status':status, 'metadata_spans': sorted(spans, key=lambda s:s['start'])}


def overlaps_metadata(start, end, result):
    return any(start < span['end'] and end > span['start'] for span in result['metadata_spans'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--corpus', type=Path, required=True, help='Directory containing Markdown sources')
    parser.add_argument('--output', type=Path, required=True, help='New JSONL file for metadata spans')
    args = parser.parse_args()
    corpus, dest = args.corpus, args.output
    if not corpus.is_dir():
        parser.error('corpus must be an existing directory')
    if dest.exists():
        parser.error('output already exists; choose a new path')
    totals = collections.Counter()
    with dest.open('x', encoding='utf-8') as out:
        for path in sorted(corpus.rglob('*.md')):
            row={'file':str(path.relative_to(corpus))}
            try:
                raw=path.read_bytes()
                row.update(source_sha256=hashlib.sha256(raw).hexdigest(), **classify_metadata(raw))
            except OSError as exc:
                row.update(status='read_error', error=str(exc))
            totals[row['status']]+=1
            out.write(json.dumps(row,ensure_ascii=False)+'\n')
    print(json.dumps(totals))


if __name__ == '__main__': main()
