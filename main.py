import logging
from abc import ABC, abstractmethod

# ==========================================
# 1. CONFIGURACIÓN DEL ARCHIVO DE LOGS
# ==========================================
logging.basicConfig(
    filename="sistema_software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# ==========================================
# 2. EXCEPCIONES PERSONALIZADAS
# ==========================================
class ErrorSistemaFJ(Exception):
    """Excepción base del sistema Software FJ."""
    pass


class ClienteInvalidoError(ErrorSistemaFJ):
    """Error lanzado cuando los datos del cliente no son válidos."""
    pass


class ParametroServicioError(ErrorSistemaFJ):
    """Error lanzado cuando un servicio tiene datos o cálculos inválidos."""
    pass


# ==========================================
# 3. IMPORTACIÓN O RESPALDO DE RESERVA
# ==========================================
try:
    from reservas import Reserva, ReservaError
except ImportError:
    class ReservaError(ErrorSistemaFJ):
        """Error lanzado cuando ocurre un fallo en la reserva."""
        pass

    class Reserva:
        """Representa una reserva con estado y manejo de excepciones."""

        def __init__(self, cliente, servicio, duracion: int):
            if cliente is None or servicio is None:
                raise ReservaError("La reserva requiere un cliente y un servicio.")
            if not isinstance(duracion, int) or duracion <= 0:
                raise ReservaError("La duración debe ser un número entero mayor a 0.")
            self.cliente = cliente
            self.servicio = servicio
            self.duracion = duracion
            self.estado = "Pendiente"

        def confirmar(self) -> None:
            try:
                if self.estado == "Cancelada":
                    raise ReservaError("No se puede confirmar una reserva cancelada.")
                self.estado = "Confirmada"
            except ReservaError as err:
                logging.error(f"Fallo al confirmar reserva: {err}")
                raise
            else:
                logging.info(
                    f"Reserva confirmada para {self.cliente.nombre} en '{self.servicio.nombre}'."
                )
            finally:
                logging.info(f"Estado tras confirmar: {self.estado}")

        def cancelar(self) -> None:
            try:
                if self.estado == "Cancelada":
                    raise ReservaError("La reserva ya estaba cancelada.")
                self.estado = "Cancelada"
            except ReservaError as err:
                logging.warning(f"Intento de cancelar reserva ya cancelada: {err}")
                raise
            else:
                logging.info(f"Reserva cancelada para {self.cliente.nombre}.")


# ==========================================
# 4. ENTIDADES: CLIENTE Y SERVICIOS
# ==========================================
class EntidadBase(ABC):
    """Clase abstracta general del sistema."""

    def __init__(self, codigo: str):
        if not codigo or not str(codigo).strip():
            raise ValueError("El código de la entidad es obligatorio.")
        self._codigo = str(codigo).strip()

    @property
    def codigo(self) -> str:
        return self._codigo

    @abstractmethod
    def describir(self) -> str:
        pass


class Cliente(EntidadBase):
    """Cliente con datos encapsulados y validaciones estrictas."""

    def __init__(self, codigo: str, nombre: str, correo: str):
        super().__init__(codigo)
        self.nombre = nombre
        self.correo = correo

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not isinstance(valor, str) or "@" not in valor or "." not in valor.split("@")[-1]:
            raise ClienteInvalidoError("El correo electrónico no tiene un formato válido.")
        self._correo = valor.strip()

    def describir(self) -> str:
        return f"Cliente [{self.codigo}] - {self.nombre} ({self.correo})"


class Servicio(EntidadBase, ABC):
    """Clase abstracta para los servicios ofrecidos por Software FJ."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float):
        super().__init__(codigo)
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise ParametroServicioError("La tarifa base debe ser mayor que 0.")
        self.nombre = nombre
        self.tarifa_base = float(tarifa_base)

    @abstractmethod
    def calcular_costo(self) -> float:
        pass

    def calcular_costo_final(self, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        if not (0.0 <= descuento < 1.0):
            raise ParametroServicioError("El descuento debe estar entre 0.0 y menor a 1.0.")
        if impuesto < 0.0:
            raise ParametroServicioError("El impuesto no puede ser negativo.")
        subtotal = self.calcular_costo() * (1.0 - descuento)
        return round(subtotal * (1.0 + impuesto), 2)


class ReservaSala(Servicio):
    def __init__(self, codigo: str, tarifa_base: float, capacidad: int):
        super().__init__(codigo, "Reserva de Sala", tarifa_base)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ParametroServicioError("La capacidad de la sala debe ser mayor que 0.")
        self.capacidad = capacidad

    def calcular_costo(self) -> float:
        return round(self.tarifa_base * 1.05, 2)

    def describir(self) -> str:
        return f"{self.nombre} [{self.codigo}] - Capacidad: {self.capacidad} personas"


class AlquilerEquipo(Servicio):
    def __init__(self, codigo: str, tarifa_base: float, unidades: int):
        super().__init__(codigo, "Alquiler de Equipo", tarifa_base)
        if not isinstance(unidades, int) or unidades <= 0:
            raise ParametroServicioError("La cantidad de equipos debe ser mayor que 0.")
        self.unidades = unidades

    def calcular_costo(self) -> float:
        return round(self.tarifa_base * self.unidades, 2)

    def describir(self) -> str:
        return f"{self.nombre} [{self.codigo}] - Unidades: {self.unidades}"


class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo: str, tarifa_base: float, horas: int):
        super().__init__(codigo, "Asesoría Especializada", tarifa_base)
        if not isinstance(horas, int) or horas <= 0:
            raise ParametroServicioError("Las horas de asesoría deben ser mayores que 0.")
        self.horas = horas

    def calcular_costo(self) -> float:
        return round(self.tarifa_base * self.horas, 2)

    def describir(self) -> str:
        return f"{self.nombre} [{self.codigo}] - Horas: {self.horas}"


# ==========================================
# 5. SIMULACIÓN DE LAS 10 OPERACIONES
# ==========================================
def ejecutar_simulacion():
    """Ejecuta 10 operaciones (válidas e inválidas) sin detener la aplicación."""
    clientes = []
    servicios = []
    reservas = []
    total_operaciones = 0

    print("=== SIMULACIÓN SOFTWARE FJ (10 OPERACIONES) ===\n")
    logging.info("Inicio de simulación de 10 operaciones en Software FJ.")

    # 1. Registro válido de cliente
    total_operaciones += 1
    try:
        c1 = Cliente("CL-01", "Laura Gómez", "laura.gomez@correo.com")
        clientes.append(c1)
        print(f"1. [OK] Cliente registrado: {c1.describir()}")
        logging.info(f"Op 1 OK: {c1.describir()}")
    except Exception as e:
        print(f"1. [ERROR] {e}")
        logging.error(f"Op 1 error: {e}")

    # 2. Registro inválido de cliente
    total_operaciones += 1
    try:
        c_inv = Cliente("CL-02", "Andrés Ruiz", "correo_invalido")
        clientes.append(c_inv)
    except ClienteInvalidoError as e:
        print(f"2. [CONTROLADO] Registro de cliente rechazado: {e}")
        logging.warning(f"Op 2 controlada: {e}")

    # 3. Creación correcta de servicio de sala
    total_operaciones += 1
    try:
        s_sala = ReservaSala("SR-01", 80000.0, 12)
        servicios.append(s_sala)
        print(f"3. [OK] Servicio creado: {s_sala.describir()} | Costo: ${s_sala.calcular_costo()}")
        logging.info(f"Op 3 OK: {s_sala.describir()}")
    except Exception as e:
        print(f"3. [ERROR] {e}")
        logging.error(f"Op 3 error: {e}")

    # 4. Creación correcta de servicio de alquiler de equipos
    total_operaciones += 1
    try:
        s_eq = AlquilerEquipo("EQ-01", 35000.0, 3)
        servicios.append(s_eq)
        print(f"4. [OK] Servicio creado: {s_eq.describir()} | Costo: ${s_eq.calcular_costo()}")
        logging.info(f"Op 4 OK: {s_eq.describir()}")
    except Exception as e:
        print(f"4. [ERROR] {e}")
        logging.error(f"Op 4 error: {e}")

    # 5. Creación incorrecta de servicio
    total_operaciones += 1
    try:
        s_malo = AsesoriaEspecializada("AS-01", 60000.0, -2)
        servicios.append(s_malo)
    except ParametroServicioError as e:
        print(f"5. [CONTROLADO] Creación de servicio rechazada: {e}")
        logging.warning(f"Op 5 controlada: {e}")

    # 6. Creación de asesoría válida
    total_operaciones += 1
    try:
        s_ase = AsesoriaEspecializada("AS-02", 60000.0, 2)
        servicios.append(s_ase)
        print(f"6. [OK] Servicio creado: {s_ase.describir()} | Costo final (IVA): ${s_ase.calcular_costo_final()}")
        logging.info(f"Op 6 OK: {s_ase.describir()}")
    except Exception as e:
        print(f"6. [ERROR] {e}")
        logging.error(f"Op 6 error: {e}")

    # 7. Reserva exitosa
    total_operaciones += 1
    try:
        r1 = Reserva(clientes[0], servicios[0], 2)
        r1.confirmar()
        reservas.append(r1)
        print(f"7. [OK] Reserva confirmada para {r1.cliente.nombre} ({r1.estado})")
    except Exception as e:
        print(f"7. [ERROR] {e}")
        logging.error(f"Op 7 error: {e}")

    # 8. Reserva fallida por duración inválida
    total_operaciones += 1
    try:
        r_fallida = Reserva(clientes[0], servicios[1], 0)
        r_fallida.confirmar()
    except ReservaError as e:
        print(f"8. [CONTROLADO] Reserva rechazada: {e}")
        logging.warning(f"Op 8 controlada: {e}")

    # 9. Cálculo de costo con descuento inválido
    total_operaciones += 1
    try:
        precio_err = servicios[0].calcular_costo_final(descuento=1.5)
        print(f"9. Costo calculado: {precio_err}")
    except ParametroServicioError as e:
        print(f"9. [CONTROLADO] Cálculo rechazado: {e}")
        logging.warning(f"Op 9 controlada: {e}")

    # 10. Cancelación de reserva existente
    total_operaciones += 1
    try:
        if reservas:
            reservas[0].cancelar()
            print(f"10. [OK] Reserva cancelada. Estado actual: {reservas[0].estado}")
        else:
            raise ReservaError("No hay reservas registradas para cancelar.")
    except ReservaError as e:
        print(f"10. [CONTROLADO] Cancelación no realizada: {e}")
        logging.warning(f"Op 10 controlada: {e}")

    print(f"\n=== FIN DE LA SIMULACIÓN: {total_operaciones}/10 OPERACIONES EJECUTADAS ===")
    logging.info("Simulación finalizada sin interrupciones.")


if __name__ == "__main__":
    ejecutar_simulacion()
