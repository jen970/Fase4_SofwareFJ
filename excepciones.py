 #+----------------------------------------------------------------------------+
# | MÓDULO DE EXCEPCIONES PERSONALIZADAS - SISTEMA SOFTWARE FJ                 |
# | Define la jerarquía de errores propios del negocio para evitar cierres     |
# | inesperados y controlar fallos de validación, disponibilidad y cálculos.   |
# +----------------------------------------------------------------------------+


class ErrorSistemaFJ(Exception):
    """
    Excepción base de la aplicación Software FJ.
    Hereda de la clase nativa Exception de Python para permitir capturar
    cualquier error propio del sistema de forma centralizada.
    """

    def _init_(self, mensaje: str, codigo_error: str = "ERR-000"):
        # Llama al constructor de la clase Exception con el mensaje descriptivo
        super()._init_(mensaje)
        # Almacena un código identificador único para clasificar el fallo en el log
        self.codigo_error = codigo_error
        # Guarda el texto explicativo del error
        self.mensaje = mensaje

    def _str_(self) -> str:
        # Define cómo se mostrará el error al imprimirlo en consola o guardarlo en el log
        return f"[{self.codigo_error}] {self.mensaje}"


class DatoInvalidoError(ErrorSistemaFJ):
    """
    Excepción lanzada cuando un dato ingresado por el usuario o el sistema
    está vacío, es nulo o no cumple con el formato requerido (ej. correo sin '@').
    """

    def _init_(self, mensaje: str):
        # Inicializa la excepción padre asignando el código específico de datos inválidos
        super()._init_(mensaje, codigo_error="ERR-DATO-001")


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """
    Excepción lanzada cuando se intenta confirmar una reserva sobre una sala,
    equipo o asesoría que ya se encuentra ocupada o inactiva.
    """

    def _init_(self, mensaje: str):
        # Inicializa la excepción padre asignando el código de conflicto de disponibilidad
        super()._init_(mensaje, codigo_error="ERR-DISP-002")


class ReservaInvalidaError(ErrorSistemaFJ):
    """
    Excepción lanzada cuando se intenta ejecutar una transición de estado no
    permitida en una reserva (por ejemplo, cancelar una reserva ya cancelada).
    """

    def _init_(self, mensaje: str):
        # Inicializa la excepción padre asignando el código de operación de reserva inválida
        super()._init_(mensaje, codigo_error="ERR-RES-003")


class CalculoInconsistenteError(ErrorSistemaFJ):
    """
    Excepción lanzada cuando los valores numéricos involucrados en el cálculo
    de tarifas, duración en horas o porcentajes de descuento son negativos o nulos.
    """

    def _init_(self, mensaje: str):
        # Inicializa la excepción padre asignando el código de inconsistencia matemática
        super()._init_(mensaje, codigo_error="ERR-CALC-004")


# Bloque de ejecución directa para comprobar el funcionamiento de las excepciones
if __name__ == "__main__":
    print("=== VERIFICACIÓN DEL MÓDULO DE EXCEPCIONES ===")
    try:
        # Se fuerza el lanzamiento de una excepción personalizada para probar su captura
        raise DatoInvalidoError("Prueba de validación: el correo ingresado no es válido.")
    except ErrorSistemaFJ as error_capturado:
        # Se imprime el mensaje formateado con su código de error
        print(f"Controlado correctamente -> {error_capturado}")