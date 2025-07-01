from django import forms
from .models import Prueba, Estudiante, Examen, Pregunta, Respuesta


class PruebaForm(forms.ModelForm):
    class Meta:
        model = Prueba
        fields = ['fechainicio', 'fechafin', 'estado']

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'apellido', 'correo', 'cedula']


class ExamenForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = ['titulo', 'estado', 'descripcion']

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['cuerpo', 'url_imagen', 'idbancopregunta']

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ['descripcion', 'estado']  # No incluir 'id' ni 'idpregunta'
        labels = {
            'estado': '¿Es correcta?',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'id' in self.fields:
            self.fields['id'].widget = forms.HiddenInput()
        if 'idpregunta' in self.fields:
            self.fields['idpregunta'].widget = forms.HiddenInput()
