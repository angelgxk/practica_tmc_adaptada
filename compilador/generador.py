"""
Generador de código para una máquina abstracta.
Cada sentencia válida se traduce a MOV/CALL y SERVIR produce HALT.
"""

def generar_sentencia(data):
    tipo = data["tipo"]

    if tipo == "AGREGAR":
        return [
            f"MOV R1, {data['cantidad']}",
            f"MOV R2, {data['unidad']}",
            f"CALL sys.agregar ; {data['ingrediente']}"
        ]

    if tipo == "PICAR":
        return [
            f"MOV R1, {data['ingrediente']}",
            "CALL sys.picar"
        ]

    if tipo == "CORTAR":
        return [
            f"MOV R1, {data['ingrediente']}",
            "CALL sys.cortar"
        ]

    if tipo == "MEZCLAR":
        return [
            f"MOV R1, {', '.join(data['elementos'])}",
            "CALL sys.mezclar"
        ]

    if tipo == "CALENTAR":
        return [
            f"MOV R1, {data['temperatura']}",
            "CALL sys.calentar"
        ]

    if tipo == "HORNEAR":
        return [
            f"MOV R1, {data['temperatura']}",
            "CALL sys.hornear"
        ]

    if tipo == "SERVIR":
        return [
            "CALL sys.servir",
            "HALT"
        ]

    return []


def generar_programa(validas):
    output = [
        "; ===========================================",
        "; CÓDIGO GENERADO - RECETARIO TÉCNICO",
        "; ===========================================",
        ""
    ]

    for linea, original, data in validas:
        output.append(f"; Línea {linea}: {original}")
        output.extend(generar_sentencia(data))
        output.append("")

    return "\n".join(output)
