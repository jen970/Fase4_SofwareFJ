# Fase4_SofwareFJ

#programacion
#valerin_sabi

import logging  
from abc import ABC, abstractmethod
from datetime import datetime


# ==========================================
# 1. CONFIGURACIÓN DEL SISTEMA DE LOGS
# ==========================================
# Configura el archivo de texto donde se registrarán todos los eventos y errores del sistema

logging.basicConfig(
    filename="sistema_software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ==========================================
# 2. EXCEPCIONES PERSONALIZADAS
# ==========================================

class SoftwareFJError(Exception):
    """Clase base para las excepciones personalizadas de Software FJ."""

    pass


class ClienteInvalidoError(SoftwareFJError):
    """Excepción lanzada cuando los datos ingresados del cliente no son válidos."""

    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """Excepción lanzada cuando un servicio no existe o presenta parámetros inválidos."""

    pass


class ReservaFallidaError(SoftwareFJError):
    """Excepción lanzada cuando ocurre un error al procesar o confirmar una reserva."""

    pass

# ==========================================
# 3. CLASE ABSTRACTA BASE
# ==========================================

class EntidadSistema(ABC):
    """Clase abstracta general de la que heredarán las entidades principales del sistema."""

    def __init__(self, identificador: str):
        # Encapsulación del identificador único de la entidad
        self._identificador = identificador

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def obtener_detalles(self) -> str:
        """Método abstracto que obliga a las clases hijas a implementar su propia descripción."""
        pass
