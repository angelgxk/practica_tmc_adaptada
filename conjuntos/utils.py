"""Conversión de entrada de texto a conjuntos."""

import re

def parse_set(text):
    result = set()

    for raw in text.split(","):
        item = raw.strip()
        if not item:
            continue

        if re.fullmatch(r"[+-]?\d+", item):
            value = int(item)
        elif re.fullmatch(r"[+-]?(?:\d+\.\d*|\d*\.\d+)", item):
            value = float(item)
        else:
            value = item

        result.add(value)

    return result


def format_value(x):
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    if isinstance(x, str):
        return f'"{x}"'
    return str(x)


def format_set(s):
    if not s:
        return "∅"

    values = sorted(
        s,
        key=lambda x: (0, x) if isinstance(x, (int, float)) else (1, str(x))
    )
    return "{ " + ", ".join(format_value(x) for x in values) + " }"
