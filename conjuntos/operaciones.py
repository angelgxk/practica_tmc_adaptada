"""Operaciones algebraicas de conjuntos."""

def operaciones(A, B):
    return {
        "cardinalidad_A": len(A),
        "cardinalidad_B": len(B),
        "union": A | B,
        "interseccion": A & B,
        "A_menos_B": A - B,
        "B_menos_A": B - A,
        "diferencia_simetrica": A ^ B,
        "A_subconjunto_B": A <= B,
        "B_subconjunto_A": B <= A,
    }
