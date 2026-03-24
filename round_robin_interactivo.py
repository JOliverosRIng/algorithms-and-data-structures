# Este programa simula el algoritmo de planificación Round Robin con una interfaz gráfica interactiva usando Tkinter.

# Hecho por: Janeth Oliveros Ramirez - 20182020100 & Hana Sofía Pinilla Manrique - 20221020092

# Se hizo uso de IA para las barras de Scrolling, la mejora de la interfaz gráfica en los estilos y en el inicio por medio de un ejemplo.

#El sistema inicia con un ejemplo por default pero el usuario puede limpiar los datos e introducir las tareas, los tiempo iniciales, las ráfagas y el quantum.

import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque


class RoundRobinGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Round Robin con interfaz gráfica")
        self.geometry("1360x900")
        self.minsize(1180, 760)
        self.configure(bg="#ffffff")

        self.quantum_var = tk.StringVar(value="2")
        self.name_var = tk.StringVar()
        self.arrival_var = tk.StringVar()
        self.burst_var = tk.StringVar()
        self.quantum_label_var = tk.StringVar(value="Quantum: 2")
        self.status_var = tk.StringVar(value="Agrega las tareas y presiona 'Generar diagrama'.")

        self.tasks = []
        self.color_palette = [
            "#b8d4ff",
            "#f3dc8c",
            "#b7d9a8",
            "#d9c2d1",
            "#c5d5e8",
            "#ffcc99",
            "#d0bdf4",
            "#b5ead7",
            "#ffd6e0",
            "#d9f99d",
        ]

        self._build_style()
        self._build_scrollable_window()
        self._build_ui()
        self.after(250, self.load_example)

    def _build_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), background="#f3f4f6")
        style.configure("Sub.TLabel", font=("Segoe UI", 11), background="#f3f4f6")
        style.configure("Card.TLabelframe", background="#f3f4f6")
        style.configure("Card.TLabelframe.Label", background="#f3f4f6", font=("Segoe UI", 11, "bold"))
        style.configure("Dark.TLabelframe", background="#0f172a")
        style.configure("Dark.TLabelframe.Label", background="#0f172a", foreground="white", font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def _build_scrollable_window(self):
        container = tk.Frame(self, bg="#f3f4f6")
        container.pack(fill="both", expand=True)

        self.window_canvas = tk.Canvas(container, bg="#f3f4f6", highlightthickness=0)
        self.window_vbar = ttk.Scrollbar(container, orient="vertical", command=self.window_canvas.yview)
        self.window_hbar = ttk.Scrollbar(container, orient="horizontal", command=self.window_canvas.xview)
        self.window_canvas.configure(yscrollcommand=self.window_vbar.set, xscrollcommand=self.window_hbar.set)

        self.window_canvas.grid(row=0, column=0, sticky="nsew")
        self.window_vbar.grid(row=0, column=1, sticky="ns")
        self.window_hbar.grid(row=1, column=0, sticky="ew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.content = tk.Frame(self.window_canvas, bg="#f3f4f6")
        self.content_window = self.window_canvas.create_window((0, 0), window=self.content, anchor="nw")

        self.content.bind("<Configure>", self._on_content_configure)
        self.window_canvas.bind("<Configure>", self._on_window_canvas_configure)

        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind_all("<Shift-MouseWheel>", self._on_shift_mousewheel)

    def _on_content_configure(self, event=None):
        self.window_canvas.configure(scrollregion=self.window_canvas.bbox("all"))

    def _on_window_canvas_configure(self, event):
        self.window_canvas.itemconfig(self.content_window, width=event.width)

    def _on_mousewheel(self, event):
        if event.delta:
            self.window_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_shift_mousewheel(self, event):
        if event.delta:
            self.window_canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def _build_ui(self):
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=0)
        self.content.grid_rowconfigure(1, weight=0)
        self.content.grid_rowconfigure(2, weight=0)
        self.content.grid_rowconfigure(3, weight=0)

        header = tk.Frame(self.content)
        header.grid(row=0, column=0, sticky="ew", padx=18, pady=(14, 8))
        header.grid_columnconfigure(0, weight=1)

        ttk.Label(header, text="Algoritmo de planificación Round Robin", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="Añade las tareas, indica el tiempo de inicio, la ráfaga y el quantum. Luego genera el diagrama de Gantt en forma de matriz.",
            style="Sub.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))

        top = ttk.Frame(self.content)
        top.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 10))
        top.grid_columnconfigure(0, weight=3)
        top.grid_columnconfigure(1, weight=2)

        form = ttk.LabelFrame(top, text="Entrada de datos", style="Card.TLabelframe", padding=14)
        form.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        for i in range(8):
            form.grid_columnconfigure(i, weight=1)

        ttk.Label(form, text="Proceso:").grid(row=0, column=0, sticky="w", padx=4, pady=6)
        ttk.Entry(form, textvariable=self.name_var, width=12).grid(row=0, column=1, sticky="ew", padx=4, pady=6)

        ttk.Label(form, text="Tiempo de inicio:").grid(row=0, column=2, sticky="w", padx=4, pady=6)
        ttk.Entry(form, textvariable=self.arrival_var, width=12).grid(row=0, column=3, sticky="ew", padx=4, pady=6)

        ttk.Label(form, text="Ráfaga:").grid(row=0, column=4, sticky="w", padx=4, pady=6)
        ttk.Entry(form, textvariable=self.burst_var, width=12).grid(row=0, column=5, sticky="ew", padx=4, pady=6)

        ttk.Label(form, text="Quantum:").grid(row=0, column=6, sticky="w", padx=4, pady=6)
        ttk.Entry(form, textvariable=self.quantum_var, width=10).grid(row=0, column=7, sticky="ew", padx=4, pady=6)

        buttons = ttk.Frame(form)
        buttons.grid(row=1, column=0, columnspan=8, sticky="w", pady=(8, 0))
        ttk.Button(buttons, text="Añadir tarea", command=self.add_task).pack(side="left", padx=(0, 6))
        ttk.Button(buttons, text="Eliminar seleccionada", command=self.delete_selected).pack(side="left", padx=6)
        ttk.Button(buttons, text="Limpiar tareas", command=self.clear_tasks).pack(side="left", padx=6)
        ttk.Button(buttons, text="Cargar ejemplo", command=self.load_example).pack(side="left", padx=6)
        ttk.Button(buttons, text="Generar diagrama", command=self.generate_diagram).pack(side="left", padx=6)

        ttk.Label(form, textvariable=self.status_var, foreground="#374151").grid(
            row=2, column=0, columnspan=8, sticky="w", pady=(10, 0), padx=4
        )

        side = ttk.LabelFrame(top, text="Resumen", style="Card.TLabelframe", padding=14)
        side.grid(row=0, column=1, sticky="nsew")

        self.quantum_box = tk.Label(
            side,
            textvariable=self.quantum_label_var,
            bg="#7fa4f8",
            fg="white",
            font=("Segoe UI", 18, "bold"),
            height=3,
        )
        self.quantum_box.pack(fill="x", pady=(4, 10))

        info = (
            "La tabla muestra las tareas ingresadas por el usuario.\n"
            "En el diagrama inferior:\n"
            "• Eje X: unidades de tiempo\n"
            "• Eje Y: tareas\n"
            "• X: instante de llegada al sistema"
        )
        ttk.Label(side, text=info, justify="left").pack(anchor="w")

        table_card = ttk.LabelFrame(self.content, text="Tareas registradas", style="Card.TLabelframe", padding=12)
        table_card.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 10))
        table_card.grid_columnconfigure(0, weight=1)

        cols = ("proceso", "inicio", "rafaga")
        self.tree = ttk.Treeview(table_card, columns=cols, show="headings", height=5)
        self.tree.heading("proceso", text="PROCESO")
        self.tree.heading("inicio", text="INICIO")
        self.tree.heading("rafaga", text="RÁFAGA")
        self.tree.column("proceso", width=250, anchor="center")
        self.tree.column("inicio", width=200, anchor="center")
        self.tree.column("rafaga", width=200, anchor="center")
        self.tree.grid(row=0, column=0, sticky="ew")

        diagram_card = ttk.LabelFrame(self.content, text="Diagrama de Gantt", style="Dark.TLabelframe", padding=10)
        diagram_card.grid(row=3, column=0, sticky="nsew", padx=18, pady=(0, 18))
        diagram_card.grid_columnconfigure(0, weight=1)
        diagram_card.grid_rowconfigure(0, weight=1)

        self.canvas_container = tk.Frame(diagram_card, bg="#111111", height=420)
        self.canvas_container.grid(row=0, column=0, sticky="nsew")
        self.canvas_container.grid_columnconfigure(0, weight=1)
        self.canvas_container.grid_rowconfigure(0, weight=1)
        self.canvas_container.grid_propagate(False)

        self.canvas = tk.Canvas(
            self.canvas_container,
            bg="#111111",
            highlightthickness=0,
            xscrollincrement=24,
            yscrollincrement=24,
            height=390,
        )
        self.hbar = ttk.Scrollbar(self.canvas_container, orient="horizontal", command=self.canvas.xview)
        self.vbar = ttk.Scrollbar(self.canvas_container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.vbar.grid(row=0, column=1, sticky="ns")
        self.hbar.grid(row=1, column=0, sticky="ew")

        self.show_placeholder()

    def show_placeholder(self):
        self.canvas.delete("all")
        w = 1100
        h = 360
        self.canvas.configure(scrollregion=(0, 0, w, h))
        self.canvas.create_rectangle(0, 0, w, h, fill="#111111", outline="#111111")
        self.canvas.create_text(
            w / 2,
            h / 2 - 12,
            text="Aquí aparecerá el diagrama de Gantt",
            fill="white",
            font=("Segoe UI", 18, "bold"),
        )
        self.canvas.create_text(
            w / 2,
            h / 2 + 18,
            text="Agrega tareas y presiona 'Generar diagrama'",
            fill="#cbd5e1",
            font=("Segoe UI", 11),
        )

    def default_process_name(self):
        used = {task["name"] for task in self.tasks}
        for i in range(26):
            name = chr(65 + i)
            if name not in used:
                return name
        return f"P{len(self.tasks) + 1}"

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for task in sorted(self.tasks, key=lambda t: (t["arrival"], t["name"])):
            self.tree.insert("", "end", values=(task["name"], task["arrival"], task["burst"]))
        self.quantum_label_var.set(f"Quantum: {self.quantum_var.get().strip() or '-'}")
        self.update_idletasks()
        self._on_content_configure()

    def add_task(self):
        name = self.name_var.get().strip() or self.default_process_name()
        try:
            arrival = int(self.arrival_var.get())
            burst = int(self.burst_var.get())
        except ValueError:
            messagebox.showerror("Dato inválido", "El tiempo de inicio y la ráfaga deben ser números enteros.")
            return

        if arrival < 0:
            messagebox.showerror("Dato inválido", "El tiempo de inicio no puede ser negativo.")
            return
        if burst <= 0:
            messagebox.showerror("Dato inválido", "La ráfaga debe ser mayor que cero.")
            return
        if any(task["name"] == name for task in self.tasks):
            messagebox.showerror("Nombre repetido", f"Ya existe una tarea llamada '{name}'.")
            return

        self.tasks.append({"name": name, "arrival": arrival, "burst": burst})
        self.refresh_table()
        self.name_var.set("")
        self.arrival_var.set("")
        self.burst_var.set("")
        self.status_var.set(f"Tarea '{name}' añadida correctamente.")

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Selecciona una tarea", "Primero selecciona una fila de la tabla.")
            return

        item_id = selected[0]
        values = self.tree.item(item_id, "values")
        process_name = values[0]
        self.tasks = [task for task in self.tasks if task["name"] != process_name]
        self.refresh_table()
        self.status_var.set(f"Tarea '{process_name}' eliminada.")
        if self.tasks:
            self.generate_diagram()
        else:
            self.show_placeholder()

    def clear_tasks(self):
        self.tasks.clear()
        self.refresh_table()
        self.show_placeholder()
        self.status_var.set("Se limpiaron todas las tareas.")

    def load_example(self):
        self.tasks = [
            {"name": "A", "arrival": 0, "burst": 3},
            {"name": "B", "arrival": 2, "burst": 6},
            {"name": "C", "arrival": 4, "burst": 4},
            {"name": "D", "arrival": 8, "burst": 2},
        ]
        self.quantum_var.set("2")
        self.name_var.set("")
        self.arrival_var.set("")
        self.burst_var.set("")
        self.refresh_table()
        self.generate_diagram()
        self.status_var.set("Ejemplo cargado.")

    def simulate_round_robin(self, tasks, quantum):
        work = [
            {
                "name": task["name"],
                "arrival": task["arrival"],
                "burst": task["burst"],
                "remaining": task["burst"],
                "order": idx,
            }
            for idx, task in enumerate(tasks)
        ]

        work.sort(key=lambda t: (t["arrival"], t["order"]))
        queue = deque()
        time = 0
        index = 0
        completed = 0
        total = len(work)
        segments = []

        while completed < total:
            while index < total and work[index]["arrival"] <= time:
                queue.append(work[index])
                index += 1

            if not queue:
                next_time = work[index]["arrival"]
                if next_time > time:
                    segments.append({"name": "IDLE", "start": time, "end": next_time})
                    time = next_time
                continue

            current = queue.popleft()
            run = min(quantum, current["remaining"])
            start = time
            end = time + run
            segments.append({"name": current["name"], "start": start, "end": end})
            current["remaining"] -= run
            time = end

            while index < total and work[index]["arrival"] <= time:
                queue.append(work[index])
                index += 1

            if current["remaining"] > 0:
                queue.append(current)
            else:
                completed += 1

        return segments

    def generate_diagram(self):
        if not self.tasks:
            messagebox.showinfo("Sin tareas", "Debes añadir al menos una tarea.")
            return

        try:
            quantum = int(self.quantum_var.get())
        except ValueError:
            messagebox.showerror("Quantum inválido", "El quantum debe ser un número entero.")
            return

        if quantum <= 0:
            messagebox.showerror("Quantum inválido", "El quantum debe ser mayor que cero.")
            return

        self.refresh_table()
        segments = self.simulate_round_robin(self.tasks, quantum)
        self.draw_matrix(segments, quantum)
        self.status_var.set("Diagrama generado correctamente.")
        self.after(50, lambda: self.window_canvas.yview_moveto(1.0))

    def draw_matrix(self, segments, quantum):
        self.canvas.delete("all")

        ordered_tasks = sorted(self.tasks, key=lambda t: (t["arrival"], t["name"]))
        names = [task["name"] for task in ordered_tasks]
        if not names or not segments:
            return

        total_time = max(segment["end"] for segment in segments)
        color_map = {name: self.color_palette[i % len(self.color_palette)] for i, name in enumerate(names)}

        left_margin = 150
        top_margin = 60
        cell_w = 48
        cell_h = 52
        bottom_space = 72
        right_space = 40

        width = left_margin + total_time * cell_w + right_space
        height = top_margin + len(names) * cell_h + bottom_space

        self.canvas.configure(scrollregion=(0, 0, width, height))
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.canvas.create_rectangle(0, 0, width, height, fill="#111111", outline="#111111")
        self.canvas.create_text(
            left_margin,
            24,
            text=f"Diagrama de Gantt | Q = {quantum}",
            fill="white",
            anchor="w",
            font=("Segoe UI", 16, "bold"),
        )

        for row, name in enumerate(names):
            y1 = top_margin + row * cell_h
            y2 = y1 + cell_h
            self.canvas.create_rectangle(24, y1, left_margin - 12, y2, fill="#768c9d", outline="#9ca3af")
            self.canvas.create_text((24 + left_margin - 12) / 2, (y1 + y2) / 2, text=name, fill="white", font=("Segoe UI", 14, "bold"))

        for row in range(len(names)):
            y1 = top_margin + row * cell_h
            y2 = y1 + cell_h
            for t in range(total_time):
                x1 = left_margin + t * cell_w
                x2 = x1 + cell_w
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#efefef", outline="#b6b6b6")

        row_map = {name: idx for idx, name in enumerate(names)}
        for segment in segments:
            if segment["name"] == "IDLE":
                for t in range(segment["start"], segment["end"]):
                    x1 = left_margin + t * cell_w
                    x2 = x1 + cell_w
                    self.canvas.create_rectangle(
                        x1,
                        top_margin,
                        x2,
                        top_margin + len(names) * cell_h,
                        fill="#f8fafc",
                        outline="#b6b6b6",
                        stipple="gray25",
                    )
                continue

            row = row_map[segment["name"]]
            y1 = top_margin + row * cell_h
            y2 = y1 + cell_h
            for t in range(segment["start"], segment["end"]):
                x1 = left_margin + t * cell_w
                x2 = x1 + cell_w
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color_map[segment["name"]], outline="#b6b6b6")

        for task in ordered_tasks:
            row = row_map[task["name"]]
            y1 = top_margin + row * cell_h
            y2 = y1 + cell_h
            x1 = left_margin + task["arrival"] * cell_w
            x2 = x1 + cell_w
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="X", fill="#111111", font=("Segoe UI", 18, "bold"))

        axis_y = top_margin + len(names) * cell_h + 12
        self.canvas.create_text(30, axis_y + 14, text="Clock", fill="white", anchor="w", font=("Segoe UI", 11, "bold"))

        for t in range(total_time + 1):
            x = left_margin + t * cell_w
            self.canvas.create_line(x, top_margin, x, top_margin + len(names) * cell_h, fill="#9ca3af")
            self.canvas.create_text(x, axis_y + 14, text=str(t), fill="white", font=("Segoe UI", 13))

        self.canvas.create_line(
            left_margin,
            top_margin + len(names) * cell_h,
            left_margin + total_time * cell_w,
            top_margin + len(names) * cell_h,
            fill="#d1d5db",
            width=1,
        )

        legend_y = axis_y + 42
        self.canvas.create_text(24, legend_y, text="X = tiempo de llegada al sistema", fill="white", anchor="w", font=("Segoe UI", 11, "bold"))

        self.update_idletasks()
        self._on_content_configure()


if __name__ == "__main__":
    app = RoundRobinGUI()
    app.mainloop()
