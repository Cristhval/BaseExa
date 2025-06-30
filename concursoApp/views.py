from django.shortcuts import render, redirect
from .decorators import admin_required
from django.contrib.auth.models import User
from .forms import PruebaForm, EstudianteForm
import random
import string

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

            # Aquí puedes elegir qué campo usar para username, ejemplo: cedula
            username = estudiante.cedula

            # Verificar que el username no exista
            if User.objects.filter(username=username).exists():
                form.add_error(None, 'Ya existe un usuario con esa cédula')
                return render(request, 'registro_estudiante.html', {'form': form})

            password = generar_password()

            user = User.objects.create_user(username=username, password=password)
            user.save()

            # Si tienes relación entre estudiante y user, asigna aquí
            # estudiante.user = user

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
        # Si no hay datos en session, redirige a registro
        return redirect('registro_estudiante')

    # Opcional: limpiar las credenciales para que no se repitan
    del request.session['username']
    del request.session['password']

    return render(request, 'registro_exitoso.html', {
        'username': username,
        'password': password,
    })

def pregunta1(request):
    return render(request, 'pregunta1.html')
# Create your views here.


@admin_required
def crear_prueba(request):
    if request.method == 'POST':
        form = PruebaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_prueba')  # o a donde quieras
    else:
        form = PruebaForm()
    return render(request, 'crear_prueba.html', {'form': form})

@admin_required
def panel_admin(request):
    return render(request, 'panel_admin.html')