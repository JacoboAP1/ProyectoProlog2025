# Gestiona la lógica entre vista y motor
from motor import consultar_destino

class Controlador:
    def obtener_recomendacion(self, presupuesto, gusto, idioma, cultura):
        gusto = gusto.lower()
        idioma = idioma.lower()
        cultura = cultura.lower()
        try:
            presupuesto = int(presupuesto)
        except ValueError:
            raise ValueError("El presupuesto debe ser un número entero.")

        destino, explicacion = consultar_destino(presupuesto, gusto, idioma, cultura)
        return destino, explicacion
