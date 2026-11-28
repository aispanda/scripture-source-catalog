"""Experimental per-book configuration bound to a verified local input hash."""
import argparse
import hashlib
import json
import re
from pathlib import Path

import gretil_profile
import gretil_verse_profile

PROFILES = {
    'numbered-sutra': ('0.1.0', gretil_profile.parse),
    'numbered-multiline-verse': ('0.1.0', gretil_verse_profile.parse),
}


def parse_record(record, raw):
    actual_hash = hashlib.sha256(raw).hexdigest()
    if record['source_sha256'] != actual_hash:
        raise ValueError('source hash differs from inventory; refresh evidence')
    profile = record['parser_profile']
    if profile not in PROFILES:
        raise ValueError('unknown parser profile: ' + profile)
    version, parser = PROFILES[profile]
    settings = record['parser_settings']
    if not isinstance(settings.get('siglum'), str) or not settings['siglum'].isascii() or not settings['siglum'].isalpha():
        raise ValueError('siglum must be ASCII letters')
    settings_hash = hashlib.sha256(json.dumps(settings, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    passages = parser(raw, settings)
    text = raw.decode('utf-8')
    markers = {'devanagari_double_danda': text.count('॥'), 'devanagari_single_danda': text.count('।'),
               'ascii_double_bar': len(re.findall(r'\|\|', text)),
               'ascii_single_bar': len(re.findall(r'(?<!\|)\|(?!\|)', text))}
    return {'book_id': record['id'], 'source_sha256': actual_hash, 'profile': profile,
            'profile_version': version, 'settings_sha256': settings_hash,
            'status': 'experimental', 'observed_markers': markers, 'passages': passages}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--inventory', required=True)
    p.add_argument('--book-id', required=True)
    p.add_argument('--project-root', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    inventory = json.loads(Path(args.inventory).read_text())
    records = [r for r in inventory['books'] if r['id'] == args.book_id]
    if len(records) != 1:
        raise ValueError('expected exactly one matching book')
    root = Path(args.project_root).resolve()
    source = (root / records[0]['local_markdown']).resolve()
    if not source.is_relative_to(root):
        raise ValueError('local Markdown must be inside the project root')
    result = parse_record(records[0], source.read_bytes())
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f"{result['book_id']}: {len(result['passages'])} experimental passages")


if __name__ == '__main__':
    main()
