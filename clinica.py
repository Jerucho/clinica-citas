"""
Sistema de gestión de citas para una clínica pequeña.
Programación 2 (UPC) - Grupo 6.

Ejecutar:  python3 clinica.py

PUNTAPIÉ INICIAL: las clases y la estructura están definidas. Cada método tiene un
TODO con su tarjeta de Trello, responsable y las reglas de negocio que debe cumplir.
Reglas (RN-xx) y requerimientos (RF-xx): ver docs/ del grupo.

Cómo trabajar:
  1. Una rama por tarjeta:  git checkout -b c2-pacientes
  2. Implementar solo tus métodos (quita el `raise NotImplementedError`).
  3. Probar con:  python3 clinica.py
  4. Subir la rama, avisar en el grupo y mover la tarjeta en Trello.
"""
from datetime import datetime

FORMATO = "%Y-%m-%d %H:%M"  # formato de fecha y hora: 2026-11-20 09:30


def fmt(fecha_hora):
    """Devuelve la fecha y hora como texto legible."""
    return fecha_hora.strftime(FORMATO)


# =====================================================================
# MODELOS (ya definidos: no cambiar atributos sin avisar al grupo)
# =====================================================================
class Paciente:
    def __init__(self, dni, nombre, telefono=""):
        self.dni = dni
        self.nombre = nombre
        self.telefono = telefono
        self.historial = []  # lista de Cita atendidas

    def __str__(self):
        return f"{self.dni} | {self.nombre} | tel: {self.telefono or '-'}"


class Medico:
    def __init__(self, id_medico, nombre, especialidad):
        self.id = id_medico
        self.nombre = nombre
        self.especialidad = especialidad
        self.horarios = []  # lista de datetime en los que el médico atiende

    def __str__(self):
        return f"[{self.id}] Dr(a). {self.nombre} - {self.especialidad}"


class Consulta:
    def __init__(self, diagnostico, receta, observaciones):
        self.diagnostico = diagnostico
        self.receta = receta
        self.observaciones = observaciones


class Cita:
    RESERVADA = "reservada"
    CANCELADA = "cancelada"
    ATENDIDA = "atendida"

    def __init__(self, id_cita, paciente, medico, fecha_hora):
        self.id = id_cita
        self.paciente = paciente
        self.medico = medico
        self.fecha_hora = fecha_hora
        self.estado = Cita.RESERVADA
        self.consulta = None

    def esta_activa(self):
        return self.estado == Cita.RESERVADA

    def __str__(self):
        return (f"Cita #{self.id} | {fmt(self.fecha_hora)} | {self.paciente.nombre} "
                f"con {self.medico.nombre} | {self.estado}")


# =====================================================================
# LÓGICA DE NEGOCIO (aquí se trabaja: sin input ni print)
# Los errores de regla se avisan con:  raise ErrorClinica("mensaje claro")
# =====================================================================
class ErrorClinica(Exception):
    """Error de regla de negocio con mensaje legible para el usuario."""


