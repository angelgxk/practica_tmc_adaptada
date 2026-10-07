"""Clausura de Kleene hasta una longitud máxima."""

from itertools import product

def kleene(alphabet, max_len=3):
    alphabet = list(dict.fromkeys(alphabet))
    result = [""]

    for length in range(1, max_len + 1):
        for word in product(alphabet, repeat=length):
            result.append("".join(word))

    return result


def gramatica_regular_derecha(alphabet):
    """
    Para Σ*, una gramática regular derecha equivalente es:
    S → ε | aS | bS | ...
    """
    productions = ["S → ε"]
    for symbol in alphabet:
        productions.append(f"S → {symbol}S")

    return "\n".join(productions)
