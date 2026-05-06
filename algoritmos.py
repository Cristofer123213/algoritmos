import random
import time
import sys
import tkinter as tk
from tkinter import ttk, messagebox

#  Algoritmos
 

def bubble_sort(arr):
    a, pasos, n = arr[:], 0, len(arr)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            pasos += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return pasos

def selection_sort(arr):
    a, pasos, n = arr[:], 0, len(arr)
    for i in range(n):
        minimo = i
        for j in range(i + 1, n):
            pasos += 1
            if a[j] < a[minimo]:
                minimo = j
        a[i], a[minimo] = a[minimo], a[i]
    return pasos

def insertion_sort(arr):
    a, pasos = arr[:], 0
    for i in range(1, len(a)):
        clave, j = a[i], i - 1
        while j >= 0:
            pasos += 1
            if a[j] <= clave:
                break
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = clave
    return pasos

def merge_sort(arr):
    pasos = [0]

    def dividir(a):
        if len(a) <= 1:
            return a
        m = len(a) // 2
        izq, der = dividir(a[:m]), dividir(a[m:])
        # mezclar las dos mitades
        res, i, j = [], 0, 0
        while i < len(izq) and j < len(der):
            pasos[0] += 1
            if izq[i] <= der[j]:
                res.append(izq[i]); i += 1
            else:
                res.append(der[j]); j += 1
        return res + izq[i:] + der[j:]

    dividir(arr[:])
    return pasos[0]

def quick_sort(arr):
    pasos = [0]

    def ordenar(a, lo, hi):
        if lo >= hi:
            return
        # particionar alrededor del último elemento como pivote
        pivote, i = a[hi], lo - 1
        for j in range(lo, hi):
            pasos[0] += 1
            if a[j] <= pivote:
                i += 1
                a[i], a[j] = a[j], a[i]
        a[i + 1], a[hi] = a[hi], a[i + 1]
        p = i + 1
        ordenar(a, lo, p - 1)
        ordenar(a, p + 1, hi)

    a = arr[:]
    sys.setrecursionlimit(max(10000, len(a) * 10))
    ordenar(a, 0, len(a) - 1)
    return pasos[0]

def heap_sort(arr):
    a, pasos, n = arr[:], 0, len(arr)

    def heapify(n, i):
        nonlocal pasos
        mayor, l, r = i, 2*i+1, 2*i+2
        pasos += 1
        if l < n and a[l] > a[mayor]: mayor = l
        pasos += 1
        if r < n and a[r] > a[mayor]: mayor = r
        if mayor != i:
            a[i], a[mayor] = a[mayor], a[i]
            heapify(n, mayor)

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        heapify(i, 0)
    return pasos

def shell_sort(arr):
    a, pasos, n = arr[:], 0, len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            tmp, j = a[i], i
            while j >= gap:
                pasos += 1
                if a[j - gap] <= tmp: break
                a[j] = a[j - gap]
                j -= gap
            a[j] = tmp
        gap //= 2
    return pasos

def counting_sort(arr):
    if not arr: return 0
    a, pasos = arr[:], 0
    mn, mx = min(a), max(a)
    cuenta = [0] * (mx - mn + 1)
    for x in a:
        pasos += 1
        cuenta[x - mn] += 1
    idx = 0
    for i, c in enumerate(cuenta):
        for _ in range(c):
            pasos += 1
            a[idx] = i + mn
            idx += 1
    return pasos

