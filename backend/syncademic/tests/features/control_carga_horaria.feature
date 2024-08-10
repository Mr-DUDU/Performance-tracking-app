# Created by david at 7/25/2024
# language: es

Característica: Control de carga horaria
  Como institución, quiero que el sistema monitoree la carga horaria de cada docente para
  identificar las horas de Gestión atrasadas.

  Esquema del escenario: Notificación según estado del "Jodimetro"
    Dado que la tasa de avance del docente es <calcular_progreso_actual_aspecto>% y el tiempo transcurrido es <tiempo_transcurrido>%
    Cuando el sistema revisa su tasa de avance
    Entonces el docente debe recibir un nivel <estado> notificaciones

  Ejemplos:
    | calcular_progreso_actual_aspecto | tiempo_transcurrido  | estado               |
    | 19                               | 50                   | NORMAL               |
    | 51                               | 80                   | INTENSO              |
    | 49                               | 90                   | CRITICO              |
