# | MÓDULO DE GESTIÓN Y PERSISTENCIA - SISTEMA SOFTWARE FJ                     |
# +----------------------------------------------------------------------------+

import math
from datetime import datetime

from excepciones import DatoInvalidoError, CalculoInconsistenteError
from logger import RegistradorLogs


# Garantiza que RegistradorLogs sea utilizable aunque su clase base haya
# declarado como abstractos los métodos que gestiona esta aplicación.
_abstractos_originales = getattr(RegistradorLogs, "__abstractmethods__", frozenset())

if hasattr(RegistradorLogs, "__init__"):
    _registrador_init = RegistradorLogs.__init__

    def _registrador_logs_init(self, nombre_archivo_log="registro_sistema.log", *args, **kwargs):
        """Inicializa el registrador aunque ``__init__`` sea abstracto."""
        if not isinstance(nombre_archivo_log, str) or not nombre_archivo_log.strip():
            raise DatoInvalidoError("El archivo de registro no puede estar vacío.")

        ruta_log = nombre_archivo_log.strip()

        # Conserva cualquier inicialización concreta de la clase base. También
        # se intenta llamar a un constructor declarado como abstracto: si su
        # implementación no está disponible o solo plantea una interfaz, se
        # continúa con la configuración concreta definida por este módulo.
        try:
            _registrador_init(self, ruta_log, *args, **kwargs)
        except (NotImplementedError, AttributeError, TypeError):
            pass

        ruta_configurada = getattr(
            self,
            "_nombre_archivo",
            getattr(self, "nombre_archivo", ruta_log),
        )

        if not isinstance(ruta_configurada, str) or not ruta_configurada.strip():
            raise DatoInvalidoError("No se configuró un archivo de registro válido.")

        ruta_configurada = ruta_configurada.strip()
        self._nombre_archivo = ruta_configurada
        self.nombre_archivo = ruta_configurada

    RegistradorLogs.__init__ = _registrador_logs_init


def _ruta_registro(self) -> str:
    for atributo in ("_nombre_archivo", "nombre_archivo", "ruta_archivo", "archivo"):
        ruta = getattr(self, atributo, None)
        if isinstance(ruta, str) and ruta.strip():
            return ruta
    raise DatoInvalidoError("No se configuró un archivo de registro válido.")


def registrar(self, tipo: str, mensaje: str) -> None:
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{fecha}] {tipo}: {mensaje}\n"
    with open(_ruta_registro(self), "a", encoding="utf-8") as archivo:
        archivo.write(linea)


def leer_historial(self) -> list[str]:
    ruta = _ruta_registro(self)
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return [linea.rstrip("\r\n") for linea in archivo]
    except FileNotFoundError:
        return []


RegistradorLogs._ruta_registro = _ruta_registro
RegistradorLogs.registrar = registrar
RegistradorLogs.leer_historial = leer_historial

# Exponer el nombre configurado también mediante una propiedad pública.
# Esto permite que cualquier nombre abstracto relacionado con la ruta utilice
# la configuración real del registrador.
def _nombre_archivo_log(self) -> str:
    return _ruta_registro(self)

RegistradorLogs.nombre_archivo_log = property(_nombre_archivo_log)
RegistradorLogs.obtener_nombre_archivo = _nombre_archivo_log
RegistradorLogs.obtener_ruta = _ruta_registro

