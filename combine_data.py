# Combina los datos de los archivos CSV y crea un archivo CSV con los datos combinados

import pandas as pd
import numpy as np
import re

def limpiar_costo(valor):
    if pd.isna(valor):
        return np.nan
    # Convertir a string y eliminar caracteres no numéricos excepto el punto
    valor_str = str(valor)
    valor_limpio = re.sub(r'[^\d.]', '', valor_str)
    try:
        return float(valor_limpio)
    except:
        return np.nan

try:
    # Leer los archivos CSV
    print("Leyendo archivos CSV...")
    destinos_df = pd.read_csv('travel_destinations.csv')
    viajes_df = pd.read_csv('Travel details dataset.csv')

    # Limpiar y procesar los datos de destinos
    print("Procesando datos de destinos...")
    destinos_df['City'] = destinos_df['City'].str.strip()
    destinos_df['Country'] = destinos_df['Country'].str.strip()
    destinos_df['Category'] = destinos_df['Category'].str.strip()

    # Limpiar y procesar los datos de viajes
    print("Procesando datos de viajes...")
    viajes_df['Destination'] = viajes_df['Destination'].str.strip()
    
    # Extraer ciudad y país del destino
    viajes_df[['City', 'Country']] = viajes_df['Destination'].str.split(',', expand=True)
    viajes_df['City'] = viajes_df['City'].str.strip()
    viajes_df['Country'] = viajes_df['Country'].str.strip()

    # Limpiar costos
    print("Limpiando datos de costos...")
    viajes_df['Accommodation cost'] = viajes_df['Accommodation cost'].apply(limpiar_costo)
    viajes_df['Transportation cost'] = viajes_df['Transportation cost'].apply(limpiar_costo)

    # Calcular estadísticas de costos por destino
    print("Calculando estadísticas...")
    costos_por_destino = viajes_df.groupby(['City', 'Country']).agg({
        'Accommodation cost': ['mean', 'min', 'max'],
        'Transportation cost': ['mean', 'min', 'max'],
        'Duration (days)': 'mean'
    }).reset_index()

    # Renombrar columnas para mayor claridad
    costos_por_destino.columns = ['City', 'Country', 
                                'Costo_Alojamiento_Promedio', 'Costo_Alojamiento_Min', 'Costo_Alojamiento_Max',
                                'Costo_Transporte_Promedio', 'Costo_Transporte_Min', 'Costo_Transporte_Max',
                                'Duracion_Promedio']

    # Combinar con la información de destinos
    print("Combinando datos...")
    resultado_df = pd.merge(destinos_df, costos_por_destino, 
                           on=['City', 'Country'], 
                           how='left')

    # Calcular el costo total promedio
    resultado_df['Costo_Total_Promedio'] = resultado_df['Costo_Alojamiento_Promedio'] + resultado_df['Costo_Transporte_Promedio']

    # Seleccionar y ordenar las columnas más relevantes
    columnas_finales = [
        'City', 'Country', 'Category', 'Best_Time_to_Travel',
        'Costo_Total_Promedio', 'Costo_Alojamiento_Promedio', 'Costo_Transporte_Promedio',
        'Costo_Alojamiento_Min', 'Costo_Alojamiento_Max',
        'Costo_Transporte_Min', 'Costo_Transporte_Max',
        'Duracion_Promedio'
    ]

    resultado_df = resultado_df[columnas_finales]

    # Guardar el resultado
    print("Guardando archivo...")
    resultado_df.to_csv('destinos_combinados.csv', index=False)

    print("Archivo 'destinos_combinados.csv' creado exitosamente.")
    print("\nPrimeras 5 filas del archivo combinado:")
    print(resultado_df.head())

except Exception as e:
    print(f"Error: {str(e)}") 