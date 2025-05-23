from motor import cargar_destinos_desde_db, recomendar_destino_prolog

def main():
    # Paso 1: cargar datos desde la base de datos a Prolog
    cargar_destinos_desde_db()

    # pedir datos al usuario
    presupuesto = int(input("Ingrese su presupuesto máximo: "))
    gusto = input("Ingrese su gusto turístico (ej. playa, museo, cultura): ").lower()
    idioma = input("Ingrese su idioma preferido (ej. espanol, ingles): ").lower()
    cultura = input("Ingrese afinidad cultural (ej. europea, latina, asiatica): ").lower()

    # consultar recomendación
    resultados = recomendar_destino_prolog(presupuesto, gusto, idioma, cultura)

    # mostrar resultados
    if resultados:
        print("\nDestinos recomendados:")
        for destino, explicacion in resultados:
            print(f"- {destino.capitalize()}: {explicacion}")
    else:
        print("No se encontraron destinos que cumplan con tus criterios.")

if __name__ == "__main__":
    main()
