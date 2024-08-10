from behave import step
from datetime import datetime, timedelta
from syncademic.models.aspecto import Aspecto
from syncademic.models.docente import Docente
from syncademic.models.notificacion import Notificacion

@step("que la tasa de avance del docente es {progreso_actual:d}% y el tiempo transcurrido es {tiempo_transcurrido:d}%")
def step_impl(context, progreso_actual, tiempo_transcurrido):
    # Simula la creación de un aspecto con los valores proporcionados
    fecha_inicio = datetime.now().date() - timedelta(days=(tiempo_transcurrido * 10 / 100))
    fecha_fin = datetime.now().date() + timedelta(days=(100 - tiempo_transcurrido) * 10 / 100)

    subaspectos = [
        {'nombre': 'Actividad1', 'progreso': progreso_actual / 3},
        {'nombre': 'Actividad2', 'progreso': progreso_actual / 3},
        {'nombre': 'Actividad3', 'progreso': progreso_actual / 3}
    ]

    docente = Docente.objects.get(id_docente=3)
    context.aspecto = Aspecto.objects.create(
        nombre="AspectoPrueba",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        subaspectos=subaspectos,
        docente=docente
    )

@step("el sistema revisa su tasa de avance")
def step_impl(context):
    # Crea una notificación para el aspecto
    context.notificacion = Notificacion.objects.create(
        aspecto=context.aspecto,
        estado="BAJO"  # Estado inicial
    )

    # Ahora se recalcula el estado basado en el progreso y tiempo
    tiempo_transcurrido = context.aspecto.calcular_tiempo_transcurrido()
    progreso_actual = context.aspecto.calcular_progreso_actual()
    context.notificacion.estado = context.aspecto.determinar_estado_notificacion(tiempo_transcurrido, progreso_actual)
    context.notificacion.save()

@step("el docente debe recibir un nivel {estado} notificaciones")
def step_impl(context, estado):
    # Verifica que el estado de la notificación sea el esperado
    assert context.notificacion.estado == estado, f"Expected {estado} but got {context.notificacion.estado}"
