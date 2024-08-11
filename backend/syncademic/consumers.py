import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from datetime import datetime


class NotificacionConsumidor(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'message': 'Conexion establecida exitosamente'
        }))

    async def receive(self, text_data=None, bytes_data=None):
        from syncademic.models.docente import Docente
        from syncademic.models.aspecto import Aspecto
        from syncademic.models.notificacion import Notificacion

        text_data_json = json.loads(text_data)
        id_docente = text_data_json.get('id_docente')

        try:
            docente = await sync_to_async(Docente.objects.get)(id_docente=id_docente)
            nombre = docente.nombre  # Nombre del docente
            fecha_actual = datetime.now().date()
            aspectos = await sync_to_async(list)(Aspecto.objects.filter(docente=docente))
            aspectos_info = []

            for aspecto in aspectos:
                if fecha_actual >= aspecto.fecha_inicio:
                    estado_notificacion = aspecto.determinar_estado_notificacion(
                        aspecto.calcular_tiempo_transcurrido(),
                        aspecto.calcular_progreso_actual()
                    )

                    mensaje = {
                        'estado_aspecto': 'Activo',
                        'nombre_aspecto': aspecto.nombre,
                        'fecha_fin': aspecto.fecha_fin.isoformat(),
                        'estado_notificacion': estado_notificacion,
                        'progreso_general_porcentaje': aspecto.calcular_progreso_actual(),
                        'tiempo_transcurrido_porcentaje': aspecto.calcular_tiempo_transcurrido()
                    }

                    if estado_notificacion in ["CRITICO", "INTENSO"]:
                        mensaje['subaspectos'] = aspecto.subaspectos

                    notificacion = await sync_to_async(Notificacion.objects.create)(
                        aspecto=aspecto,
                        estado=estado_notificacion,
                        mensaje=mensaje
                    )

                    es_dia_notificacion = notificacion.comportarse_segun(estado_notificacion)

                    aspectos_info.append({
                        'nombre_aspecto': aspecto.nombre,
                        'estado_notificacion': estado_notificacion,
                        'notificaciones_disponibles': es_dia_notificacion,
                        'mensaje': notificacion.mensaje if es_dia_notificacion else {}
                    })
                else:
                    aspectos_info.append({
                        'nombre_aspecto': aspecto.nombre,
                        'estado_aspecto': 'Inactivo',
                        'fecha_inicio': aspecto.fecha_inicio.isoformat(),
                        'fecha_fin': aspecto.fecha_fin.isoformat(),
                    })

            # Preparar el JSON final para enviar
            response_data = {
                'nombre_docente': nombre,
                'notificaciones': aspectos_info
            }

            # Enviar el JSON al cliente
            await self.send(text_data=json.dumps(response_data))

        except Docente.DoesNotExist:
            await self.send(text_data=json.dumps({
                'error': 'Docente no encontrado'
            }))
