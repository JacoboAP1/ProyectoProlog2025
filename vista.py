import tkinter as tk
from tkinter import ttk, messagebox
from interface import obtener_recomendaciones
import os
from PIL import Image, ImageTk
import requests
from pyswip import Prolog

# Listas fijas de gustos y meses
GUSTOS = [
    'beach', 'history', 'culture', 'nightlife', 'food', 'nature', 'art', 'shopping', 'mountains', 'adventure',
    'architecture', 'music', 'relaxation', 'sports', 'islands', 'museums', 'romance', 'festivals', 'technology', 'wine'
]
MESES = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
]

UNSPLASH_ACCESS_KEY = "2Dzla8YkatgAmwzykQL36mT5vZL0B3M4AqcSyfXJxms"  

# Cambia esta ruta según la ubicación real de tu carpeta de imágenes
CARPETA_IMAGENES = r"C:\Users\arroy\OneDrive\Documentos\5to semestre\Paradigmas de lenguajes\Prolog\ProyectoProlog2025\imagenes_destinos"

def descargar_imagen_destino(ciudad):
    carpeta = CARPETA_IMAGENES
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    nombre_archivo = f"{ciudad}.jpg"
    ruta = os.path.join(carpeta, nombre_archivo)
    if os.path.exists(ruta):
        return ruta  # Ya existe
    url = f"https://api.unsplash.com/photos/random?query={ciudad}&client_id={UNSPLASH_ACCESS_KEY}"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            img_url = data['urls']['small']
            img_data = requests.get(img_url).content
            with open(ruta, 'wb') as handler:
                handler.write(img_data)
            return ruta
    except Exception as e:
        print(f"Error descargando imagen para {ciudad}: {e}")
    return None

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, borderwidth=0, background="#f7f7f7", height=120)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Recomendador de Destinos Turísticos")
        self.geometry("700x600")
        self.configure(bg="#f0f4f8")
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Segoe UI', 12, 'bold'), background='#1976d2', foreground='white')
        self.style.configure('TLabel', font=('Segoe UI', 11), background='#f0f4f8')
        self.style.configure('Header.TLabel', font=('Segoe UI', 18, 'bold'), background='#1976d2', foreground='white')
        self.style.configure('Result.TFrame', background='#e3f2fd')
        self.style.configure('Result.TLabel', font=('Segoe UI', 12), background='#e3f2fd')
        self.create_widgets()

    def create_widgets(self):
        header = ttk.Label(self, text="Recomendador de Destinos Turísticos", style='Header.TLabel', anchor='center')
        header.pack(fill='x', pady=10)

        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10, padx=20, fill='x')

        # Presupuesto
        ttk.Label(form_frame, text="Presupuesto máximo (USD):").grid(row=0, column=0, sticky='w', pady=5)
        self.presupuesto_var = tk.StringVar()
        self.presupuesto_entry = ttk.Entry(form_frame, textvariable=self.presupuesto_var, font=('Segoe UI', 11))
        self.presupuesto_entry.grid(row=0, column=1, sticky='ew', pady=5)
        form_frame.columnconfigure(1, weight=1)

        # Mes
        ttk.Label(form_frame, text="Mes de viaje:").grid(row=1, column=0, sticky='w', pady=5)
        self.mes_var = tk.StringVar()
        self.mes_combo = ttk.Combobox(form_frame, textvariable=self.mes_var, values=MESES, state='readonly', font=('Segoe UI', 11))
        self.mes_combo.grid(row=1, column=1, sticky='ew', pady=5)

        # Gustos
        ttk.Label(form_frame, text="Selecciona tus gustos:").grid(row=2, column=0, sticky='nw', pady=5)
        gustos_frame = ScrollableFrame(form_frame)
        gustos_frame.grid(row=2, column=1, sticky='ew', pady=5)
        self.gustos_vars = {}
        for i, gusto in enumerate(GUSTOS):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(gustos_frame.scrollable_frame, text=gusto, variable=var)
            chk.grid(row=i, column=0, sticky='w')
            self.gustos_vars[gusto] = var

        # Botón de búsqueda
        buscar_btn = ttk.Button(self, text="Buscar destinos", command=self.buscar_destinos)
        buscar_btn.pack(pady=20)

        # Resultados
        resultados_label = ttk.Label(self, text="Resultados:", font=('Segoe UI', 13, 'bold'))
        resultados_label.pack(anchor='w', padx=20)
        self.resultados_frame = ttk.Frame(self, style='Result.TFrame')
        self.resultados_frame.pack(fill='both', expand=True, padx=20, pady=10)
        self.resultados_canvas = tk.Canvas(self.resultados_frame, bg='#e3f2fd', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.resultados_frame, orient="vertical", command=self.resultados_canvas.yview)
        self.scrollable_results = ttk.Frame(self.resultados_canvas, style='Result.TFrame')
        self.scrollable_results.bind(
            "<Configure>",
            lambda e: self.resultados_canvas.configure(
                scrollregion=self.resultados_canvas.bbox("all")
            )
        )
        self.resultados_canvas.create_window((0, 0), window=self.scrollable_results, anchor="nw")
        self.resultados_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.resultados_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def buscar_destinos(self):
        # Validar datos
        try:
            presupuesto = float(self.presupuesto_var.get())
            if presupuesto <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un presupuesto válido.")
            return
        mes = self.mes_var.get()
        if not mes:
            messagebox.showerror("Error", "Por favor selecciona un mes de viaje.")
            return
        gustos = [g for g, var in self.gustos_vars.items() if var.get()]
        if not gustos:
            messagebox.showerror("Error", "Por favor selecciona al menos un gusto.")
            return
        # Limpiar resultados anteriores
        for widget in self.scrollable_results.winfo_children():
            widget.destroy()
        # Consultar recomendaciones
        recomendaciones = obtener_recomendaciones(gustos, mes, presupuesto)
        if not recomendaciones:
            ttk.Label(self.scrollable_results, text="No se encontraron destinos que coincidan con tus preferencias.", style='Result.TLabel').pack(anchor='w', pady=10)
            return
        for rec in recomendaciones:
            ciudad = rec['ciudad'].decode() if isinstance(rec['ciudad'], bytes) else rec['ciudad']
            pais = rec['pais'].decode() if isinstance(rec['pais'], bytes) else rec['pais']
            frame = ttk.Frame(self.scrollable_results, style='Result.TFrame', padding=10)
            frame.pack(fill='x', pady=5)
            ttk.Label(frame, text=f"{ciudad}, {pais}", style='Result.TLabel', font=('Segoe UI', 13, 'bold')).pack(anchor='w')
            # Mostrar imagen si existe o descargarla
            img_path = descargar_imagen_destino(ciudad)
            print(f"Mostrando imagen para: {ciudad} en {img_path}")
            if img_path and os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    if hasattr(Image, 'Resampling'):
                        img = img.resize((120, 80), Image.Resampling.LANCZOS)
                    else:
                        img = img.resize((120, 80), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(img)
                    img_label = ttk.Label(frame, image=photo, style='Result.TLabel')
                    img_label.image = photo  # Mantener referencia
                    img_label.pack(anchor='w', pady=2)
                except Exception as e:
                    print(f"Error mostrando imagen: {e}")
            ttk.Label(frame, text=rec['explicacion'], style='Result.TLabel', wraplength=600, justify='left').pack(anchor='w', pady=2)