ALGORITMOS = [
    ("Bubble Sort",    bubble_sort),
    ("Selection Sort", selection_sort),
    ("Insertion Sort", insertion_sort),
    ("Merge Sort",     merge_sort),
    ("Quick Sort",     quick_sort),
    ("Heap Sort",      heap_sort),
    ("Shell Sort",     shell_sort),
    ("Counting Sort",  counting_sort),
]

 
#  Ventana principal
 

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Comparador de Algoritmos de Ordenamiento")
        self.configure(bg="white")
        self.minsize(860, 580)
        self.geometry("1000x640")
        self._construir()

    def _construir(self):
        # --- Título ---
        tk.Label(self, text="Comparador de Algoritmos de Ordenamiento",
                 bg="white", fg="black",
                 font=("Courier", 14, "bold"), pady=12).pack()

        tk.Frame(self, bg="black", height=1).pack(fill="x", padx=20)

        # --- Fila de entrada ---
        fila = tk.Frame(self, bg="white", pady=10)
        fila.pack(fill="x", padx=20)

        def campo(texto, default, ancho=6):
            tk.Label(fila, text=texto, bg="white",
                     font=("Courier", 10)).pack(side="left", padx=(10, 2))
            var = tk.StringVar(value=str(default))
            tk.Entry(fila, textvariable=var, width=ancho,
                     font=("Courier", 11), relief="solid", bd=1).pack(side="left")
            return var

        self.var_n   = campo("Cantidad:", 20)
        self.var_min = campo("Mínimo:",    1)
        self.var_max = campo("Máximo:",  100)

        self.btn = tk.Button(fila, text="Ejecutar",
                             font=("Courier", 10, "bold"),
                             relief="solid", bd=1, padx=12, pady=3,
                             cursor="hand2", command=self._ejecutar)
        self.btn.pack(side="left", padx=16)

        self.lbl_estado = tk.Label(fila, text="", bg="white",
                                   font=("Courier", 9), fg="gray")
        self.lbl_estado.pack(side="left")

        # --- Caja del array generado ---
        frame_arr = tk.Frame(self, bg="white")
        frame_arr.pack(fill="x", padx=20, pady=(4, 0))

        tk.Label(frame_arr, text="Array generado:",
                 bg="white", font=("Courier", 9), fg="gray").pack(anchor="w")

        self.txt_array = tk.Text(frame_arr, height=2,
                                  font=("Courier", 9), relief="solid", bd=1,
                                  state="disabled", wrap="word", bg="#F8F8F8")
        self.txt_array.pack(fill="x", pady=(2, 0))

        # --- Zona principal: tabla izquierda, gráfica derecha ---
        zona = tk.Frame(self, bg="white")
        zona.pack(fill="both", expand=True, padx=20, pady=10)
        zona.columnconfigure(0, weight=1, minsize=320)
        zona.columnconfigure(1, weight=2)
        zona.rowconfigure(0, weight=1)

        # Tabla
        frame_tabla = tk.Frame(zona, bg="white", bd=1, relief="solid")
        frame_tabla.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        tk.Label(frame_tabla, text="Resultados",
                 bg="white", font=("Courier", 10, "bold"),
                 pady=6).pack(anchor="w", padx=8)

        # Estilo blanco y negro para el Treeview
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("BN.Treeview",
                         background="white", foreground="black",
                         fieldbackground="white",
                         rowheight=26, font=("Courier", 10))
        estilo.configure("BN.Treeview.Heading",
                         background="#DDDDDD", foreground="black",
                         font=("Courier", 9, "bold"), relief="flat")
        estilo.map("BN.Treeview",
                   background=[("selected", "#CCCCCC")],
                   foreground=[("selected", "black")])

        cols = ("pos", "nombre", "pasos", "tiempo")
        self.tabla = ttk.Treeview(frame_tabla, columns=cols,
                                   show="headings", style="BN.Treeview",
                                   selectmode="none")
        self.tabla.heading("pos",    text="Pos")
        self.tabla.heading("nombre", text="Algoritmo")
        self.tabla.heading("pasos",  text="Pasos")
        self.tabla.heading("tiempo", text="Tiempo (ns)")
        self.tabla.column("pos",    width=36,  anchor="center")
        self.tabla.column("nombre", width=130, anchor="w")
        self.tabla.column("pasos",  width=75,  anchor="e")
        self.tabla.column("tiempo", width=105, anchor="e")
        self.tabla.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # Gráfica
        frame_graf = tk.Frame(zona, bg="white", bd=1, relief="solid")
        frame_graf.grid(row=0, column=1, sticky="nsew")

        tk.Label(frame_graf, text="Tiempo de ejecución (ns)",
                 bg="white", font=("Courier", 10, "bold"),
                 pady=6).pack(anchor="w", padx=8)

        self.canvas = tk.Canvas(frame_graf, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    # -----------------------------------------------------------------------
    #  Ejecutar comparación
    # -----------------------------------------------------------------------

    def _ejecutar(self):
        try:
            n  = int(self.var_n.get())
            mn = int(self.var_min.get())
            mx = int(self.var_max.get())
        except ValueError:
            messagebox.showerror("Error", "Los valores deben ser números enteros.")
            return

        if n <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor a 0.")
            return
        if mn > mx:
            messagebox.showerror("Error", "El mínimo no puede ser mayor que el máximo.")
            return
        if n > 5000:
            messagebox.showerror("Error", "Máximo 5000 elementos.")
            return

        self.lbl_estado.config(text="Ejecutando...")
        self.btn.config(state="disabled")
        self.update()

        arr = [random.randint(mn, mx) for _ in range(n)]

        # Mostrar el array
        self.txt_array.config(state="normal")
        self.txt_array.delete("1.0", "end")
        self.txt_array.insert("end", str(arr))
        self.txt_array.config(state="disabled")

        # Medir cada algoritmo
        resultados = []
        for nombre, fn in ALGORITMOS:
            t0    = time.perf_counter_ns()
            pasos = fn(arr)
            ns    = time.perf_counter_ns() - t0
            resultados.append((nombre, pasos, ns))

        # Ordenar de más rápido a más lento
        resultados.sort(key=lambda x: x[2])

        # Llenar tabla
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        # El ganador va en negrita con fondo gris claro
        self.tabla.tag_configure("ganador", background="#E8E8E8", font=("Courier", 10, "bold"))

        for i, (nombre, pasos, ns) in enumerate(resultados):
            tag = ("ganador",) if i == 0 else ()
            self.tabla.insert("", "end",
                              values=(i + 1, nombre, f"{pasos:,}", f"{ns:,}"),
                              tags=tag)

        self._dibujar_barras(resultados)

        self.lbl_estado.config(text=f"Listo — ganador: {resultados[0][0]}")
        self.btn.config(state="normal")

    # -----------------------------------------------------------------------
    #  Barras horizontales en blanco y negro
    # -----------------------------------------------------------------------

    def _dibujar_barras(self, resultados):
        c = self.canvas
        c.delete("all")
        self.update_idletasks()

        W, H = c.winfo_width(), c.winfo_height()
        if W < 10 or H < 10:
            self.after(80, lambda: self._dibujar_barras(resultados))
            return

        PAD_IZQ  = 120
        PAD_DER  = 90
        PAD_TOP  = 16
        PAD_BOT  = 16
        n        = len(resultados)
        espacio  = (H - PAD_TOP - PAD_BOT) / n
        alto_bar = max(14, int(espacio * 0.55))
        max_ns   = max(r[2] for r in resultados) or 1
        ancho_max = W - PAD_IZQ - PAD_DER

        # líneas de referencia verticales en gris claro
        for f in [0.25, 0.5, 0.75, 1.0]:
            x = PAD_IZQ + int(ancho_max * f)
            c.create_line(x, PAD_TOP, x, H - PAD_BOT, fill="#DDDDDD")

        for i, (nombre, pasos, ns) in enumerate(resultados):
            yc = PAD_TOP + espacio * i + espacio / 2
            y1 = int(yc - alto_bar / 2)
            y2 = int(yc + alto_bar / 2)
            ancho = max(2, int(ancho_max * ns / max_ns))

            # el ganador va relleno negro, el resto con borde negro relleno gris
            if i == 0:
                c.create_rectangle(PAD_IZQ, y1, PAD_IZQ + ancho, y2,
                                   fill="black", outline="")
                color_texto = "black"
            else:
                # tono de gris proporcional a la posición
                gris = 180 - i * 14
                hex_gris = f"#{gris:02X}{gris:02X}{gris:02X}"
                c.create_rectangle(PAD_IZQ, y1, PAD_IZQ + ancho, y2,
                                   fill=hex_gris, outline="")
                color_texto = "black"

            # nombre a la izquierda
            c.create_text(PAD_IZQ - 6, yc, text=nombre,
                          anchor="e", fill="black", font=("Courier", 9))

            # valor a la derecha
            c.create_text(PAD_IZQ + ancho + 6, yc,
                          text=f"{ns:,} ns", anchor="w",
                          fill=color_texto, font=("Courier", 9,
                          "bold" if i == 0 else "normal"))


if __name__ == "__main__":
    App().mainloop()