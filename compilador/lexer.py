"""
Analizador léxico del DSL.

Reconoce:
- Palabras reservadas de las instrucciones.
- Números.
- Unidades de medida.
- Temperaturas.
- Identificadores/ingredientes.
"""

import re

TOKEN_REGEX = [
    ("AGREGAR",  r"\bAGREGAR\b"),
    ("PICAR",    r"\bPICAR\b"),
    ("CORTAR",   r"\bCORTAR\b"),
    ("MEZCLAR",  r"\bMEZCLAR\b"),
    ("CALENTAR", r"\bCALENTAR\b"),
    ("HORNEAR",  r"\bHORNEAR\b"),
    ("SERVIR",   r"\bSERVIR\b"),
    ("NUM",      r"\b\d+(?:[.,]\d+)?\b"),
    ("UNIDAD",   r"\b(?:mg|g|kg|ml|l|cda|cdta|taza|tazas|pieza|piezas)\b"),
    ("TEMP",     r"\b(?:\d+(?:[.,]\d+)?)\s*(?:°?C)\b"),
    ("IDENT",    r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9_-]*"),
]

MASTER = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_REGEX),
    re.IGNORECASE
)

def lex(line):
    tokens = []
    pos = 0

    while pos < len(line):
        if line[pos].isspace():
            pos += 1
            continue

        match = MASTER.match(line, pos)

        if not match:
            tokens.append({
                "type": "ERROR",
                "value": line[pos],
                "position": pos
            })
            pos += 1
            continue

        kind = match.lastgroup
        value = match.group()
        tokens.append({
            "type": kind.upper(),
            "value": value,
            "position": pos
        })
        pos = match.end()

    # Normaliza números decimales.
    for token in tokens:
        if token["type"] == "NUM":
            token["value"] = token["value"].replace(",", ".")

    return tokens


def token_table():
    return [
        ("AGREGAR", r"\bAGREGAR\b"),
        ("PICAR", r"\bPICAR\b"),
        ("CORTAR", r"\bCORTAR\b"),
        ("MEZCLAR", r"\bMEZCLAR\b"),
        ("CALENTAR", r"\bCALENTAR\b"),
        ("HORNEAR", r"\bHORNEAR\b"),
        ("SERVIR", r"\bSERVIR\b"),
        ("NUM", r"\d+(?:[.,]\d+)?"),
        ("UNIDAD", r"\b(mg|g|kg|ml|l|cda|cdta|taza|tazas|pieza|piezas)\b"),
        ("TEMP", r"\b\d+(?:[.,]\d+)?\s*(?:°?C)\b"),
        ("IDENT", r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9_-]*"),
    ]
