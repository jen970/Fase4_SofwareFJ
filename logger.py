# +----------------------------------------------------------------------------+
#  MÓDULO DE AUDITORÍA Y REGISTRO DE LOGS - SISTEMA SOFTWARE FJ               
# Escritura y consulta de eventos informativos y errores en archivo plano    
# +----------------------------------------------------------------------------+

from datetime import datetime


class RegistradorLogs:
    """Administra el historial persistente en el archivo registro_sistema.log."""

    def _init_(self, nombre_archivo: str = "registro_sistema.log"):
        # Define el archivo donde se guardará el historial de auditoría
        self.nombre_archivo = nombre_archivo

    def registrar(self, nivel: str, mensaje: str) -> None:
        """Agrega una línea estructurada con fecha, hora, nivel y descripción."""
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nivel_limpio = nivel.strip().upper()
        linea = f"[{fecha_hora}] | {nivel_limpio:<5} | {mensaje}\n"

        try:
            # Abre el archivo en modo 'a' (append) para conservar registros anteriores
            with open(self.nombre_archivo, mode="a", encoding="utf-8") as archivo:
                archivo.write(linea)
        except OSError as error_io:
            # Protege el sistema si ocurre un fallo de permisos o disco
            print(f"[ADVERTENCIA] No se pudo escribir en el log: {error_io}")

    def leer_historial(self) -> list:
        """Lee y retorna todas las líneas almacenadas en el archivo de registro."""
        try:
            with open(self.nombre_archivo, mode="r", encoding="utf-8") as archivo:
                return archivo.readlines()
        except FileNotFoundError:
            return []
        except OSError as error_io:
            print(f"[ADVERTENCIA] Error al leer el archivo de log: {error_io}")
            return []