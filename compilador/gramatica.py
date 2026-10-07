"""
Gramática formal del DSL de recetario técnico.

G = (VN, VT, P, S)

No terminales:
VN = {S, I, A, C, M, T, V, ING, NUM, UNIDAD, TEMP}

Terminales:
VT = {AGREGAR, PICAR, CORTAR, MEZCLAR, CALENTAR, HORNEAR, SERVIR,
      NUM, UNIDAD, TEMP, IDENT}

La gramática se implementa mediante reglas equivalentes en parser.py.
"""

VN = {
    "S", "I", "A", "C", "M", "T", "V",
    "ING", "NUM", "UNIDAD", "TEMP"
}

VT = {
    "AGREGAR", "PICAR", "CORTAR", "MEZCLAR",
    "CALENTAR", "HORNEAR", "SERVIR",
    "NUM", "UNIDAD", "TEMP", "IDENT"
}

PRODUCCIONES = [
    "S → I S | ε",
    "I → A | C | M | T | V",
    "A → AGREGAR NUM UNIDAD ING",
    "C → PICAR ING | CORTAR ING",
    "M → MEZCLAR ING ING",
    "T → CALENTAR TEMP | HORNEAR TEMP",
    "V → SERVIR",
]

SIMBOLO_INICIAL = "S"


def texto_gramatica():
    return (
        "G = (VN, VT, P, S)\n\n"
        f"VN = {{{', '.join(sorted(VN))}}}\n\n"
        f"VT = {{{', '.join(sorted(VT))}}}\n\n"
        "P:\n" + "\n".join(PRODUCCIONES) +
        f"\n\nS = {SIMBOLO_INICIAL}"
    )
