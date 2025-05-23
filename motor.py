# Se encarga de las consultas a la base de datos MySQL, 
# y si no hay resultados, se consulta a Prolog

import mysql.connector
from pyswip import Prolog, Functor, Variable, Query
import os

os.environ['SWI_HOME_DIR'] = r"C:\Program Files\swipl"   
os.environ['PATH'] += r";C:\Program Files\swipl\bin"

# Inicializamos Prolog
prolog = Prolog()

# Cargar el archivo de base de conocimiento
ruta_base_conocimiento = os.path.join(os.path.dirname(__file__), 'BaseConocimiento_hechos.pl')
prolog.consult(ruta_base_conocimiento)

def cargar_destinos_desde_db():
    # Conexión a MySQL
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="MySQL_2%",
        database="turismo"
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, costo, tipo, idioma, cultura FROM destinos")
    destinos = cursor.fetchall()

    # Limpiar hechos previos
    prolog.retractall("destino(_,_,_,_,_)")

    # Insertar hechos en Prolog dinámicamente
    for nombre, costo, tipo, idioma, cultura in destinos:
        hecho = f"destino({nombre.lower()}, {costo}, {tipo.lower()}, {idioma.lower()}, {cultura.lower()})"
        prolog.assertz(hecho)

    cursor.close()
    conexion.close()

def recomendar_destino_prolog(presupuesto, gusto, idioma, cultura):
    resultados = []

    # Consultar usando la regla recomendar_destino/6
    query = f"recomendar_destino({presupuesto}, {gusto}, {idioma}, {cultura}, Destino, Explicacion)"
    # Como los valores son variables Prolog, deben ir entre comillas simples y con atomos
    query = f"recomendar_destino({presupuesto}, '{gusto}', '{idioma}', '{cultura}', Destino, Explicacion)"

    for sol in prolog.query(query):
        destino = sol["Destino"]
        explicacion = sol["Explicacion"]
        resultados.append((destino, explicacion))

    return resultados
