===============================================
SISTEMA EXPERTO - RECOMENDACIÓN DE DESTINOS
===============================================

Autores: [Jacobo Arroyave Pérez] - [David Esteban Toro Herrera] - [Thomas Alejandro Toro Herrera]  
Fecha de entrega: 22 de mayo de 2025

Descripción:
-------------
Este proyecto es un sistema experto desarrollado con Python y Prolog. Su objetivo es recomendar destinos turísticos de acuerdo con las preferencias del usuario: presupuesto, gusto (tipo de destino), idioma y cultura.

Estructura del proyecto:
-------------------------
- main.py                  -> Punto de entrada principal del programa.
- interfaz.py              -> Interfaz gráfica desarrollada con Tkinter.
- controlador.py           -> Controlador que conecta la vista y la lógica.
- vista.py                 -> Componentes de interfaz (separación lógica).
- motor.py                 -> Motor que realiza la consulta a Prolog.
- BaseConocimiento_hechos.pl -> Base de conocimiento con hechos y reglas Prolog.

Requisitos:
------------
- Python 3.8 o superior
- Librerías: tkinter, pyswip

Instalación de dependencias:
-----------------------------
Para instalar pyswip:

    pip install pyswip

Además, se debe tener instalado SWI-Prolog. Puedes descargarlo desde:  
https://www.swi-prolog.org/Download.html

Instrucciones de ejecución con interfaz gráfica:
-------------------------------------------------
1. Asegúrate de tener todos los archivos en la misma carpeta.
2. Ejecuta el archivo principal:

    python main.py

3. Se abrirá una ventana gráfica donde puedes ingresar:
   - Tu presupuesto
   - El tipo de destino que te gusta (por ejemplo: playa, ciudad)
   - Idioma preferido
   - Cultura afín

4. El sistema te mostrará un destino recomendado y explicará la razón de la recomendación.

Modo de uso desde la línea de comandos (SWI-Prolog):
-----------------------------------------------------
También puedes usar directamente el sistema desde la consola con SWI-Prolog:

1. Abre una terminal y navega hasta el directorio del proyecto.
2. Ejecuta SWI-Prolog con el archivo `.pl`:

    swipl BaseConocimiento_hechos.pl

3. Una vez cargado el archivo, puedes realizar consultas como por ejemplo:

    ?- recomendar_destino(2000, museo, espanol, europea, D, E).

   Esto buscará un destino que:
   - Cueste como máximo 2000
   - Sea del tipo "museo"
   - Tenga afinidad con el idioma "espanol"
   - Y/o comparta la cultura "europea"

4. El sistema responderá con un destino (`D`) y una explicación (`E`).
5. Para salir de swipl coloca "halt." y presiona ENTER.

Notas:
------
- Puedes editar el archivo `BaseConocimiento_hechos.pl` para agregar nuevos destinos.
- Asegúrate de que los datos estén en el formato correcto:  
  `destino(nombre, costo, tipo, idioma, cultura).`

Contacto:
---------
[jacobo.arroyavep@autonoma.edu.co]  
[davide.toroh@autonoma.edu.co]  
[thomasa.toroh@autonoma.edu.co]
