# Este archivo contiene la interfaz de usuario para la aplicación

from controller import recomendar_destino_py, recomendar_economico_py

def obtener_recomendaciones(gustos, mes, presupuesto):
    return recomendar_destino_py(gustos, mes, presupuesto)

def obtener_destinos_economicos(mes, presupuesto):
    return recomendar_economico_py(mes, presupuesto)
