# Este archivo contiene la lógica de negocio para la aplicación

from pyswip import Prolog

def recomendar_destino_py(gustos, mes, presupuesto):
    prolog = Prolog()
    prolog.consult("motor.pl")  # Asegúrate que la ruta esté correcta
    resultados = []
    consulta = f"recomendar_destino({gustos}, '{mes}', {presupuesto}, Ciudad, Pais, Explicacion)"
    ciudades_vistas = set()
    for sol in prolog.query(consulta):
        ciudad = sol["Ciudad"]
        if ciudad not in ciudades_vistas:
            ciudades_vistas.add(ciudad)
            resultados.append({
                "ciudad": ciudad,
                "pais": sol["Pais"],
                "explicacion": sol["Explicacion"]
            })
    return resultados

def recomendar_economico_py(mes, presupuesto):
    prolog = Prolog()
    prolog.consult("motor.pl")  # Reutilizamos el mismo archivo
    resultados = []
    consulta = f"recomendar_economico(Ciudad, Pais, {presupuesto}, '{mes}', Costo, Explicacion)"
    ciudades_vistas = set()
    for sol in prolog.query(consulta):
        ciudad = sol["Ciudad"]
        if ciudad not in ciudades_vistas:
            ciudades_vistas.add(ciudad)
            resultados.append({
                "ciudad": ciudad,
                "pais": sol["Pais"],
                "costo": sol["Costo"],
                "explicacion": sol["Explicacion"]
            })
    return resultados
