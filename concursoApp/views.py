from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory, modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from .decorators import admin_required
from django.contrib.auth.models import User
from .forms import PruebaForm, EstudianteForm, ExamenForm, PreguntaForm, RespuestaForm
import random
import string

from .models import Pregunta, Prueba, Respuesta, Examen


def bienvenida(request):
    return render(request, 'bienvenida.html')

def generar_password(length=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(length))

def registro_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            estudiante = form.save(commit=False)


            username = estudiante.cedula

            # Verificar que el username no exista
            if User.objects.filter(username=username).exists():
                form.add_error(None, 'Ya existe un usuario con esa cédula')
                return render(request, 'registro_estudiante.html', {'form': form})

            password = generar_password()

            user = User.objects.create_user(username=username, password=password)
            user.save()



            estudiante.save()

            # Guardar las credenciales en session para mostrarlas en la siguiente vista
            request.session['username'] = username
            request.session['password'] = password

            return redirect('registro_exitoso')
    else:
        form = EstudianteForm()

    return render(request, 'registro_estudiante.html', {'form': form})

def registro_exitoso(request):
    username = request.session.get('username')
    password = request.session.get('password')

    if not username or not password:
        # Si no hay datos en session redirige a registro
        return redirect('registro_estudiante')


    del request.session['username']
    del request.session['password']

    return render(request, 'registro_exitoso.html', {
        'username': username,
        'password': password,
    })

def pregunta1(request):
    return render(request, 'pregunta1.html')



@admin_required
def crear_prueba(request):
    if request.method == 'POST':
        prueba_form = PruebaForm(request.POST)
        examen_form = ExamenForm(request.POST)
        if prueba_form.is_valid() and examen_form.is_valid():
            prueba = prueba_form.save()
            examen = examen_form.save(commit=False)
            examen.idprueba = prueba
            examen.save()
            return redirect('agregar_preguntas', idprueba=prueba.id)
    else:
        prueba_form = PruebaForm()
        examen_form = ExamenForm()
    return render(request, 'crear_prueba.html', {'prueba_form': prueba_form, 'examen_form': examen_form})

@admin_required
def agregar_preguntas(request, idprueba):
    prueba = get_object_or_404(Prueba, id=idprueba)
    PreguntaFormSet = modelformset_factory(Pregunta, form=PreguntaForm, extra=3)

    if request.method == 'POST':
        formset = PreguntaFormSet(request.POST, queryset=Pregunta.objects.none())
        if formset.is_valid():
            preguntas = formset.save(commit=False)
            for pregunta in preguntas:
                pregunta.idprueba = prueba
                pregunta.save()
            return redirect('agregar_respuestas', idprueba=prueba.id)
    else:
        formset = PreguntaFormSet(queryset=Pregunta.objects.none())
    return render(request, 'agregar_preguntas.html', {'formset': formset, 'prueba': prueba})


@admin_required
def agregar_respuestas(request, idprueba):
    prueba = get_object_or_404(Prueba, id=idprueba)
    preguntas = Pregunta.objects.filter(idprueba=prueba)

    RespuestaFormSet = modelformset_factory(Respuesta, form=RespuestaForm, extra=4, can_delete=False)

    formsets = []

    if request.method == 'POST':
        all_valid = True
        for pregunta in preguntas:
            prefix = f'respuesta_{pregunta.id}'
            formset = RespuestaFormSet(request.POST, queryset=Respuesta.objects.filter(idpregunta=pregunta), prefix=prefix)
            formsets.append((pregunta, formset))
            if not formset.is_valid():
                all_valid = False

        if all_valid:
            for pregunta, formset in formsets:
                respuestas = formset.save(commit=False)
                for respuesta in respuestas:
                    respuesta.idpregunta = pregunta
                    respuesta.save()
            return redirect('panel_admin')
    else:
        for pregunta in preguntas:
            prefix = f'respuesta_{pregunta.id}'
            formset = RespuestaFormSet(queryset=Respuesta.objects.filter(idpregunta=pregunta), prefix=prefix)
            formsets.append((pregunta, formset))

    return render(request, 'agregar_respuestas.html', {'formsets': formsets})

@login_required
def ver_pruebas_activas(request):
    pruebas_activas = Prueba.objects.filter(estado=True)
    examenes = Examen.objects.filter(idprueba__in=pruebas_activas)
    return render(request, 'ver_pruebas_activas.html', {
        'examenes': examenes
    })


@admin_required
def panel_admin(request):
    return render(request, 'panel_admin.html')


@login_required
def redireccion_por_grupo(request):
    if request.user.groups.filter(name='admin').exists():
        return redirect('panel_admin')
    else:
        return redirect('ver_pruebas_activas')


@login_required
def presentar_pregunta(request, examen_id, numero):
    examen = get_object_or_404(Examen, pk=examen_id)
    preguntas = Pregunta.objects.filter(idprueba=examen.idprueba).order_by('id')
    total_preguntas = preguntas.count()

    if numero < 1 or numero > total_preguntas:
        return redirect('ver_pruebas_activas')

    pregunta = preguntas[numero - 1]
    respuestas = Respuesta.objects.filter(idpregunta=pregunta)

    # Obtener tiempo desde el banco de preguntas
    tiempo_segundos = pregunta.idbancopregunta.tiempo.tiempo if pregunta.idbancopregunta and pregunta.idbancopregunta.tiempo else 60

    if request.method == 'POST':
        respuesta_id = request.POST.get('respuesta')

        siguiente = numero + 1
        if siguiente > total_preguntas:
            return redirect('ver_pruebas_activas')
        return redirect('presentar_pregunta', examen_id=examen_id, numero=siguiente)

    return render(request, 'presentar_pregunta.html', {
        'pregunta': pregunta,
        'respuestas': respuestas,
        'examen': examen,
        'numero': numero,
        'total': total_preguntas,
        'tiempo_segundos': tiempo_segundos,
    })
