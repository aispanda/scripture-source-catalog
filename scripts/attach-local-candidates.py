#!/usr/bin/env python3
"""Attach verified local file pointers to a new catalogue candidate, not the source."""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('candidate', type=Path)
    ap.add_argument('batch_report', type=Path)
    ap.add_argument('output', type=Path)
    args = ap.parse_args()
    if args.output.exists() or args.output.resolve() == args.candidate.resolve():
        raise SystemExit('Output must be a new file')
    catalogue = json.loads(args.candidate.read_text())
    batch = json.loads(args.batch_report.read_text())
    known = {row['id'] for row in catalogue['catalog_items']}
    assets = []
    for row in batch['results']:
        if row['catalogue_id'] not in known:
            raise ValueError('Unmatched catalogue item: ' + row['catalogue_id'])
        rel = Path(row['markdown_path'])
        if rel.is_absolute() or '..' in rel.parts or rel.suffix != '.md':
            raise ValueError('Invalid corpus path: ' + str(rel))
        path = args.batch_report.parent / rel
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != row['markdown_sha256']:
            raise ValueError('Markdown hash mismatch: ' + str(rel))
        assets.append({'catalog_item_id': row['catalogue_id'],
                       'path_ref': {'root': 'SPIRITUALITY_WORKSPACE',
                                    'rel': 'scripture-ingestion/pilot/' + rel.as_posix()},
                       'markdown_sha256': actual, 'source_file_sha256': row['source_file_sha256'],
                       'cloud_uri': None, 'status': 'draft_fidelity_and_rights_pending',
                       'reconciliation': 'check_existing_asset' if row['provider_item_id'] in ('M00271', 'M00347') else 'pending'})
    catalogue['local_corpus_candidates'] = assets
    args.output.write_text(json.dumps(catalogue, ensure_ascii=False, indent=2) + '\n')
    print(f'Wrote {len(assets)} draft pointers with verified file hashes; cloud URIs unset.')


if __name__ == '__main__':
    main()
