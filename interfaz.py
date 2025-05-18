# Conecta al controlador con la vista
from vista import VistaRecomendaciones

class Interfaz:
    def __init__(self, controlador):
        self.vista = VistaRecomendaciones(controlador)

    def iniciar(self):
        self.vista.mostrar_ventana()

def iniciar_interfaz():
    from controlador import Controlador
    controlador = Controlador()
    interfaz = Interfaz(controlador)
    interfaz.iniciar()
