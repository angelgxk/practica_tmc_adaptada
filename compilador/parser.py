"""
Analizador sintáctico.
Valida cada línea independientemente para que un error no detenga
el escaneo global.
"""

from .lexer import lex


class Parser:
    def parse_line(self, line):
        tokens = lex(line)

        if not tokens:
            return False, None, "Línea vacía."

        if any(t["type"] == "ERROR" for t in tokens):
            bad = next(t["value"] for t in tokens if t["type"] == "ERROR")
            return False, tokens, f"Símbolo no reconocido: '{bad}'."

        types = [t["type"] for t in tokens]

        if types[0] == "AGREGAR":
            # AGREGAR NUM UNIDAD IDENT+
            if len(tokens) < 4:
                return False, tokens, "AGREGAR requiere cantidad, unidad e ingrediente."
            if types[1] != "NUM":
                return False, tokens, "Después de AGREGAR debe aparecer una cantidad numérica."
            if types[2] != "UNIDAD":
                return False, tokens, "Después de la cantidad debe aparecer una unidad."
            if any(t != "IDENT" for t in types[3:]):
                return False, tokens, "El ingrediente contiene un token no válido."

            return True, tokens, {
                "tipo": "AGREGAR",
                "cantidad": tokens[1]["value"],
                "unidad": tokens[2]["value"],
                "ingrediente": " ".join(t["value"] for t in tokens[3:])
            }

        if types[0] in ("PICAR", "CORTAR"):
            if len(tokens) < 2:
                return False, tokens, f"{types[0]} requiere un ingrediente."
            if any(t != "IDENT" for t in types[1:]):
                return False, tokens, "El ingrediente contiene un token no válido."

            return True, tokens, {
                "tipo": types[0],
                "ingrediente": " ".join(t["value"] for t in tokens[1:])
            }

        if types[0] == "MEZCLAR":
            if len(tokens) < 3:
                return False, tokens, "MEZCLAR requiere al menos dos elementos."
            if any(t != "IDENT" for t in types[1:]):
                return False, tokens, "Los elementos de MEZCLAR deben ser identificadores."

            return True, tokens, {
                "tipo": "MEZCLAR",
                "elementos": [t["value"] for t in tokens[1:]]
            }

        if types[0] in ("CALENTAR", "HORNEAR"):
            # La especificación acepta temperatura + unidad de temperatura.
            # Ejemplo: CALENTAR 180 C
            if len(tokens) != 2:
                return False, tokens, f"{types[0]} requiere una temperatura, por ejemplo {types[0]} 180 C."
            if tokens[1]["type"] != "TEMP":
                # Permite la forma separada NUM C si el lexer produjo NUM + IDENT.
                if len(tokens) == 3 and tokens[1]["type"] == "NUM" and tokens[2]["type"] == "IDENT" and tokens[2]["value"].upper() == "C":
                    temp = tokens[1]["value"]
                else:
                    return False, tokens, f"{types[0]} requiere una temperatura válida."
            else:
                temp = tokens[1]["value"].replace(" ", "")

            return True, tokens, {
                "tipo": types[0],
                "temperatura": temp
            }

        if types[0] == "SERVIR":
            if len(tokens) != 1:
                return False, tokens, "SERVIR no acepta parámetros."
            return True, tokens, {"tipo": "SERVIR"}

        return False, tokens, f"Instrucción '{tokens[0]['value']}' no pertenece al lenguaje."

    def parse_program(self, source):
        validas = []
        errores = []

        for numero, line in enumerate(source.splitlines(), start=1):
            if not line.strip():
                continue

            ok, tokens, data = self.parse_line(line.strip())

            if ok:
                validas.append((numero, line.strip(), data))
            else:
                errores.append((numero, data))

        # La práctica usa SERVIR como término.
        nonempty = [x.strip() for x in source.splitlines() if x.strip()]
        if nonempty and not nonempty[-1].upper().startswith("SERVIR"):
            errores.append(
                (len(source.splitlines()),
                 "La receta debe terminar con SERVIR.")
            )

        return validas, errores
