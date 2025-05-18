import tkinter as tk
from tkinter import messagebox

class VistaRecomendaciones:
    def __init__(self, controlador):
        self.controlador = controlador
        self.ventana = tk.Tk()
        self.ventana.title("Asistente de Viaje Inteligente")

        tk.Label(self.ventana, text="Presupuesto (USD):").grid(row=0, column=0, padx=5, pady=5)
        self.entry_presupuesto = tk.Entry(self.ventana)
        self.entry_presupuesto.grid(row=0, column=1)

        tk.Label(self.ventana, text="Gusto de viaje:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_gusto = tk.Entry(self.ventana)
        self.entry_gusto.grid(row=1, column=1)

        tk.Label(self.ventana, text="Idioma nativo:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_idioma = tk.Entry(self.ventana)
        self.entry_idioma.grid(row=2, column=1)

        tk.Label(self.ventana, text="Cultura de afinidad:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_cultura = tk.Entry(self.ventana)
        self.entry_cultura.grid(row=3, column=1)

        tk.Button(self.ventana, text="Recomendar destino", command=self.recomendar_destino).grid(row=4, columnspan=2, pady=10)

    def mostrar_ventana(self):
        self.ventana.mainloop()

    def recomendar_destino(self):
        try:
            presupuesto = int(self.entry_presupuesto.get())
            gusto = self.entry_gusto.get().lower()
            idioma = self.entry_idioma.get().lower()
            cultura = self.entry_cultura.get().lower()

            destino, explicacion = self.controlador.obtener_recomendacion(presupuesto, gusto, idioma, cultura)

            if destino:
                messagebox.showinfo("Recomendación", f"Destino recomendado: {destino.capitalize()}\n\nExplicación: {explicacion}")
            else:
                messagebox.showinfo("Sin resultados", "No se encontraron destinos con esos criterios.")

        except Exception as e:
            messagebox.showerror("Error", f"Entrada inválida o error: {e}")