class Clinica:
    def __init__(self):
        self.pacientes = {}   # dni -> Paciente
        self.medicos = {}     # id -> Medico
        self.citas = []       # lista de Cita
        self._sig_medico = 1  # siguiente ID de médico
        self._sig_cita = 1    # siguiente número de cita

    # ---------- Pacientes (C2 - Fernando) ----------
    def registrar_paciente(self, dni, nombre, telefono=""):
        """Crea y guarda un Paciente. Devuelve el paciente creado.
        TODO C2: validar RN-01 (DNI de 8 dígitos), RN-02 (sin duplicados), RN-03 (nombre obligatorio).
        """
        raise NotImplementedError("C2 - registrar_paciente")

    def buscar_pacientes(self, texto):
        """Devuelve la lista de pacientes cuyo DNI es igual al texto o cuyo nombre lo contiene.
        TODO C2: RN-04 (sin distinguir mayúsculas).
        """
        raise NotImplementedError("C2 - buscar_pacientes")

    def obtener_paciente(self, dni):
        """Devuelve el Paciente con ese DNI o lanza ErrorClinica si no existe.
        TODO C2.
        """
        raise NotImplementedError("C2 - obtener_paciente")

    # ---------- Médicos y horarios (C3 - Yulissa) ----------
    def registrar_medico(self, nombre, especialidad):
        """Crea un Medico con ID automático (usa self._sig_medico). Devuelve el médico.
        TODO C3: RN-05 (nombre y especialidad obligatorios).
        """
        raise NotImplementedError("C3 - registrar_medico")

    def obtener_medico(self, id_medico):
        """Devuelve el Medico con ese ID o lanza ErrorClinica si no existe.
        TODO C3.
        """
        raise NotImplementedError("C3 - obtener_medico")

    def agregar_horario(self, id_medico, fecha_hora):
        """Agrega un datetime a los horarios del médico (mantenerlos ordenados).
        TODO C3: RN-07 (no repetir el mismo horario).
        """
        raise NotImplementedError("C3 - agregar_horario")

    def horarios_libres(self, id_medico):
        """Devuelve los horarios del médico que no tienen una cita reservada.
        TODO C3: RN-08 y RN-15 (una cita cancelada libera el horario).
        """
        raise NotImplementedError("C3 - horarios_libres")

    # ---------- Citas (C4 - Jeremías) ----------
    def reservar_cita(self, dni, id_medico, fecha_hora):
        """Crea una Cita reservada y la guarda en self.citas. Devuelve la cita.
        TODO C4: RN-09 (horario del médico), RN-10 (médico sin cruce), RN-11 (paciente sin cruce).
        Usa self._sig_cita para el número de cita.
        """
        raise NotImplementedError("C4 - reservar_cita")

    def obtener_cita(self, id_cita):
        """Devuelve la Cita con ese número o lanza ErrorClinica si no existe.
        TODO C4.
        """
        raise NotImplementedError("C4 - obtener_cita")

    def reprogramar_cita(self, id_cita, nueva_fecha_hora):
        """Cambia la fecha y hora de una cita reservada.
        TODO C4: RN-13 (solo reservadas) y RN-14 (mismas reglas de disponibilidad que reservar).
        """
        raise NotImplementedError("C4 - reprogramar_cita")

    def cancelar_cita(self, id_cita):
        """Cambia el estado de la cita a CANCELADA.
        TODO C4: RN-13 (solo reservadas).
        """
        raise NotImplementedError("C4 - cancelar_cita")

    def citas_activas_paciente(self, dni):
        """Devuelve las citas reservadas de un paciente.
        TODO C4.
        """
        raise NotImplementedError("C4 - citas_activas_paciente")

    # ---------- Consulta e historial (C5 - Yulissa) ----------
    def registrar_consulta(self, id_cita, diagnostico, receta, observaciones):
        """Guarda la Consulta en la cita, la marca ATENDIDA y la agrega al historial del paciente.
        TODO C5: RN-17 (solo citas reservadas), RN-18 (diagnóstico obligatorio), RN-19.
        """
        raise NotImplementedError("C5 - registrar_consulta")

    def historial_paciente(self, dni):
        """Devuelve las citas atendidas del paciente, ordenadas por fecha.
        TODO C5: RN-20.
        """
        raise NotImplementedError("C5 - historial_paciente")

    # ---------- Reportes (C6 - Víctor) ----------
    def reporte_atenciones(self, id_medico, desde, hasta):
        """Devuelve las citas ATENDIDAS del médico con desde <= fecha <= hasta (objetos date).
        TODO C6: RN-22 y RN-23. Ordenar por fecha y hora.
        """
        raise NotImplementedError("C6 - reporte_atenciones")


# =====================================================================
# MENÚ DE CONSOLA (C7 - Jeremías, apoyo Fernando)
# Aquí solo input() y print(). La lógica va en la clase Clinica.
# =====================================================================
def pedir_fecha_hora(texto):
    """Pide fecha y hora hasta que el formato sea válido."""
    while True:
        try:
            return datetime.strptime(input(f"{texto} (AAAA-MM-DD HH:MM): ").strip(), FORMATO)
        except ValueError:
            print("  Formato inválido. Ejemplo: 2026-11-20 09:30")