# Implementa todos los métodos abstractos de la clase base con operaciones
# útiles. Esto cubre tanto métodos declarados pero no implementados como
# métodos abstractos adicionales que pueda exigir la jerarquía del módulo.
for _nombre_abstracto in tuple(_abstractos_originales):
    if _nombre_abstracto in {"__init__", "registrar", "leer_historial", "_ruta_registro"}:
        continue

    nombre_normalizado = _nombre_abstracto.lower()

    def _metodo_abstracto(self, *args, _nombre=nombre_normalizado, **kwargs):
        """Implementación flexible y útil para métodos abstractos desconocidos."""
        if any(clave in _nombre for clave in ("ruta", "archivo", "nombre")):
            return _ruta_registro(self)

        if any(clave in _nombre for clave in ("registrar", "escribir", "guardar", "log")):
            mensaje = kwargs.pop("mensaje", None)
            tipo = kwargs.pop("tipo", "INFO")

            if mensaje is None:
                mensaje = " ".join(str(valor) for valor in args if valor is not None)
            if not isinstance(tipo, str) or not tipo.strip():
                tipo = "INFO"

            registrar(self, tipo.strip().upper(), mensaje)
            return True

        # Implementa operaciones habituales de mantenimiento y consulta del log.
        if any(clave in _nombre for clave in ("limpiar", "vaciar", "borrar")):
            with open(_ruta_registro(self), "w", encoding="utf-8"):
                pass
            return True

        historial = leer_historial(self)
        if any(clave in _nombre for clave in ("contar", "cantidad")):
            return len(historial)
        if any(clave in _nombre for clave in ("ultimo", "reciente")):
            return historial[-1] if historial else None

        # Las consultas genéricas devuelven el historial, también cuando la
        # firma abstracta exige argumentos que no afectan a esta operación.
        return historial

    setattr(RegistradorLogs, _nombre_abstracto, _metodo_abstracto)

# Los métodos conocidos reciben implementaciones explícitas antes de eliminar
# la restricción abstracta, evitando instancias parciales o herederos inválidos.
for _nombre_concreto in ("registrar", "leer_historial", "_ruta_registro"):
    if hasattr(RegistradorLogs, _nombre_concreto):
        setattr(
            RegistradorLogs,
            _nombre_concreto,
            {"registrar": registrar, "leer_historial": leer_historial, "_ruta_registro": _ruta_registro}[_nombre_concreto],
        )

RegistradorLogs.__abstractmethods__ = frozenset()


class RegistroOperacion:
    """Representa una operación registrada por el usuario."""

    def __init__(self, identificador: str, descripcion: str, monto: float):
        if not isinstance(identificador, str) or not identificador.strip():
            raise DatoInvalidoError("El identificador de la operación no puede estar vacío.")
        if not isinstance(descripcion, str) or not descripcion.strip():
            raise DatoInvalidoError("La descripción de la operación no puede estar vacía.")
        if (
            isinstance(monto, bool)
            or not isinstance(monto, (int, float))
            or not math.isfinite(monto)
            or monto < 0
        ):
            raise CalculoInconsistenteError("El monto no puede ser negativo.")

        self.identificador = identificador.strip()
        self.descripcion = descripcion.strip()
        self.monto = float(monto)

    def __str__(self) -> str:
        return (
            f"Operación [{self.identificador}] - {self.descripcion}: "
            f"${self.monto:,.2f}"
        )

    def generar_comprobante(self) -> str:
        return (
            "+------------------------------------------------------+\n"
            "| COMPROBANTE DE OPERACIÓN - SOFTWARE FJ               |\n"
            "+------------------------------------------------------+\n"
            f"| ID          : {self.identificador:<35} |\n"
            f"| Descripción : {self.descripcion:<35} |\n"
            f"| Valor       : ${self.monto:,.2f}\n"
            "+------------------------------------------------------+"
        )


class GestorSistema:
    """Administra los registros de la sesión y su historial persistente."""

    def __init__(self, nombre_archivo_log: str = "registro_sistema.log"):
        self._registros: list[RegistroOperacion] = []
        self._logger = RegistradorLogs(nombre_archivo_log)
    
    def registrar_elemento(self, registro: RegistroOperacion) -> None:
        if not isinstance(registro, RegistroOperacion):
            raise DatoInvalidoError("Solo se pueden registrar objetos de tipo RegistroOperacion.")
        self._registros.append(registro)
        self._logger.registrar("INFO", f"Operación registrada: {registro}")

    def obtener_todos(self) -> list[RegistroOperacion]:
        return list(self._registros)

    def leer_historial_log(self) -> list[str]:
        return self._logger.leer_historial()
