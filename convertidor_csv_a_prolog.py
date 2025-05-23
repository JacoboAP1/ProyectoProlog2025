# Este archivo convierte los datos de un archivo CSV a un archivo Prolog

import csv

# Abrir el archivo CSV
with open('destinos_combinados.csv', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    with open('motor.pl', 'w', encoding='utf-8') as plfile:
        for row in reader:
            ciudad = row['City'].replace('"', '').strip()
            pais = row['Country'].replace('"', '').strip()
            # Procesar gustos
            gustos = row['Category'].replace('"', '').strip()
            lista_gustos = [g.strip() for g in gustos.split(',')] if gustos else []
            # Procesar meses
            meses = row['Best_Time_to_Travel'].replace('"', '').strip()
            lista_meses = [m.strip() for m in meses.split(',')] if meses else []
            # Procesar costo promedio
            costo = row['Costo_Total_Promedio'].strip()
            costo = costo if costo else '0'
            # Escribir hecho en Prolog
            hecho = f'destino("{ciudad}", "{pais}", {lista_gustos}, {lista_meses}, {costo}).\n'
            plfile.write(hecho) 