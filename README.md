# Gestión de Ocupación Sol Caribe

Sistema en Python para el control y análisis de ocupación hotelera, desarrollado en equipo para Fundamentos de Programación.

## Arquitectura del proyecto

El sistema separa responsabilidades en los siguientes archivos principales:

* `business_logic.py`: Contiene la clase `Hotel`, las validaciones, la lógica de simulación, los cálculos estadísticos/niveles/rachas críticas y el manejo de persistencia en archivos `.csv`.
* `user_interface.py`: Gestiona la interacción por consola, el menú principal, la captura de datos y los mensajes al usuario.
* Archivos `.csv`: Datos de entrada y/o salida para la carga masiva y persistencia de la información.
* `README.md`: Documentación general del proyecto, integrantes, instrucciones de ejecución y evidencias finales.

## Ejecución del proyecto

1. Asegúrate de tener Python instalado en tu equipo.
2. Descarga o clona el repositorio `gestion-ocupacion-sol-caribe` (organización `equipo-sol-caribe-2026`).
3. Ejecuta el punto de entrada del sistema desde la terminal:

    python user_interface.py

## Organización del trabajo y evidencias

* **Incrementos y planificación:** El desarrollo se dividió en 3 incrementos/hitos (gestión de hoteles y simulación, informes estadísticos, y persistencia CSV con entrega final) gestionados mediante *issues* en GitHub y vinculando *commits* con `Closes #N`.
* **Integrantes y roles:**
  * Integrante 1: Santiago Crespo — Arquitectura base, validaciones de creación y menú principal.
  * Integrante 2: Cristian Muñoz — Clase `Hotel` (estructura, manejo de fechas y simulación).
  * Integrante 3: Andrés Rodríguez — Clase `Hotel` (indicadores estadísticos, niveles de ocupación y rachas críticas).
  * Integrante 4: Andrés Ospina — Carga masiva CSV, trazabilidad de errores y verificación final.
* **Evidencias finales:**
  * Video de presentación: https://youtu.be/hBs9bxnX0J8?feature=shared
  * Informes técnicos y de trazabilidad:
    * `Informe del Codigo - Hoteles Sol Caribe.pdf` (informe general de fin de curso y verificación)
    * `Informe de Analisis de Codigo - Hoteles Sol Caribe.pdf` (análisis técnico de arquitectura y módulos)
    * `Informe del Uso de la Inteligencia Artificial Generativa - Hoteles Sol Caribe.pdf` (trazabilidad de IA por incremento)
