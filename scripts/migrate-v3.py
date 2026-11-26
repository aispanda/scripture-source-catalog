#!/usr/bin/env python3
"""Build a reviewable additive catalogue candidate; never modifies the input."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

FIELDS = ('traditions', 'collections', 'languages', 'language', 'script', 'genre',
          'author', 'commentator', 'editor', 'publisher', 'digital_publisher',
          'sampradaya', 'school', 'darshana')
ROOTS = ('works', 'editions', 'catalog_items', 'work_targets')


def migrate(data):
    if str(data.get('schema_version')) != '2.0':
        raise ValueError('Expected an unchanged schema 2.0 source')
    out = copy.deepcopy(data)
    assertions = []
    for root in ROOTS:
        for item in data.get(root, []):
            for field in FIELDS:
                value = item.get(field)
                if value is None or value == '' or value == []:
                    continue
                # Preserve values exactly, including provider uncertainty and lists.
                for position, label in enumerate(value if isinstance(value, list) else [value]):
                    if not isinstance(label, str) or not label.strip():
                        continue
                    identity = f'{root}:{item["id"]}:{field}:{position}'
                    assertions.append({
                        'id': 'fa-' + hashlib.sha256(identity.encode()).hexdigest()[:20],
                        'subject': {'type': root, 'id': item['id']},
                        'facet': field, 'source_label': label, 'normalized_value': None,
                        'method': 'existing_catalogue_field',
                        'evidence': {'kind': 'catalogue_field', 'field': field,
                                     'catalog_url': item.get('catalog_url')},
                        'status': 'proposed'})
    out['schema_version'] = '3.0'
    out['facet_assertions'] = assertions
    # JSON Views requires each configured column to resolve in at least one row.
    # Populate missing optional display fields with null on all rows; null is
    # unknown, not a source-backed classification.
    display_fields = ('sampradaya', 'school', 'darshana', 'author', 'publisher', 'digital_publisher')
    for root in ROOTS:
        for row in out.get(root, []):
            for field in display_fields:
                row.setdefault(field, None)
    out['migration_v3'] = {'status': 'candidate_review_pending',
                           'source_schema_version': '2.0',
                           'notes': 'Existing labels are copied, not independently verified. No normalization or model classification performed.'}
    for root, coverage in out.get('metadata_coverage', {}).items():
        if root not in ROOTS or not isinstance(coverage, dict):
            continue
        rows = out.get(root, [])
        coverage['total'] = len(rows)
        for field in coverage:
            if field != 'total':
                coverage[field] = sum(1 for row in rows if row.get(field) not in (None, '', []))
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('candidate', type=Path)
    args = parser.parse_args()
    if args.source.resolve() == args.candidate.resolve() or args.candidate.exists():
        raise SystemExit('Candidate must be a new file distinct from the source')
    raw = args.source.read_bytes()
    result = migrate(json.loads(raw))
    result['migration_v3']['source_sha256'] = hashlib.sha256(raw).hexdigest()
    args.candidate.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"Candidate: {args.candidate}; assertions: {len(result['facet_assertions'])}; source sha256: {result['migration_v3']['source_sha256']}")


if __name__ == '__main__':
    main()
