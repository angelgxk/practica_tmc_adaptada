"""Clasificación de elementos en N, Z, Q y símbolos."""

def clasificar(A):
    naturales = set()
    enteros = set()
    racionales = set()
    simbolos = set()

    for x in A:
        if isinstance(x, int):
            if x >= 0:
                naturales.add(x)
            enteros.add(x)
        elif isinstance(x, float):
            racionales.add(x)
        else:
            simbolos.add(x)

    return {
        "N": naturales,
        "Z": enteros,
        "Q": racionales,
        "simbolos": simbolos
    }
