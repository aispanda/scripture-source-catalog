"""Experimental source-marker inventory; no claim of semantic boundaries."""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

MARKER = re.compile(r'(?P<open>//|\|\|)[ \t]*(?P<prefix>[A-Za-z]+)_(?P<path>[0-9]+(?:[.,][0-9]+)+)[ \t]*(?P=open)')
BARE = re.compile(r'(?:\|\|[ \t]*(?P<ascii>[0-9]+)[ \t]*\|\||॥[ \t]*(?P<dev>[०-९0-9]+)[ \t]*॥)')
LINE_COUNTER = re.compile(r'\.\.\.[ \t]*(?P<num>[0-9]+)[ \t]*(?=\r?$)', re.MULTILINE)
UNCLOSED = re.compile(r'\|\|[ \t]*(?P<prefix>[A-Za-z]+)_(?P<path>[0-9]+(?:[.,][0-9]+)+)[ \t]*(?=\r?$)', re.MULTILINE)
SC_ID = re.compile(r'^(?P<prefix>[a-z]+[0-9]+):(?P<path>[0-9]+(?:\.[0-9]+)+)(?=\t)', re.MULTILINE)
GRETIL_SINGLE = re.compile(r'//[ \t]*(?P<prefix>[^\W\d_]+)_(?P<path>[0-9]+)(?![0-9.,]|[ \t]*//)', re.UNICODE)
TAMIL_NUMBER = re.compile(r'^[ \t]*(?P<num>[0-9]+)\.\.(?!\.)', re.MULTILINE)
TITUS_LABEL = re.compile(r'^(?P<label>Paragraph|Verse|Sentence):[ \t]*(?P<num>[0-9]+)(?![0-9])', re.MULTILINE)


def extract_references(raw, source_type=None):
    text = raw.decode('utf-8')
    counts = Counter()
    result = []
    last_char = last_byte = 0
    matches = [(m, 'prefixed_reference_candidate') for m in MARKER.finditer(text)]
    matches += [(m, 'number_marker_candidate') for m in BARE.finditer(text)]
    if source_type == 'project-madurai':
        matches += [(m, 'line_counter_candidate') for m in LINE_COUNTER.finditer(text)]
        matches += [(m, 'number_marker_candidate') for m in TAMIL_NUMBER.finditer(text)]
    if source_type == 'gretil':
        matches += [(m, 'unclosed_prefixed_reference_candidate') for m in UNCLOSED.finditer(text)]
        matches += [(m, 'unclosed_prefixed_reference_candidate') for m in GRETIL_SINGLE.finditer(text)]
    if source_type == 'suttacentral':
        matches += [(m, 'line_identifier_candidate') for m in SC_ID.finditer(text)]
    if source_type == 'titus':
        matches += [(m, 'named_unit_candidate') for m in TITUS_LABEL.finditer(text)]
    for match, kind in sorted(matches, key=lambda item: item[0].start()):
        start = (last_byte + len(text[last_char:match.start()].encode('utf-8'))
                 if match.start() >= last_char else len(text[:match.start()].encode('utf-8')))
        end = start + len(match.group().encode('utf-8'))
        last_char, last_byte = match.end(), end
        groups = match.groupdict()
        prefix = groups.get('prefix')
        path = groups.get('path') or groups.get('ascii') or groups.get('dev') or groups.get('num')
        key = prefix, path, kind
        counts[key] += 1
        result.append({'raw_marker': match.group(), 'prefix': prefix, 'marker_kind': kind,
                       'source_label': groups.get('label'),
                       'raw_path': path,
                       'levels': [{'label': f'level_{i}', 'value': value}
                                  for i, value in enumerate(re.split(r'[.,]', path), 1)],
                       'label_status': 'unverified', 'occurrence': counts[key],
                       'byte_start': start, 'byte_end': end})
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('corpus', type=Path)
    p.add_argument('output', type=Path)
    args = p.parse_args()
    counts = Counter()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('w', encoding='utf-8') as out:
        for path in sorted(args.corpus.rglob('*.md')):
            counts['files'] += 1
            try:
                raw = path.read_bytes()
                refs = extract_references(raw, path.relative_to(args.corpus).parts[0])
                counts['files_with_candidates'] += bool(refs)
                counts['candidate_markers'] += len(refs)
                row = {'file': str(path.relative_to(args.corpus)), 'sha256': hashlib.sha256(raw).hexdigest(),
                       'status': 'candidate_markers_only' if refs else 'no_supported_markers_detected',
                       'references': refs}
            except (OSError, UnicodeError) as exc:
                counts['errors'] += 1
                row = {'file': str(path.relative_to(args.corpus)), 'status': 'error', 'error': str(exc)}
            out.write(json.dumps(row, ensure_ascii=False) + '\n')
    print(json.dumps(counts))


if __name__ == '__main__':
    main()
