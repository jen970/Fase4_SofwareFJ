# +----------------------------------------------------------------------------+
# | MÓDULO DE ENTIDADES Y MODELOS DE NEGOCIO - SISTEMA SOFTWARE FJ             |
# | Implementa Abstracción, Encapsulación, Herencia y Polimorfismo             |
# +----------------------------------------------------------------------------+

from abc import ABC, abstractmethod
from excepciones import DatoInvalidoError, CalculoInconsistenteError


class EntidadBase(ABC):
    """Clase abstracta deraíz que define el contrato obligatorio para toda entidad."""

    def __init__(self, id_entidad: str):
        if not id_entidad or not isinstance(id_entidad, str) or not id_entidad.strip():
            raise DatoInvalidoError("El identificador de la entidad debe ser un texto válido.")
        self._id_entidad = id_entidad.strip()

    @property
    def id_entidad(self) -> str:
        return self._id_entidad

    @abstractmethod
    def obtener_resumen(self) -> str:
        pass

    @abstractmethod
    def generar_comprobante(self) -> str:
        pass


class Cliente(EntidadBase):
    """Representa un cliente registrado, protegiendo sus datos mediante setters."""

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str = "No registrado"):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatoInvalidoError("El nombre del cliente debe contener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not valor or not isinstance(valor, str) or "@" not in valor or "." not in valor:
            raise DatoInvalidoError(f"El correo '{valor}' no tiene un formato válido.")
        self._correo = valor.strip()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 7:
            raise DatoInvalidoError("El teléfono debe tener al menos 7 dígitos.")
        self._telefono = valor.strip()

    def obtener_resumen(self) -> str:
        return f"Cliente [{self.id_entidad}] {self.nombre} ({self.correo})"

    def generar_comprobante(self) -> str:
        return (
            "+------------------------------------------------------+\n"
            "| FICHA DE CLIENTE - SOFTWARE FJ                       |\n"
            "+------------------------------------------------------+\n"
            f"| Código Cliente : {self.id_entidad:<35} |\n"
            f"| Nombre Completo: {self.nombre:<35} |\n"
            f"| Correo         : {self.correo:<35} |\n"
            f"| Teléfono       : {self.telefono:<35} |\n"
            "+------------------------------------------------------+"
        )


class Servicio(EntidadBase, ABC):
    """Clase abstracta base para los servicios especializados de Software FJ."""

    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base: float):
        super().__init__(id_servicio)
        self.validar_parametros_base(nombre_servicio, tarifa_base)
        self._nombre_servicio = nombre_servicio.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = True

    @staticmethod
    def validar_parametros_base(nombre: str, tarifa: float) -> None:
        if not nombre or not isinstance(nombre, str) or not nombre.strip():
            raise DatoInvalidoError("El nombre del servicio es obligatorio.")
        if not isinstance(tarifa, (int, float)) or tarifa <= 0:
            raise CalculoInconsistenteError("La tarifa base por hora debe ser mayor a cero.")

    @property
    def nombre_servicio(self) -> str:
        return self._nombre_servicio

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        if not isinstance(estado, bool):
            raise DatoInvalidoError("El estado de disponibilidad debe ser booleano.")
        self._disponible = estado

    @abstractmethod
    def calcular_costo(self, horas: int) -> float:
        pass


class ReservaSala(Servicio):
    """Servicio de alquiler de salas físicas con recargo del 10% por logística."""

    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base: float, capacidad: int):
        super().__init__(id_servicio, nombre_servicio, tarifa_base)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser un entero positivo.")
        self._capacidad = capacidad

    def calcular_costo(self, horas: int) -> float:
        if not isinstance(horas, int) or horas <= 0:
            raise CalculoInconsistenteError("La duración en horas debe ser mayor a cero.")
        return round((self._tarifa_base * horas) * 1.10, 2)

    def obtener_resumen(self) -> str:
        return f"Sala [{self.id_entidad}]: {self._nombre_servicio} (Capacidad: {self._capacidad} pers.)"

    def generar_comprobante(self) -> str:
        estado_txt = "DISPONIBLE" if self._disponible else "OCUPADA"
        tarifa_txt = f"${self._tarifa_base:,.2f}"
        cap_txt = f"{self._capacidad} personas"
        return (
            "+------------------------------------------------------+\n"
            "| DETALLE DE SERVICIO: RESERVA DE SALA                 |\n"
            "+------------------------------------------------------+\n"
            f"| Código         : {self.id_entidad:<35} |\n"
            f"| Sala           : {self._nombre_servicio:<35} |\n"
            f"| Capacidad      : {cap_txt:<35} |\n"
            f"| Tarifa / Hora  : {tarifa_txt:<35} |\n"
            "| Recargo Logíst.: 10% adicional                       |\n"
            f"| Estado Actual  : {estado_txt:<35} |\n"
            "+------------------------------------------------------+"
        )


