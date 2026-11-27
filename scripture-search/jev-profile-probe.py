"""Bounded Jev classification experiment; never selects or runs a parser."""
import argparse
import json
import urllib.request
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('markdown', type=Path)
parser.add_argument('--env-file', type=Path, required=True)
args = parser.parse_args()
key = next(line.partition('=')[2].strip().strip('"\'') for line in args.env_file.read_text().splitlines() if line.startswith('TYPESAFE_API_KEY='))
text = args.markdown.read_text(encoding='utf-8')
state = {'filename': args.markdown.name, 'opening': text[:3000], 'middle': text[len(text)//2:len(text)//2+2000]}
payload = {'model': 'jev-1.14.0', 'state': state, 'questions': {
    'text_form': {'type': 'choice', 'instructions': 'Which structure is best supported by the excerpts? Choose unknown if uncertain.', 'criteria': {
        'numbered_scripture': 'Primarily numbered verses with no clear interleaved commentary.',
        'root_and_commentary': 'Root verses or sutras interleaved with explanatory commentary.',
        'tamil_lines': 'Tamil poem or prose with line numbering or line-like structure.',
        'unknown': 'Evidence is insufficient or does not fit another choice.'}}}}
req = urllib.request.Request('https://api.typesafe.ai/v1/systemone', data=json.dumps(payload,ensure_ascii=False).encode(), headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
with urllib.request.urlopen(req,timeout=60) as response:
    result=json.load(response)
print(json.dumps({'file':args.markdown.name,'model':result.get('model'),'answers':result.get('answers'),'usage':result.get('usage')},ensure_ascii=False))
