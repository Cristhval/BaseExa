from django import forms
from .models import Prueba, Estudiante


class PruebaForm(forms.ModelForm):
    class Meta:
        model = Prueba
        fields = ['fechainicio', 'fechafin', 'estado']

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'apellido', 'correo', 'cedula']