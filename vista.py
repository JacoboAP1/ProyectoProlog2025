import tkinter as tk
from tkinter import ttk, messagebox
from interface import obtener_recomendaciones
import os
from PIL import Image, ImageTk
import requests
from pyswip import Prolog
from controller import recomendar_destino_py, recomendar_economico_py


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
        self.canvas = tk.Canvas(self, borderwidth=0, background="#e3f2fd", width=420, height=120, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self._on_frame_configure()
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _on_frame_configure(self):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.itemconfig(self.canvas.find_withtag("all")[0], width=self.scrollable_frame.winfo_reqwidth())

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Recomendador de Destinos Turísticos")
        self.geometry("700x600")
        self.configure(bg="#dbe5ea")
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Segoe UI', 12, 'bold'), background='#1976d2', foreground='white')
        self.style.configure('TLabel', font=('Segoe UI', 11), background='#dbe5ea')
        self.style.configure('Header.TLabel', font=('Segoe UI', 18, 'bold'), background='#1976d2', foreground='white')
        self.style.configure('Result.TFrame', background='#e3f2fd')
        self.style.configure('Result.TLabel', font=('Segoe UI', 12), background='#e3f2fd')

        # Crear canvas + scrollbar para toda la ventana
        container = ttk.Frame(self)
        container.pack(fill='both', expand=True)

        self.canvas = tk.Canvas(container, bg="#f0f4f8", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style='Result.TFrame')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Ahora crea los widgets dentro de self.scrollable_frame en vez de self
        self.create_widgets()

    def create_widgets(self):
        # Frame principal centrado
        main_frame = ttk.Frame(self.scrollable_frame)
        main_frame.pack(expand=True, fill='both', padx=150)

        # Header centrado
        header = ttk.Label(main_frame, text="Recomendador de Destinos Turísticos", style='Header.TLabel', anchor='center')
        header.pack(fill='x', pady=20)

        # Frame del formulario centrado
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20, padx=150, fill='x')

        # Presupuesto
        ttk.Label(form_frame, text="Presupuesto máximo (USD):", font=('Segoe UI', 11)).grid(row=0, column=0, sticky='w', pady=10)
        self.presupuesto_var = tk.StringVar()
        self.presupuesto_entry = ttk.Entry(form_frame, textvariable=self.presupuesto_var, font=('Segoe UI', 11), width=30)
        self.presupuesto_entry.grid(row=0, column=1, sticky='ew', pady=10, padx=20)
        form_frame.columnconfigure(1, weight=1)

        # Mes
        ttk.Label(form_frame, text="Mes de viaje:", font=('Segoe UI', 11)).grid(row=1, column=0, sticky='w', pady=10)
        self.mes_var = tk.StringVar()
        self.mes_combo = ttk.Combobox(form_frame, textvariable=self.mes_var, values=MESES, state='readonly', font=('Segoe UI', 11), width=30)
        self.mes_combo.grid(row=1, column=1, sticky='ew', pady=10, padx=20)

        # Gustos (label y frame en la misma fila)
        gustos_label = ttk.Label(form_frame, text="Selecciona tus gustos:", font=('Segoe UI', 11))
        gustos_label.grid(row=2, column=0, sticky='nw', pady=10)
        gustos_frame = ScrollableFrame(form_frame)
        gustos_frame.grid(row=2, column=1, sticky='w', pady=10, padx=(10, 0))
        self.gustos_vars = {}
        num_columnas = 4
        for i, gusto in enumerate(GUSTOS):
            var = tk.BooleanVar()
            col = i % num_columnas
            row = i // num_columnas
            chk = ttk.Checkbutton(gustos_frame.scrollable_frame, text=gusto, variable=var)
            chk.grid(row=row, column=col, sticky='w', padx=10, pady=2)
            self.gustos_vars[gusto] = var

        # Botón de búsqueda centrado
        buscar_btn = ttk.Button(main_frame, text="Buscar destinos", command=self.buscar_destinos)
        buscar_btn.pack(pady=20)

        # Resultados
        resultados_label = ttk.Label(main_frame, text="Resultados:", font=('Segoe UI', 13, 'bold'))
        resultados_label.pack(anchor='w', padx=150)
        self.resultados_frame = ttk.Frame(main_frame, style='Result.TFrame')
        self.resultados_frame.pack(fill='both', expand=True, padx=150, pady=10)
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
        
        # Separador visual más largo y prominente
        separator_frame = ttk.Frame(main_frame, height=8, style='Result.TFrame')
        separator_frame.pack(fill='x', padx=20, pady=45)
        ttk.Separator(separator_frame, orient='horizontal').pack(fill='x')
        
        # Título de sección con más espacio
        ttk.Label(
            main_frame,
            text="Recomendación por Presupuesto",
            font=('Segoe UI', 22, 'bold'),
            style='Result.TLabel'
        ).pack(pady=(0, 45))
        
        # Sección para recomendar destino económico
        economico_frame = ttk.Frame(main_frame, style='Result.TFrame')
        economico_frame.pack(fill='x', padx=150, pady=20)

        # Título de la sección con un estilo distintivo
        ttk.Label(
            economico_frame, 
            text="Recomendación Más Económica de Cierto Mes", 
            font=('Segoe UI', 14, 'bold'),
            style='Result.TLabel'
        ).pack(pady=(10, 20))

        # Frame para los controles centrado
        controles_frame = ttk.Frame(economico_frame, style='Result.TFrame')
        controles_frame.pack(expand=True, fill='x', padx=150)

        # Mes
        mes_frame = ttk.Frame(controles_frame, style='Result.TFrame')
        mes_frame.pack(fill='x', pady=5)
        ttk.Label(
            mes_frame, 
            text="Mes de viaje:", 
            font=('Segoe UI', 11),
            style='Result.TLabel'
        ).pack(side='left', padx=(0, 10))
        self.mes_economico_var = tk.StringVar()
        self.mes_economico_combo = ttk.Combobox(
            mes_frame, 
            textvariable=self.mes_economico_var, 
            values=MESES, 
            state='readonly', 
            font=('Segoe UI', 11),
            width=30
        )
        self.mes_economico_combo.pack(side='left')

        # Presupuesto
        presupuesto_frame = ttk.Frame(controles_frame, style='Result.TFrame')
        presupuesto_frame.pack(fill='x', pady=5)
        ttk.Label(
            presupuesto_frame, 
            text="Presupuesto máximo:", 
            font=('Segoe UI', 11),
            style='Result.TLabel'
        ).pack(side='left', padx=(0, 10))
        self.presupuesto_economico_entry = ttk.Entry(
            presupuesto_frame, 
            font=('Segoe UI', 11),
            width=30
        )
        self.presupuesto_economico_entry.pack(side='left')
        ttk.Label(
            presupuesto_frame, 
            text="USD", 
            font=('Segoe UI', 11),
            style='Result.TLabel'
        ).pack(side='left', padx=(5, 0))

        # Botón con estilo mejorado y centrado
        economico_btn = ttk.Button(
            economico_frame, 
            text="Buscar Destino Económico", 
            command=self.mostrar_destino_economico,
            style='TButton'
        )
        economico_btn.pack(pady=20)

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

    def mostrar_destino_economico(self):
        try:
            mes = self.mes_economico_var.get()
            presupuesto = self.presupuesto_economico_entry.get()
            
            if not mes or presupuesto == "Presupuesto máximo (USD)":
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return
                
            try:
                presupuesto = float(presupuesto)
            except ValueError:
                messagebox.showerror("Error", "El presupuesto debe ser un número válido")
                return
                
            resultados = recomendar_economico_py(mes, presupuesto)
            
            if resultados:
                # Tomar el primer resultado
                resultado = resultados[0]
                ciudad = resultado['ciudad']
                pais = resultado['pais']
                costo = resultado['costo']
                mensaje = f"Destino recomendado: {ciudad}, {pais}\nPrecio estimado: ${costo:.2f} USD"
                messagebox.showinfo("Recomendación", mensaje)
                
                # Descargar y mostrar imagen del destino
                ruta_imagen = descargar_imagen_destino(ciudad)
                if ruta_imagen:
                    self.mostrar_imagen_destino(ruta_imagen)
            else:
                messagebox.showinfo("Información", "No se encontraron destinos que cumplan con los criterios especificados")
                
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def mostrar_imagen_destino(self, ruta_imagen):
        try:
            # Crear una nueva ventana para mostrar la imagen
            ventana_imagen = tk.Toplevel(self)
            ventana_imagen.title("Imagen del Destino")
            
            # Cargar y redimensionar la imagen
            imagen = Image.open(ruta_imagen)
            imagen = imagen.resize((400, 300), Image.Resampling.LANCZOS)
            foto = ImageTk.PhotoImage(imagen)
            
            # Mostrar la imagen
            label_imagen = ttk.Label(ventana_imagen, image=foto)
            label_imagen.image = foto  # Mantener una referencia
            label_imagen.pack(padx=10, pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar la imagen: {str(e)}")
