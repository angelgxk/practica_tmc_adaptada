import tkinter as tk
from tkinter import ttk, messagebox

from compilador.compiler import Compiler
from compilador.gramatica import texto_gramatica
from compilador.lexer import token_table, lex
from conjuntos.utils import parse_set, format_set
from conjuntos.operaciones import operaciones
from conjuntos.clasificador import clasificar
from conjuntos.kleene import kleene, gramatica_regular_derecha


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Práctica Integral - Teoría Matemática de la Computación")
        self.geometry("1180x760")
        self.minsize(1000, 680)

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        self.compiler = Compiler()

        self.build_header()
        self.build_tabs()

    def build_header(self):
        frame = ttk.Frame(self, padding=(18, 14))
        frame.pack(fill="x")

        ttk.Label(
            frame,
            text="PRÁCTICA INTEGRAL DE LABORATORIO",
            font=("Segoe UI", 19, "bold")
        ).pack(anchor="w")

        ttk.Label(
            frame,
            text="Compilador de Recetario Técnico · Álgebra de Conjuntos · Lenguajes Regulares",
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(4, 0))

    def build_tabs(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        tab_a = ttk.Frame(notebook, padding=12)
        tab_b = ttk.Frame(notebook, padding=12)

        notebook.add(tab_a, text="  Módulo A · Compilador DSL  ")
        notebook.add(tab_b, text="  Módulo B · Conjuntos y Lenguajes  ")

        self.build_module_a(tab_a)
        self.build_module_b(tab_b)

    # ---------------- MÓDULO A ----------------

    def build_module_a(self, parent):
        top = ttk.Frame(parent)
        top.pack(fill="x")

        ttk.Label(
            top,
            text="Compilador de Recetario Técnico",
            font=("Segoe UI", 14, "bold")
        ).pack(side="left")

        ttk.Button(
            top, text="Ver gramática",
            command=self.show_grammar
        ).pack(side="right", padx=4)

        ttk.Button(
            top, text="Ver tokens / Regex",
            command=self.show_tokens
        ).pack(side="right", padx=4)

        body = ttk.Frame(parent)
        body.pack(fill="both", expand=True, pady=(10, 0))

        left = ttk.Frame(body)
        left.pack(side="left", fill="both", expand=True, padx=(0, 7))

        right = ttk.Frame(body)
        right.pack(side="right", fill="both", expand=True, padx=(7, 0))

        ttk.Label(left, text="Entrada: receta / código fuente",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w")

        self.recipe = tk.Text(left, font=("Consolas", 11), wrap="none")
        self.recipe.pack(fill="both", expand=True, pady=7)

        example = (
            "AGREGAR 500 g harina\n"
            "AGREGAR 250 ml agua\n"
            "MEZCLAR harina agua\n"
            "PICAR cebolla\n"
            "CORTAR tomate\n"
            "CALENTAR 180 C\n"
            "HORNEAR 180 C\n"
            "SERVIR"
        )
        self.recipe.insert("1.0", example)

        controls = ttk.Frame(left)
        controls.pack(fill="x")

        ttk.Button(
            controls, text="▶ Compilar",
            command=self.compile_recipe
        ).pack(side="left", padx=(0, 5))

        ttk.Button(
            controls, text="Limpiar",
            command=lambda: self.recipe.delete("1.0", "end")
        ).pack(side="left")

        ttk.Label(right, text="Salida: código ensamblador",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w")

        self.asm = tk.Text(
            right, font=("Consolas", 10), wrap="none",
            state="disabled"
        )
        self.asm.pack(fill="both", expand=True, pady=7)

        ttk.Label(right, text="Diagnóstico sintáctico",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w")

        self.errors = tk.Text(
            right, height=8, font=("Consolas", 10),
            wrap="word", state="disabled"
        )
        self.errors.pack(fill="x")

    def write_readonly(self, widget, text):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.config(state="disabled")

    def compile_recipe(self):
        source = self.recipe.get("1.0", "end")
        validas, errores, assembly = self.compiler.compile(source)

        self.write_readonly(
            self.asm,
            assembly if assembly.strip() else "No se generó código."
        )

        if errores:
            text = "\n".join(f"Línea {n}: {msg}" for n, msg in errores)
        else:
            text = (
                f"Compilación exitosa.\n"
                f"Sentencias válidas: {len(validas)}\n"
                f"Errores sintácticos: 0"
            )

        self.write_readonly(self.errors, text)

    def show_grammar(self):
        self.popup("Gramática formal del recetario", texto_gramatica())

    def show_tokens(self):
        lines = ["TOKEN\t\tEXPRESIÓN REGULAR", "-" * 70]
        for token, regex in token_table():
            lines.append(f"{token:<16}{regex}")
        self.popup("Tokens y expresiones regulares", "\n".join(lines))

    # ---------------- MÓDULO B ----------------

    def build_module_b(self, parent):
        top = ttk.Frame(parent)
        top.pack(fill="x")

        ttk.Label(
            top, text="Álgebra de Conjuntos",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w")

        input_frame = ttk.Frame(parent)
        input_frame.pack(fill="x", pady=10)

        ttk.Label(input_frame, text="A =").grid(row=0, column=0, sticky="w")
        self.set_a = ttk.Entry(input_frame)
        self.set_a.grid(row=0, column=1, sticky="ew", padx=7)
        self.set_a.insert(0, "1, 2, 3, -4, 3.5, hola")

        ttk.Label(input_frame, text="B =").grid(row=1, column=0, sticky="w")
        self.set_b = ttk.Entry(input_frame)
        self.set_b.grid(row=1, column=1, sticky="ew", padx=7, pady=5)
        self.set_b.insert(0, "3, 4, 5, 3.5, mundo")

        input_frame.columnconfigure(1, weight=1)

        ttk.Button(
            input_frame, text="Calcular operaciones",
            command=self.calculate_sets
        ).grid(row=0, column=2, rowspan=2, padx=8)

        self.set_output = tk.Text(
            parent, height=13, font=("Consolas", 10),
            wrap="word", state="disabled"
        )
        self.set_output.pack(fill="both", expand=True)

        kleene_frame = ttk.LabelFrame(
            parent, text="Clausura de Kleene Σ* (longitud ≤ 3)",
            padding=10
        )
        kleene_frame.pack(fill="x", pady=(10, 0))

        ttk.Label(kleene_frame, text="Σ₁ =").grid(row=0, column=0)
        self.alpha1 = ttk.Entry(kleene_frame, width=25)
        self.alpha1.grid(row=0, column=1, padx=5)
        self.alpha1.insert(0, "a,b")

        ttk.Label(kleene_frame, text="Σ₂ =").grid(row=0, column=2)
        self.alpha2 = ttk.Entry(kleene_frame, width=25)
        self.alpha2.grid(row=0, column=3, padx=5)
        self.alpha2.insert(0, "0,1")

        ttk.Button(
            kleene_frame, text="Generar Σ*",
            command=self.calculate_kleene
        ).grid(row=0, column=4, padx=7)

        self.kleene_output = tk.Text(
            parent, height=12, font=("Consolas", 10),
            wrap="word", state="disabled"
        )
        self.kleene_output.pack(fill="x", pady=(7, 0))

    def calculate_sets(self):
        try:
            A = parse_set(self.set_a.get())
            B = parse_set(self.set_b.get())

            r = operaciones(A, B)
            c = clasificar(A)

            output = [
                "=== ÁLGEBRA DE CONJUNTOS ===",
                f"A = {format_set(A)}",
                f"B = {format_set(B)}",
                "",
                f"|A| = {r['cardinalidad_A']}",
                f"|B| = {r['cardinalidad_B']}",
                "",
                f"A ∪ B = {format_set(r['union'])}",
                f"A ∩ B = {format_set(r['interseccion'])}",
                f"A \\ B = {format_set(r['A_menos_B'])}",
                f"B \\ A = {format_set(r['B_menos_A'])}",
                f"A △ B = {format_set(r['diferencia_simetrica'])}",
                "",
                f"A ⊆ B = {'Verdadero' if r['A_subconjunto_B'] else 'Falso'}",
                f"B ⊆ A = {'Verdadero' if r['B_subconjunto_A'] else 'Falso'}",
                "",
                "=== CLASIFICACIÓN DE A ===",
                f"N = {format_set(c['N'])}",
                f"Z = {format_set(c['Z'])}",
                f"Q = {format_set(c['Q'])}",
                f"Símbolos = {format_set(c['simbolos'])}",
            ]

            self.write_readonly(self.set_output, "\n".join(output))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def calculate_kleene(self):
        a1 = [x.strip() for x in self.alpha1.get().split(",") if x.strip()]
        a2 = [x.strip() for x in self.alpha2.get().split(",") if x.strip()]

        if not a1 or not a2:
            messagebox.showwarning("Datos incompletos", "Introduce los dos alfabetos.")
            return

        def block(alpha, title):
            words = kleene(alpha, 3)
            shown = ["ε" if w == "" else w for w in words]

            return (
                f"=== {title} ===\n"
                f"Σ = {{ {', '.join(alpha)} }}\n"
                f"Número de cadenas: {len(words)}\n\n"
                f"{', '.join(shown)}\n\n"
                "Gramática regular derecha:\n"
                "G = (VN, VT, P, S)\n"
                "VN = {S}\n"
                f"VT = {{ {', '.join(alpha)} }}\n"
                "P:\n"
                f"{gramatica_regular_derecha(alpha)}\n"
                "S = S\n"
            )

        self.write_readonly(
            self.kleene_output,
            block(a1, "ALFABETO 1") + "\n" + block(a2, "ALFABETO 2")
        )

    def popup(self, title, content):
        window = tk.Toplevel(self)
        window.title(title)
        window.geometry("760x560")

        text = tk.Text(window, font=("Consolas", 10), wrap="word")
        text.pack(fill="both", expand=True, padx=10, pady=10)
        text.insert("1.0", content)
        text.config(state="disabled")


def run():
    app = App()
    app.mainloop()
