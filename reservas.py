import logging


class ReservaError(Exception):
    """Excepción personalizada para errores en reservas."""
    pass


class Reserva:
    """Representa una reserva de servicio realizada por un cliente."""

    def __init__(self, cliente, servicio, duracion: int):
        # Valida parámetros básicos al crear la reserva
        if cliente is None or servicio is None:
            raise ReservaError("La reserva requiere un cliente y un servicio válidos.")
        if not isinstance(duracion, int) or duracion <= 0:
            raise ReservaError("La duración de la reserva debe ser un entero mayor que 0.")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self) -> None:
        """Confirma la reserva aplicando bloques try/except/else/finally."""
        try:
            if self.estado == "Cancelada":
                raise ReservaError("No se puede confirmar una reserva cancelada.")
            self.estado = "Confirmada"
        except ReservaError as error:
            logging.error(f"Error al confirmar reserva: {error}")
            raise
        else:
            logging.info(
                f"Reserva confirmada para {self.cliente} en '{self.servicio}' ({self.duracion} unidad/es)."
            )
        finally:
            logging.info(f"Estado final tras intento de confirmación: {self.estado}")

    def cancelar(self) -> None:
        """Cancela una reserva activa o pendiente."""
        try:
            if self.estado == "Cancelada":
                raise ReservaError("La reserva ya se encuentra cancelada.")
            self.estado = "Cancelada"
        except ReservaError as error:
            logging.warning(f"Intento de cancelar reserva ya cancelada: {error}")
            raise
        else:
            logging.info(f"Reserva cancelada para {self.cliente}.")
