"""Fachada del compilador: conecta parser y generador."""

from .parser import Parser
from .generador import generar_programa

class Compiler:
    def __init__(self):
        self.parser = Parser()

    def compile(self, source):
        validas, errores = self.parser.parse_program(source)
        assembly = generar_programa(validas)
        return validas, errores, assembly
