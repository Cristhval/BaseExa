from django.contrib import admin
from .models import (
    Categoria, Bancopregunta, Estudiante, Prueba,
    Examen, Pregunta, Respuesta, Resultado, RespuestaEstudiante
)

admin.site.register(Categoria)
admin.site.register(Bancopregunta)
admin.site.register(Estudiante)
admin.site.register(Prueba)
admin.site.register(Examen)
admin.site.register(Pregunta)
admin.site.register(Respuesta)
admin.site.register(Resultado)
admin.site.register(RespuestaEstudiante)