class AlquilerEquipo(Servicio):
    """Servicio de préstamo de hardware con depósito fijo reembolsable."""

    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base: float, deposito_seguridad: float):
        super().__init__(id_servicio, nombre_servicio, tarifa_base)
        if not isinstance(deposito_seguridad, (int, float)) or deposito_seguridad < 0:
            raise CalculoInconsistenteError("El depósito de seguridad no puede ser negativo.")
        self._deposito = float(deposito_seguridad)

    def calcular_costo(self, horas: int) -> float:
        if not isinstance(horas, int) or horas <= 0:
            raise CalculoInconsistenteError("La duración en horas debe ser mayor a cero.")
        return round((self._tarifa_base * horas) + self._deposito, 2)

    def obtener_resumen(self) -> str:
        return f"Equipo [{self.id_entidad}]: {self._nombre_servicio} (Depósito: ${self._deposito:,.2f})"

    def generar_comprobante(self) -> str:
        estado_txt = "DISPONIBLE" if self._disponible else "ALQUILADO"
        tarifa_txt = f"${self._tarifa_base:,.2f}"
        dep_txt = f"${self._deposito:,.2f} (Reembolsable)"
        return (
            "+------------------------------------------------------+\n"
            "| DETALLE DE SERVICIO: ALQUILER DE EQUIPO              |\n"
            "+------------------------------------------------------+\n"
            f"| Código         : {self.id_entidad:<35} |\n"
            f"| Equipo         : {self._nombre_servicio:<35} |\n"
            f"| Tarifa / Hora  : {tarifa_txt:<35} |\n"
            f"| Depósito Seg.  : {dep_txt:<35} |\n"
            f"| Estado Actual  : {estado_txt:<35} |\n"
            "+------------------------------------------------------+"
        )


class AsesoriaEspecializada(Servicio):
    """Servicio de consultoría técnica con descuento del 15% desde 5 horas."""

    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base: float, especialidad: str):
        super().__init__(id_servicio, nombre_servicio, tarifa_base)
        if not especialidad or not isinstance(especialidad, str) or not especialidad.strip():
            raise DatoInvalidoError("Debe indicar el área de especialidad de la asesoría.")
        self._especialidad = especialidad.strip()

    def calcular_costo(self, horas: int) -> float:
        if not isinstance(horas, int) or horas <= 0:
            raise CalculoInconsistenteError("La duración en horas debe ser mayor a cero.")
        subtotal = self._tarifa_base * horas
        if horas >= 5:
            subtotal *= 0.85
        return round(subtotal, 2)

    def obtener_resumen(self) -> str:
        return f"Asesoría [{self.id_entidad}]: {self._nombre_servicio} (Área: {self._especialidad})"

    def generar_comprobante(self) -> str:
        estado_txt = "DISPONIBLE" if self._disponible else "ASIGNADA"
        tarifa_txt = f"${self._tarifa_base:,.2f}"
        return (
            "+------------------------------------------------------+\n"
            "| DETALLE DE SERVICIO: ASESORÍA ESPECIALIZADA          |\n"
            "+------------------------------------------------------+\n"
            f"| Código         : {self.id_entidad:<35} |\n"
            f"| Servicio       : {self._nombre_servicio:<35} |\n"
            f"| Especialidad   : {self._especialidad:<35} |\n"
            f"| Tarifa / Hora  : {tarifa_txt:<35} |\n"
            "| Beneficio      : 15% dto. desde 5 horas              |\n"
            f"| Estado Actual  : {estado_txt:<35} |\n"
            "+------------------------------------------------------+"
        )


if __name__ == "__main__":
    # Ejemplo de uso y prueba de las clases
    try:
        cliente = Cliente("C001", "Ana Pérez", "ana.perez@email.com")
        print(cliente.obtener_resumen())
    except Exception as e:
        print(f"Error: {e}")