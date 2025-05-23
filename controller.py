# Este archivo contiene la lógica de negocio para la aplicación

from pyswip import Prolog

def recomendar_destino_py(gustos, mes, presupuesto):
    prolog = Prolog()
    prolog.consult("motor.pl")
    resultados = []
    consulta = f"recomendar_destino({gustos}, '{mes}', {presupuesto}, Ciudad, Pais, Explicacion)"
    for sol in prolog.query(consulta):
        resultados.append({
            "ciudad": sol["Ciudad"],
            "pais": sol["Pais"],
            "explicacion": sol["Explicacion"]
        })
    return resultados
