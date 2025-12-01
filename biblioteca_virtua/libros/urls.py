from django.urls import path
from . import views

app_name = 'libros'

urlpatterns = [
    path('listar/', views.listar_libros, name='listar_libros'),
    path('registro/',views.registrar_libro, name='registrar_libro'),
    path('detalle/<int:libro_id>/', views.detalle_libro, name='detalle_libro'),
    path('eliminar/<int:libro_id>/', views.eliminar_libro, name='eliminar_libro'),
    path('editar/<int:libro_id>', views.editar_libro, name='editar_libro'),
]