def pedir_fecha(texto):
    """Pide una fecha (sin hora) hasta que el formato sea válido."""
    while True:
        try:
            return datetime.strptime(input(f"{texto} (AAAA-MM-DD): ").strip(), "%Y-%m-%d").date()
        except ValueError:
            print("  Formato inválido. Ejemplo: 2026-11-20")


def pedir_entero(texto):
    """Pide un número entero hasta que sea válido."""
    while True:
        try:
            return int(input(texto).strip())
        except ValueError:
            print("  Ingresa un número.")


def opcion_registrar_paciente(c):
    # TODO C7: pedir DNI, nombre y teléfono; llamar c.registrar_paciente(...) y mostrar el resultado.
    raise NotImplementedError("C7 - opcion_registrar_paciente")


def opcion_buscar_paciente(c):
    # TODO C7: pedir texto, llamar c.buscar_pacientes(...) y listar los resultados.
    raise NotImplementedError("C7 - opcion_buscar_paciente")


def opcion_registrar_medico(c):
    # TODO C7: pedir nombre y especialidad; llamar c.registrar_medico(...).
    raise NotImplementedError("C7 - opcion_registrar_medico")


def opcion_agregar_horario(c):
    # TODO C7: listar médicos, pedir ID y horario; llamar c.agregar_horario(...).
    raise NotImplementedError("C7 - opcion_agregar_horario")


def opcion_ver_horarios(c):
    # TODO C7: pedir ID del médico y mostrar c.horarios_libres(...).
    raise NotImplementedError("C7 - opcion_ver_horarios")


def opcion_reservar(c):
    # TODO C7: pedir DNI, médico y horario; llamar c.reservar_cita(...).
    raise NotImplementedError("C7 - opcion_reservar")


def opcion_reprogramar(c):
    # TODO C7: pedir número de cita y nueva fecha; llamar c.reprogramar_cita(...).
    raise NotImplementedError("C7 - opcion_reprogramar")


def opcion_cancelar(c):
    # TODO C7: pedir DNI, mostrar sus citas activas y cancelar la elegida.
    raise NotImplementedError("C7 - opcion_cancelar")


def opcion_registrar_consulta(c):
    # TODO C7: pedir DNI, elegir cita activa y pedir diagnóstico, receta y observaciones.
    raise NotImplementedError("C7 - opcion_registrar_consulta")


def opcion_historial(c):
    # TODO C7: pedir DNI y mostrar el historial con diagnóstico, receta y observaciones.
    raise NotImplementedError("C7 - opcion_historial")


def opcion_reporte(c):
    # TODO C7: pedir ID de médico y rango de fechas; mostrar c.reporte_atenciones(...).
    raise NotImplementedError("C7 - opcion_reporte")


MENU = [
    ("Registrar paciente", opcion_registrar_paciente),
    ("Buscar paciente (DNI o nombre)", opcion_buscar_paciente),
    ("Registrar médico", opcion_registrar_medico),
    ("Agregar horario a médico", opcion_agregar_horario),
    ("Ver horarios libres de un médico", opcion_ver_horarios),
    ("Reservar cita", opcion_reservar),
    ("Reprogramar cita", opcion_reprogramar),
    ("Cancelar cita", opcion_cancelar),
    ("Registrar consulta", opcion_registrar_consulta),
    ("Historial clínico de paciente", opcion_historial),
    ("Reporte de atenciones por médico y fechas", opcion_reporte),
]


def main():
    clinica = Clinica()
    while True:
        print("\n=== CLÍNICA - GESTIÓN DE CITAS ===")
        for i, (texto, _) in enumerate(MENU, 1):
            print(f"{i:>2}. {texto}")
        print(" 0. Salir")
        op = pedir_entero("Opción: ")
        if op == 0:
            print("Hasta luego.")
            break
        if not 1 <= op <= len(MENU):
            print("  Opción inválida.")
            continue
        try:
            MENU[op - 1][1](clinica)
        except ErrorClinica as e:
            print("  Error:", e)
        except NotImplementedError as e:
            print("  Pendiente de implementar:", e)


if __name__ == "__main__":
    main()
