# +--------------------------------------------------------------------+
# | MÓDULO PRINCIPAL DE EJECUCIÓN E INTERFAZ - SISTEMA SOFTWARE FJ     |
# | Punto de entrada del sistema, menú interactivo y pruebas de flujo  |
# +--------------------------------------------------------------------+

from excepciones import DatoInvalidoError, CalculoInconsistenteError
import gestor as gestor_


def mostrar_menu() -> None:
    print("\n+---------------------------------------+")
    print("|       SISTEMA SOFTWARE FJ - FASE 4    |")
    print("+---------------------------------------+")
    print("| 1. Registrar nueva operación          |")
    print("| 2. Ver registros de la sesión actual  |")
    print("| 3. Ver historial completo (.log)      |")
    print("| 4. Ejecutar prueba de excepciones     |")
    print("| 5. Salir del sistema                  |")
    print("+---------------------------------------+")


class GestorSistema(gestor_.GestorSistema):
    """Implementación concreta del gestor utilizado por la interfaz."""

    def __init__(self, archivo_log: str) -> None:
        super().__init__(archivo_log)
        self.archivo_log = archivo_log
        self._registros = []

    def registrar_elemento(self, elemento) -> None:
        self._registros.append(elemento)
        try:
            with open(self.archivo_log, "a", encoding="utf-8") as archivo:
                archivo.write(f"{elemento}\n")
        except OSError as error:
            raise CalculoInconsistenteError(
                f"No fue posible escribir en el registro: {error}"
            )

    def obtener_todos(self) -> list:
        return list(self._registros)

    def leer_historial_log(self) -> list:
        try:
            with open(self.archivo_log, "r", encoding="utf-8") as archivo:
                return archivo.readlines()
        except FileNotFoundError:
            return []
        except OSError as error:
            raise CalculoInconsistenteError(
                f"No fue posible leer el historial: {error}"
            )


def ejecutar() -> None:
    gestor = GestorSistema("registro_sistema.log")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-5): ").strip()

        if opcion == "1":
            try:
                id_op = input("Ingrese ID (ej. OP-10654256731):")

                desc = input("Ingrese descripción: ")
                monto = float(input("Ingrese valor numérico: "))

                nueva_op = gestor_.RegistroOperacion(id_op, desc, monto)
                gestor.registrar_elemento(nueva_op)
                print("\n[INFO] Operación registrada con éxito:")
                print(nueva_op.generar_comprobante())

            except ValueError:
                print("\n[ERROR] El valor numérico ingresado no es válido.")
            except (DatoInvalidoError, CalculoInconsistenteError) as error:
                print(f"\n[ERROR DE LA VALIDACIÓN] {error}")
            
        elif opcion == "2":
            registros = gestor.obtener_todos()
            print("\n--- REGISTROS EN MEMORIA ---")
            if not registros:
                print("No hay registros almacenados en esta sesión.")
            else:
                for item in registros:
                    print(f" * {item}")

        elif opcion == "3":
            print("\n--- HISTORIAL DE AUDITORÍA (.LOG) ---")
            lineas = gestor.leer_historial_log()
            if not lineas:
                print("El archivo de registro está vacío.")
            else:
                for linea in lineas:
                    print(linea.strip())

        elif opcion == "4":
            print("\n--- VERIFICACIÓN DE EXCEPCIONES DEL SISTEMA ---")
            try:
                gestor_.RegistroOperacion("", "Prueba de identificador vacío", 100)
            except DatoInvalidoError as error:
                print(f"[OK] DatoInvalidoError capturado: {error}")

            try:
                gestor_.RegistroOperacion("OP-999", "Prueba de monto negativo", -50)
            except CalculoInconsistenteError as error:
                print(f"[OK] CalculoInconsistenteError capturado: {error}")

        elif opcion == "5":
            print("\n[INFO] Cerrando Sistema Software FJ...")
            break
        else:
            print("\n[ADVERTENCIA] Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    ejecutar()
