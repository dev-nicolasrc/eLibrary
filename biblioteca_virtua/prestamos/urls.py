from django.urls import path
from . import views

app_name = 'prestamos'

urlpatterns = [
    path('registrar/',views.registrar_prestamo,name='registrar_prestamo'),
    path('listar/',views.listar_prestamos,name='listar_prestamos'),
    path('devolucion/<int:prestamo_id>/',views.registrar_devolucion,name='registrar_devolucion'),
    path('detalle/<int:prestamo_id>/',views.detalle_prestamo,name='detalle_prestamo'),
    path('eliminar/<int:prestamo_id>/',views.eliminar_prestamo,name='eliminar_prestamo'),
    path('editar/<int:prestamo_id>/',views.editar_prestamo,name='editar_prestamo'),
]