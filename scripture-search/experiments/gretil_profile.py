"""Experimental source-specific profile; spans refer to original UTF-8 bytes."""
import re


def parse(raw, config):
    raw.decode('utf-8')
    siglum = config['siglum'].encode('ascii')
    marker = re.compile(rb'^[^\r\n]+?//\s*(' + re.escape(siglum) + rb'_\d+,\d+\.\d+)\s*//[ \t]*$', re.I)
    heading = re.compile(rb'^adhy\xc4\x81ya\s+\d+\s*:\s*$', re.I)
    notes = re.compile(rb'^notes\s*:', re.I)
    lines = list(re.finditer(rb'[^\r\n]+(?:\r?\n|$)', raw))
    starts = [i for i, m in enumerate(lines) if m.group().strip() == b'# Text']
    if len(starts) != 1:
        raise ValueError('Expected exactly one # Text heading')
    spans = []
    in_notes = False
    for line in lines[starts[0] + 1:]:
        start, end = line.span()
        content = raw[start:end].rstrip(b'\r\n')
        end = start + len(content)
        if not content.strip():
            continue
        match = marker.fullmatch(content)
        if match:
            role, reference, in_notes = 'root_sutra', match.group(1).decode('ascii').lower(), False
        elif heading.fullmatch(content):
            role, reference, in_notes = 'heading', None, False
        elif notes.match(content):
            role, reference, in_notes = 'notes', None, True
        elif in_notes:
            role, reference = 'notes', None
        else:
            role, reference = 'unclassified', None
        spans.append({'role': role, 'reference': reference, 'start': start, 'end': end,
                      'text': raw[start:end].decode('utf-8')})
    return spans
