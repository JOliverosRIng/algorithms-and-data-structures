import tkinter as tk
from tkinter import ttk, messagebox


class AlgoritmoBanqueroGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmo del Banquero")
        self.root.geometry("1050x700")

        self.num_procesos = 0
        self.num_recursos = 0

        self.entries_allocation = []
        self.entries_max = []
        self.entries_available = []

        self.crear_interfaz_principal()

    def crear_interfaz_principal(self):
        titulo = tk.Label(
            self.root,
            text="Algoritmo del Banquero",
            font=("Arial", 20, "bold")
        )
        titulo.pack(pady=10)

        frame_config = tk.Frame(self.root)
        frame_config.pack(pady=10)

        tk.Label(frame_config, text="Número de procesos:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_procesos = tk.Entry(frame_config, width=10)
        self.entry_procesos.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_config, text="Número de recursos:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_recursos = tk.Entry(frame_config, width=10)
        self.entry_recursos.grid(row=0, column=3, padx=5, pady=5)

        btn_generar = tk.Button(
            frame_config,
            text="Crear tablas",
            command=self.crear_tablas,
            bg="#1976D2",
            fg="white",
            width=15
        )
        btn_generar.grid(row=0, column=4, padx=10, pady=5)

        self.frame_scroll = tk.Frame(self.root)
        self.frame_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self.frame_scroll)
        self.scrollbar_y = ttk.Scrollbar(
            self.frame_scroll,
            orient="vertical",
            command=self.canvas.yview
        )
        self.scrollbar_x = ttk.Scrollbar(
            self.frame_scroll,
            orient="horizontal",
            command=self.canvas.xview
        )

        self.frame_tablas = tk.Frame(self.canvas)

        self.frame_tablas.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.frame_tablas, anchor="nw")
        self.canvas.configure(
            yscrollcommand=self.scrollbar_y.set,
            xscrollcommand=self.scrollbar_x.set
        )

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")

        self.frame_resultado = tk.Frame(self.root)
        self.frame_resultado.pack(fill="x", padx=10, pady=10)

        self.resultado_texto = tk.Text(
            self.frame_resultado,
            height=8,
            font=("Consolas", 11)
        )
        self.resultado_texto.pack(fill="x")

    def crear_tablas(self):
        try:
            self.num_procesos = int(self.entry_procesos.get())
            self.num_recursos = int(self.entry_recursos.get())

            if self.num_procesos <= 0 or self.num_recursos <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Error",
                "Ingrese números enteros positivos para procesos y recursos."
            )
            return

        for widget in self.frame_tablas.winfo_children():
            widget.destroy()

        self.entries_allocation = []
        self.entries_max = []
        self.entries_available = []

        self.crear_tabla_available()
        self.crear_tabla_allocation()
        self.crear_tabla_max()

        btn_calcular = tk.Button(
            self.frame_tablas,
            text="Calcular estado seguro",
            command=self.calcular_estado_seguro,
            bg="#388E3C",
            fg="white",
            width=25
        )
        btn_calcular.pack(pady=20)

        self.resultado_texto.delete("1.0", tk.END)

    def crear_tabla_available(self):
        frame = tk.LabelFrame(
            self.frame_tablas,
            text="Recursos disponibles - Available",
            padx=10,
            pady=10
        )
        frame.pack(pady=10, fill="x")

        for j in range(self.num_recursos):
            tk.Label(
                frame,
                text=f"R{j}",
                font=("Arial", 10, "bold")
            ).grid(row=0, column=j, padx=5, pady=5)

        for j in range(self.num_recursos):
            entry = tk.Entry(frame, width=8, justify="center")
            entry.grid(row=1, column=j, padx=5, pady=5)
            self.entries_available.append(entry)

    def crear_tabla_allocation(self):
        frame = tk.LabelFrame(
            self.frame_tablas,
            text="Matriz de recursos asignados - Allocation",
            padx=10,
            pady=10
        )
        frame.pack(pady=10, fill="x")

        tk.Label(
            frame,
            text="Proceso",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, padx=5, pady=5)

        for j in range(self.num_recursos):
            tk.Label(
                frame,
                text=f"R{j}",
                font=("Arial", 10, "bold")
            ).grid(row=0, column=j + 1, padx=5, pady=5)

        for i in range(self.num_procesos):
            fila = []

            tk.Label(
                frame,
                text=f"P{i}",
                font=("Arial", 10, "bold")
            ).grid(row=i + 1, column=0, padx=5, pady=5)

            for j in range(self.num_recursos):
                entry = tk.Entry(frame, width=8, justify="center")
                entry.grid(row=i + 1, column=j + 1, padx=5, pady=5)
                fila.append(entry)

            self.entries_allocation.append(fila)

    def crear_tabla_max(self):
        frame = tk.LabelFrame(
            self.frame_tablas,
            text="Matriz de demanda máxima - Max",
            padx=10,
            pady=10
        )
        frame.pack(pady=10, fill="x")

        tk.Label(
            frame,
            text="Proceso",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, padx=5, pady=5)

        for j in range(self.num_recursos):
            tk.Label(
                frame,
                text=f"R{j}",
                font=("Arial", 10, "bold")
            ).grid(row=0, column=j + 1, padx=5, pady=5)

        for i in range(self.num_procesos):
            fila = []

            tk.Label(
                frame,
                text=f"P{i}",
                font=("Arial", 10, "bold")
            ).grid(row=i + 1, column=0, padx=5, pady=5)

            for j in range(self.num_recursos):
                entry = tk.Entry(frame, width=8, justify="center")
                entry.grid(row=i + 1, column=j + 1, padx=5, pady=5)
                fila.append(entry)

            self.entries_max.append(fila)

    def leer_datos(self):
        try:
            available = []

            for j in range(self.num_recursos):
                valor = int(self.entries_available[j].get())

                if valor < 0:
                    raise ValueError

                available.append(valor)

            allocation = []

            for i in range(self.num_procesos):
                fila = []

                for j in range(self.num_recursos):
                    valor = int(self.entries_allocation[i][j].get())

                    if valor < 0:
                        raise ValueError

                    fila.append(valor)

                allocation.append(fila)

            maximo = []

            for i in range(self.num_procesos):
                fila = []

                for j in range(self.num_recursos):
                    valor = int(self.entries_max[i][j].get())

                    if valor < 0:
                        raise ValueError

                    fila.append(valor)

                maximo.append(fila)

            return available, allocation, maximo

        except ValueError:
            messagebox.showerror(
                "Error",
                "Todos los campos deben tener números enteros positivos o cero."
            )
            return None, None, None

    def calcular_need(self, allocation, maximo):
        need = []

        for i in range(self.num_procesos):
            fila = []

            for j in range(self.num_recursos):
                if allocation[i][j] > maximo[i][j]:
                    messagebox.showerror(
                        "Error",
                        f"En P{i}, R{j}: Allocation no puede ser mayor que Max."
                    )
                    return None

                fila.append(maximo[i][j] - allocation[i][j])

            need.append(fila)

        return need

    def calcular_estado_seguro(self):
        available, allocation, maximo = self.leer_datos()

        if available is None:
            return

        need = self.calcular_need(allocation, maximo)

        if need is None:
            return

        work = available.copy()
        finish = [False] * self.num_procesos
        secuencia_segura = []

        cambio = True

        while cambio:
            cambio = False

            for i in range(self.num_procesos):
                if not finish[i]:
                    puede_ejecutarse = True

                    for j in range(self.num_recursos):
                        if need[i][j] > work[j]:
                            puede_ejecutarse = False
                            break

                    if puede_ejecutarse:
                        for j in range(self.num_recursos):
                            work[j] += allocation[i][j]

                        finish[i] = True
                        secuencia_segura.append(i)
                        cambio = True

        self.mostrar_resultado(
            available,
            allocation,
            maximo,
            need,
            finish,
            secuencia_segura
        )

    def mostrar_resultado(self, available, allocation, maximo, need, finish, secuencia_segura):
        self.resultado_texto.delete("1.0", tk.END)

        self.resultado_texto.insert(tk.END, "MATRIZ NEED / NECESIDAD\n")
        self.resultado_texto.insert(tk.END, "-" * 50 + "\n")

        for i in range(self.num_procesos):
            self.resultado_texto.insert(tk.END, f"P{i}: {need[i]}\n")

        self.resultado_texto.insert(tk.END, "\n")

        if all(finish):
            self.resultado_texto.insert(
                tk.END,
                "RESULTADO: El sistema está en ESTADO SEGURO.\n"
            )

            secuencia = " -> ".join([f"P{i}" for i in secuencia_segura])

            self.resultado_texto.insert(
                tk.END,
                f"Secuencia segura: {secuencia}\n"
            )
        else:
            self.resultado_texto.insert(
                tk.END,
                "RESULTADO: El sistema NO está en estado seguro.\n"
            )
            self.resultado_texto.insert(
                tk.END,
                "No existe una secuencia segura para finalizar todos los procesos.\n"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = AlgoritmoBanqueroGUI(root)
    root.mainloop()