"""Vscode extension helpers."""
from dashmips.instructions import Instructions


def generate_snippets():
    """Generate Instruction snippets."""
    snippets = {}
    names = sorted(Instructions.keys())
    for name in names:
        ins = Instructions[name]
        snippets[name] = {
            'prefix': name,
            'body': f'{name} ',
            'description': ins.fn.__doc__ if ins.fn.__doc__ else '',
            'scope': 'mips',
        }
    return snippets
