# Sistema Software FJ — Fase 4 (Programación)

Proyecto académico desarrollado para la **Fase 4 del curso de Programación** en la **Universidad Nacional Abierta y a Distancia (UNAD)**. El sistema simula la gestión de clientes, servicios y reservas aplicando Programación Orientada a Objetos (POO) avanzada, excepciones personalizadas y registro de eventos (*logs*) en archivo de texto sin utilizar base de datos.

## Características principales
- **Programación Orientada a Objetos (POO):** Clases abstractas, herencia, encapsulamiento mediante propiedades (`@property` y setters) y polimorfismo en el cálculo de costos.
- **Excepciones personalizadas:** Manejo controlado de errores de validación de clientes, parámetros de servicios y estados de reservas (`try`, `except`, `else` y `finally`).
- **Registro de actividad (*logging*):** Trazabilidad de operaciones exitosas, advertencias y errores en un archivo de texto (`.log`), garantizando que la simulación complete las **10 operaciones** sin interrumpirse.
- **Persistencia sin base de datos:** Gestión en memoria durante la ejecución y registro histórico en archivo de *log*.

## Estructura del repositorio
- `reservas.py`: Implementación de la clase `Reserva` y la gestión de estados (`Pendiente`, `Confirmada`, `Cancelada`) con control de excepciones y *logging*.
- `main.py`: Definición de entidades y servicios, configuración de *logs* y ejecución de la simulación de las **10 operaciones**.
- `README.md`: Documentación general del proyecto, instrucciones de ejecución y aportes del equipo.
- *(Archivos base del proyecto según organización del equipo)*: `excepciones.py`, `logger.py` y `modelos.py`.

## Requisitos y ejecución
1. Tener instalado **Python 3.x**.
2. Clonar o descargar el repositorio y ubicarse en la carpeta del proyecto.
3. Ejecutar el punto de entrada principal desde la terminal:
   ```bash
   python main.py
   ```
## Participación y control de versiones
El trabajo colaborativo se gestionó mediante ramas y *Pull Requests* en GitHub:
- **Integrante:** Valerin Sabi Bravo — Implementación de `reservas.py` y `main.py`, actualización de `README.md` y aporte al informe en PDF.
- **Integrante Líder de equipo: Jennifer Jiménez** — Desarrollo de la estructura base del proyecto (excepciones.py, logger.py y modelos.py), integración de ramas en GitHub
- **Integrante:** **Camilo Andrés Ocampo Ortiz:** Corrección de constructores en `excepciones.py`, `logger.py` y `main.py`; ejecución y verificación de las cinco opciones del menú en Google Colab; integración de la gestión de clientes, servicios y reservas en el menú principal.
