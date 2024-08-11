from django.db import models

from syncademic.models.docente import Docente
from syncademic.models.periodo import Periodo


class Puntuacion_docente(models.Model):
    """ Modelo PuntuacionDocente

        Utilizado para Feature 8
        Creado por Christopher Zambrano

        Attributes:
            id_puntuacion (int): Identificador primario.
            id_docente (ForeignKey): Relación con el modelo Docente.
            periodo (ForeignKey): Relación con el modelo Periodo.
            puntaje (int): Puntaje obtenido por el docente en el periodo.
    """
    id_puntuacion = models.AutoField(primary_key=True)
    id_docente = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True)
    periodo = models.ForeignKey(Periodo, on_delete=models.SET_DEFAULT, default=1)
    puntaje = models.IntegerField()

    def __str__(self):
        return f"{self.id_docente} - {self.puntaje}"
