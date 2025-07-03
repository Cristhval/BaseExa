
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView


from concursoApp import views
from concursoApp.views import crear_prueba, bienvenida, registro_estudiante, registro_exitoso, CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', bienvenida, name='bienvenida'),
    path('registro/', views.registro_estudiante, name='registro_estudiante'),
    path('registro/exitoso/', views.registro_exitoso, name='registro_exitoso'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('panel-admin/', views.panel_admin, name='panel_admin'),

    path('crear-prueba/', crear_prueba, name='crear_prueba'),
    path('crear-prueba/<int:idprueba>/agregar-preguntas/', views.agregar_preguntas, name='agregar_preguntas'),

    # Paso 2: Agregar preguntas
    path('crear-prueba/<int:idprueba>/agregar-respuestas/', views.agregar_respuestas, name='agregar_respuestas'),
    path('redirigir-por-grupo/', views.redireccion_por_grupo, name='redireccion_por_grupo'),
    path('pruebas-activas/', views.ver_pruebas_activas, name='ver_pruebas_activas'),

    path('examen/<int:examen_id>/pregunta/<int:numero>/', views.presentar_pregunta, name='presentar_pregunta'),
    path('resultados/', views.ver_resultados, name='ver_resultados'),

    path('pregunta1/', views.pregunta1, name='pregunta1'),
]
