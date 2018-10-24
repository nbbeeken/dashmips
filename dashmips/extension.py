"""Vscode extension helpers."""
from typing import Dict

from dashmips.instructions import Instructions

snippet_part = '${{{count}:{filler}}}'

SNIPPET_REPLACEMENTS = {
    'register': '\\$reg',
    'label': 'label',
    'number': 'number',
    'instr_gap': ' ',
    'args_gap': ', ',
}

REG_ARGS = ['t0', 't1', 't2']


def generate_snippets() -> Dict[str, Dict[str, str]]:
    """Generate Instruction snippets."""
    snippets = {}
    names = sorted(Instructions.keys())
    for name in names:
        ins = Instructions[name]
        body = build_body(ins.name, ins.pattern, ins.label)
        desc = ins.fn.__doc__.split('\n')[0] if ins.fn.__doc__ else ''

        snippets[name] = {
            'prefix': name,
            'body': body,
            'description': desc,
            'scope': 'mips',
        }
    return snippets


def build_body(name: str, pattern: str, label: bool) -> str:
    """Create snippet body.

    :param name: Instruction name
    :param pattern: Instruction regex pattern
    """
    snip: str = f'{name:7s}' + pattern.format(**SNIPPET_REPLACEMENTS)
    snip = snip.replace('(', '')
    snip = snip.replace(')', '')
    snip = snip.replace('number?\\\\$reg\\', 'number(\\$reg)')
    replace_ct = 1

    reg_ct = snip.count('reg')
    for i in range(0, reg_ct):
        f = f'${{{replace_ct}:{REG_ARGS[i]}}}'
        snip = snip.replace('reg', f, 1)
        replace_ct += 1

    if label:
        snip = snip.replace('label', f'${{{replace_ct}:label}}')
        replace_ct += 1
    else:
        snip = snip.replace('number', f'${{{replace_ct}:100}}')
        replace_ct += 1

    return snip


def instruction_name_regex() -> str:
    """Generate big or capture regex for all instruction names."""
    names = sorted(Instructions.keys())
    return f"\\\\b({'|'.join(names)})\\\\b"
