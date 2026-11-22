
# +--------------------------------------------------------------------+
# | MÓDULO DE GESTIÓN DE RESERVAS - SISTEMA SOFTWARE FJ                |
# | Administración y control del estado de las reservas               |
# +--------------------------------------------------------------------+

from modelos import Cliente, Servicio
from logger import RegistradorLogs
from excepciones import (
    DatoInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    CalculoInconsistenteError
)


class Reserva:
    """Representa una reserva de un servicio solicitado por un cliente."""

    def __init__(self, id_reserva: str, cliente: Cliente,
                 servicio: Servicio, horas: int):

        if not isinstance(id_reserva, str) or not id_reserva.strip():
            raise DatoInvalidoError(
                "El identificador de la reserva no puede estar vacío."
            )

        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError(
                "La reserva debe estar asociada a un cliente válido."
            )

        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError(
                "La reserva debe tener un servicio válido."
            )

        if isinstance(horas, bool) or not isinstance(horas, int) or horas <= 0:
            raise CalculoInconsistenteError(
                "Las horas de reserva deben ser un entero positivo."
            )

        self._id_reserva = id_reserva.strip()
        self._logger = RegistradorLogs()
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = "Pendiente"
        self._costo = servicio.calcular_costo(horas)

    @property
    def estado(self) -> str:
        return self._estado

    def confirmar(self) -> None:
        #Registra los errores que pueden ocurrir al confirmar una reserva.
        try:
            if self._estado != "Pendiente":
                raise ReservaInvalidaError(
                    "Solo se pueden confirmar reservas pendientes."
                )

            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(
                    "El servicio seleccionado no está disponible."
                )

            self._servicio.disponible = False
            self._estado = "Confirmada"

            self._logger.registrar(
                "INFO",
                f"Reserva {self._id_reserva} confirmada para {self._cliente.nombre}."
            )

        except (ReservaInvalidaError, ServicioNoDisponibleError) as error:
            self._logger.registrar(
                "ERROR",
                f"Error al confirmar reserva {self._id_reserva}: {error}"
            )
            raise
            
    def cancelar(self) -> None:
        # Controla y registra los errores durante la cancelación.
        try:
            if self._estado == "Cancelada":
                raise ReservaInvalidaError(
                    "La reserva ya se encuentra cancelada."
                )

            if self._estado == "Confirmada":
                self._servicio.disponible = True

            self._estado = "Cancelada"

            self._logger.registrar(
                "INFO",
                f"Reserva {self._id_reserva} cancelada para {self._cliente.nombre}."
            )

        except ReservaInvalidaError as error:
            self._logger.registrar(
                "ERROR",
                f"Error al cancelar reserva {self._id_reserva}: {error}"
            )
            raise        

    def procesar(self) -> str:
        # Procesa una reserva que ya ha sido confirmada.
        try:
            if self._estado != "Confirmada":
                raise ReservaInvalidaError(
                    "Solo se pueden procesar reservas confirmadas."
                )

        except ReservaInvalidaError as error:
            self._logger.registrar(
                "ERROR",
                f"Error al procesar reserva {self._id_reserva}: {error}"
            )
            raise

        else:
            self._logger.registrar(
                "INFO",
                f"Reserva {self._id_reserva} procesada correctamente."
            )
            return self.generar_comprobante()

        finally:
            self._logger.registrar(
                "INFO",
                f"Finalizó el intento de procesamiento de reserva {self._id_reserva}."
            )
            
    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self._id_reserva}] - "
            f"Cliente: {self._cliente.nombre} - "
            f"Servicio: {self._servicio.nombre_servicio} - "
            f"Estado: {self._estado}"
        )
        
    def generar_comprobante(self) -> str:
        return (
            "+------------------------------------------------------+\n"
            "|          COMPROBANTE DE RESERVA - SOFTWARE FJ        |\n"
            "+------------------------------------------------------+\n"
            f"| Reserva       : {self._id_reserva:<35} |\n"
            f"| Cliente       : {self._cliente.nombre:<35} |\n"
            f"| Servicio      : {self._servicio.nombre_servicio:<35} |\n"
            f"| Duración      : {self._horas} horas{'':<28} |\n"
            f"| Estado        : {self._estado:<35} |\n"
            f"| Costo total   : ${self._costo:,.2f}{'':<25} |\n"
            "+------------------------------------------------------+"
        )
# Proyecto Fase 4 -Software FJ
