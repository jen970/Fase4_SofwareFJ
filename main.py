# +--------------------------------------------------------------------+
# | MÓDULO PRINCIPAL DE EJECUCIÓN E INTERFAZ - SISTEMA SOFTWARE FJ     |
# | Punto de entrada del sistema, menú interactivo y pruebas de flujo  |
# +--------------------------------------------------------------------+

from excepciones import DatoInvalidoError, CalculoInconsistenteError
import gestor as gestor_
from gestión_reservas import Reserva
from modelos import Cliente, ReservaSala, AlquilerEquipo, AsesoriaEspecializada

def mostrar_menu() -> None:
    print("\n+---------------------------------------+")
    print("|       SISTEMA SOFTWARE FJ - FASE 4    |")
    print("+---------------------------------------+")
    print("| 1. Registrar nueva operación          |")
    print("| 2. Ver registros de la sesión actual  |")
    print("| 3. Ver historial completo (.log)      |")
    print("| 4. Ejecutar prueba de excepciones     |")
    print("| 5. Gestión de clientes y reservas     |")
    print("| 6. Salir del sistema                  |")
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

def gestionar_clientes_servicios_reservas(clientes, servicios, reservas) -> None:
    """Administra clientes, servicios y reservas del sistema."""

    while True:
        print("\n--- GESTIÓN DE CLIENTES Y RESERVAS ---")
        print("1. Registrar cliente")
        print("2. Registrar servicio")
        print("3. Crear reserva")
        print("4. Confirmar reserva")
        print("5. Cancelar reserva")
        print("6. Procesar reserva")
        print("7. Consultar reservas")
        print("8. Volver al menú principal")

        opcion = input("Seleccione una opción (1-8): ").strip()

        try:
            if opcion == "1":
                id_cliente = input("ID del cliente: ").strip()
                nombre = input("Nombre completo: ").strip()
                correo = input("Correo electrónico: ").strip()
                telefono = input("Teléfono: ").strip()

                if any(c.id_entidad == id_cliente for c in clientes):
                    print("[ERROR] Ya existe un cliente con ese ID.")
                    continue

                cliente = Cliente(id_cliente, nombre, correo, telefono)
                clientes.append(cliente)
                print("[OK] Cliente registrado.")
                print(cliente.generar_comprobante())

            elif opcion == "2":
                print("\nTipos de servicio:")
                print("1. Reserva de sala")
                print("2. Alquiler de equipo")
                print("3. Asesoría especializada")

                tipo = input("Seleccione el tipo: ").strip()
                id_servicio = input("ID del servicio: ").strip()
                nombre = input("Nombre del servicio: ").strip()
                tarifa = float(input("Tarifa por hora: "))

                if any(s.id_entidad == id_servicio for s in servicios):
                    print("[ERROR] Ya existe un servicio con ese ID.")
                    continue

                if tipo == "1":
                    capacidad = int(input("Capacidad de la sala: "))
                    servicio = ReservaSala(
                        id_servicio, nombre, tarifa, capacidad
                    )
                elif tipo == "2":
                    deposito = float(input("Depósito de seguridad: "))
                    servicio = AlquilerEquipo(
                        id_servicio, nombre, tarifa, deposito
                    )
                elif tipo == "3":
                    especialidad = input("Especialidad: ").strip()
                    servicio = AsesoriaEspecializada(
                        id_servicio, nombre, tarifa, especialidad
                    )
                else:
                    print("[ERROR] Tipo de servicio no válido.")
                    continue

                servicios.append(servicio)
                print("[OK] Servicio registrado.")
                print(servicio.generar_comprobante())

            elif opcion == "3":
                if not clientes or not servicios:
                    print("[ADVERTENCIA] Registre primero clientes y servicios.")
                    continue

                id_reserva = input("ID de la reserva: ").strip()
                id_cliente = input("ID del cliente: ").strip()
                id_servicio = input("ID del servicio: ").strip()
                horas = int(input("Cantidad de horas: "))

                cliente = next(
                    (c for c in clientes if c.id_entidad == id_cliente), None
                )
                servicio = next(
                    (s for s in servicios if s.id_entidad == id_servicio), None
                )

                if cliente is None or servicio is None:
                    print("[ERROR] Cliente o servicio no encontrado.")
                    continue

                if any(r._id_reserva == id_reserva for r in reservas):
                    print("[ERROR] Ya existe una reserva con ese ID.")
                    continue

                reserva = Reserva(id_reserva, cliente, servicio, horas)
                reservas.append(reserva)
                print("[OK] Reserva creada.")
                print(reserva.obtener_resumen())

            elif opcion in ("4", "5", "6"):
                id_reserva = input("ID de la reserva: ").strip()
                reserva = next(
                    (r for r in reservas if r._id_reserva == id_reserva), None
                )

                if reserva is None:
                    print("[ERROR] Reserva no encontrada.")
                    continue

                if opcion == "4":
                    reserva.confirmar()
                    print("[OK] Reserva confirmada.")
                elif opcion == "5":
                    reserva.cancelar()
                    print("[OK] Reserva cancelada.")
                else:
                    print(reserva.procesar())

            elif opcion == "7":
                if not reservas:
                    print("No hay reservas registradas.")
                else:
                    for reserva in reservas:
                        print(reserva.obtener_resumen())

            elif opcion == "8":
                break

            else:
                print("[ADVERTENCIA] Opción no válida.")

        except (ValueError, DatoInvalidoError, CalculoInconsistenteError) as error:
            print(f"[ERROR] No se pudo completar la operación: {error}")
        except Exception as error:
            print(f"[ERROR] Operación no completada: {error}")

def ejecutar() -> None:
    gestor = GestorSistema("registro_sistema.log")
    clientes = []
    servicios = []
    reservas = []

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-6): ").strip()

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
            gestionar_clientes_servicios_reservas(
                clientes, servicios, reservas
            )
            
        elif opcion == "6":
            print("\n[INFO] Cerrando Sistema Software FJ...")
            break
        else:
            print("\n[ADVERTENCIA] Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    ejecutar()
