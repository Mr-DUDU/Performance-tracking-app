from datetime import datetime
from syncademic.models.aspecto import Aspecto
from syncademic.models.docente import Docente

def run():
    try:
        # Eliminar todos los docentes existentes
        Docente.objects.all().delete()

        # Crear un nuevo docente para las pruebas de Gherkin
        docente_prueba = Docente.objects.create(
            id_docente=3,
            nombre="Carlos",
            correo="carlos@example.com",
            estado_capacitacion="Completo",
            carrera="Ingeniería"
        )

        print(f"Docente {docente_prueba.nombre} creado para pruebas de Gherkin.")

        # Crear aspectos para el docente de prueba Gherkin
        Aspecto.objects.create(
            nombre="Docencia",
            fecha_inicio=datetime(2024, 1, 1),
            fecha_fin=datetime(2024, 12, 31),
            subaspectos=[{'nombre': 'Registro de clases', 'progreso': 19}],
            docente=docente_prueba
        )

        Aspecto.objects.create(
            nombre="Gestión",
            fecha_inicio=datetime(2024, 1, 1),
            fecha_fin=datetime(2024, 12, 31),
            subaspectos=[{'nombre': 'Administración', 'progreso': 51}],
            docente=docente_prueba
        )

        Aspecto.objects.create(
            nombre="Investigación",
            fecha_inicio=datetime(2024, 1, 1),
            fecha_fin=datetime(2024, 12, 31),
            subaspectos=[{'nombre': 'Publicaciones', 'progreso': 49}],
            docente=docente_prueba
        )

        # Crear un nuevo docente Marcela
        docente_marcela = Docente.objects.create(
            id_docente=1,
            nombre="Marcela",
            correo="marcela@example.com",
            estado_capacitacion="Incompleto",
            carrera="Ingeniería Software"
        )

        print(f"Docente {docente_marcela.nombre} creado.")

        # Crear aspectos para Marcela
        subaspectos_docencia = [
            {'nombre': 'Registro_clase', 'progreso': 20},
            {'nombre': 'Tutoría', 'progreso': 30},
            {'nombre': 'Planificación', 'progreso': 50}
        ]
        Aspecto.objects.create(
            nombre="Docencia",
            fecha_inicio=datetime(2024, 7, 12),
            fecha_fin=datetime(2024, 8, 18),
            subaspectos=subaspectos_docencia,
            docente=docente_marcela
        )

        subaspectos_gestion = [
            {'nombre': 'Administración', 'progreso': 50},
            {'nombre': 'Comité', 'progreso': 65},
            {'nombre': 'Capacitación', 'progreso': 30}
        ]
        Aspecto.objects.create(
            nombre="Gestión",
            fecha_inicio=datetime(2024, 7, 24),
            fecha_fin=datetime(2024, 8, 20),
            subaspectos=subaspectos_gestion,
            docente=docente_marcela
        )

        subaspectos_investigacion = [
            {'nombre': 'TIC', 'progreso': 10},
            {'nombre': 'Conferencias', 'progreso': 20},
            {'nombre': 'Publicaciones', 'progreso': 15}
        ]
        Aspecto.objects.create(
            nombre="Investigación",
            fecha_inicio=datetime(2024, 8, 5),
            fecha_fin=datetime(2024, 8, 23),
            subaspectos=subaspectos_investigacion,
            docente=docente_marcela
        )

        print("Datos de prueba actualizados con éxito.")
    except Exception as e:
        print(f"Error durante la actualización de datos: {str(e)}")
