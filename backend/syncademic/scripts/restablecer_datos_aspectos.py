from datetime import datetime
from syncademic.models.aspecto import Aspecto, Docente

def run():
    # Eliminar todos los docentes existentes
    Docente.objects.all().delete()

    # Crear un nuevo docente
    docente = Docente.objects.create(
        id_docente=1,
        nombre="Carlos"
    )

    print(f"Docente {docente.nombre} creado.")

    # Borrar todos los aspectos existentes de este docente (aunque no debería ser necesario ya que es un nuevo docente)
    Aspecto.objects.filter(docente=docente).delete()

    # Subaspectos para Docencia - Estado CRÍTICO (Progreso bajo, tiempo muy avanzado)
    subaspectos_docencia = [
        {'nombre': 'Registro_clase', 'progreso': 10},
        {'nombre': 'Tutoría', 'progreso': 20},
        {'nombre': 'Planificación', 'progreso': 30}
    ]

    # Crear el aspecto de Docencia
    aspecto_docencia = Aspecto.objects.create(
        nombre="Docencia",
        fecha_inicio=datetime(2024, 6, 1),
        fecha_fin=datetime(2024, 8, 7),  # Fecha de fin justo antes de la fecha actual
        subaspectos=subaspectos_docencia,
        docente=docente
    )

    # Subaspectos para Gestión - Estado INTENSO (Tiempo avanzado, progreso medio-bajo)
    subaspectos_gestion = [
        {'nombre': 'Administración', 'progreso': 10},
        {'nombre': 'Comité', 'progreso': 15},
        {'nombre': 'Capacitación', 'progreso': 5}
    ]

    # Crear el aspecto de Gestión
    aspecto_gestion = Aspecto.objects.create(
        nombre="Gestión",
        fecha_inicio=datetime(2024, 6, 1),
        fecha_fin=datetime(2024, 9, 10),
        subaspectos=subaspectos_gestion,
        docente=docente
    )

    # Subaspectos para Investigación - Estado BAJO (Inactivo, fecha futura)
    subaspectos_investigacion = [
        {'nombre': 'TIC', 'progreso': 0},
        {'nombre': 'Conferencias', 'progreso': 0},
        {'nombre': 'Publicaciones', 'progreso': 0}
    ]

    # Crear el aspecto de Investigación
    aspecto_investigacion = Aspecto.objects.create(
        nombre="Investigación",
        fecha_inicio=datetime(2024, 9, 30),  # Fecha de inicio futura
        fecha_fin=datetime(2024, 12, 1),
        subaspectos=subaspectos_investigacion,
        docente=docente
    )

    print("Docente creado y datos de prueba actualizados con éxito.")
