from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('registro/',views.registrar_usuario, name='registrar_usuario'),
    path('confirmacion/<int:usuario_id>/',views.confirmacion_usuario,name='confirmacion_usuario')
]