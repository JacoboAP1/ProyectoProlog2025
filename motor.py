# Se encarga de las consultas a Prolog
from pyswip import Prolog

prolog = Prolog()
prolog.consult("BaseConocimiento_hechos.pl")

def consultar_destino(presupuesto, gusto, idioma, cultura):
    consulta = f"recomendar_destino({presupuesto}, {gusto}, {idioma}, {cultura}, Destino, Explicacion)"
    try:
        resultados = list(prolog.query(consulta))
        if resultados:
            return resultados[0]['Destino'], resultados[0]['Explicacion']
        else:
            return None, None
    except Exception as e:
        raise Exception(f"Error en la consulta a Prolog: {e}")
