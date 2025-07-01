"""
URL configuration for ConcursoPreguntas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView


from concursoApp import views
from concursoApp.views import crear_prueba, bienvenida, registro_estudiante, registro_exitoso

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', bienvenida, name='bienvenida'),
    path('registro/', views.registro_estudiante, name='registro_estudiante'),
    path('registro/exitoso/', views.registro_exitoso, name='registro_exitoso'),

    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('panel-admin/', views.panel_admin, name='panel_admin'),

    path('crear-prueba/', crear_prueba, name='crear_prueba'),
    path('crear-prueba/<int:idprueba>/agregar-preguntas/', views.agregar_preguntas, name='agregar_preguntas'),

    # Paso 2: Agregar preguntas
    path('crear-prueba/<int:idprueba>/agregar-respuestas/', views.agregar_respuestas, name='agregar_respuestas'),

    path('pregunta1/', views.pregunta1, name='pregunta1'),
]
