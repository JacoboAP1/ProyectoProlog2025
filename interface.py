# Este archivo contiene la interfaz de usuario para la aplicación

from controller import recomendar_destino_py

def obtener_recomendaciones(gustos, mes, presupuesto):
    """
    Función de interfaz para obtener recomendaciones de destinos turísticos.
    Recibe gustos (lista), mes (str) y presupuesto (float/int).
    Devuelve una lista de recomendaciones (diccionarios).
    """
    return recomendar_destino_py(gustos, mes, presupuesto) 