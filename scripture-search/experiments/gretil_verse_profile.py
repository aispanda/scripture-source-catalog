"""Experimental paragraph-based verse profile with original UTF-8 offsets."""
import re


def parse(raw, config):
    raw.decode('utf-8')
    siglum = re.escape(config['siglum'].encode('ascii'))
    heading = list(re.finditer(rb'(?m)^# Text[ \t]*\r?$', raw))
    if len(heading) != 1:
        raise ValueError('Expected exactly one # Text heading')
    closer = rb'/{1,2}' if config.get('allow_single_closing_slash') else rb'//'
    ref = re.compile(rb'//\s*(' + siglum + rb'_\d+\.\d+)\s*(' + closer + rb')[ \t]*$', re.I | re.M)
    paragraph = re.compile(rb'(?m)\S[^\r\n]*(?:\r?\n(?![ \t]*\r?$)[^\r\n]+)*')
    spans = []
    for m in paragraph.finditer(raw, heading[0].end()):
        start, end = m.span()
        cursor = start
        for match in ref.finditer(raw, start, end):
            stop = match.end()
            text = raw[cursor:stop]
            spans.append({'role': 'verse', 'reference': match.group(1).decode('ascii').lower(),
                          'irregular_marker': len(match.group(2)) == 1,
                          'start': cursor, 'end': stop, 'text': text.decode('utf-8')})
            cursor = stop
            while cursor < end and raw[cursor] in b'\r\n':
                cursor += 1
        if cursor < end:
            spans.append({'role': 'unclassified', 'reference': None, 'start': cursor, 'end': end,
                          'text': raw[cursor:end].decode('utf-8')})
    return spans
