from django.shortcuts import render, redirect
from .forms import PrestamoForm
from django.contrib import messages
from .models import Prestamo
from django.utils import timezone

def registrar_prestamo(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = form.save()
            messages.success(request,'El prestamo se registro exitosamente')
            return redirect('prestamos:detalle_prestamo',prestamo_id=prestamo.id)
        else:
            messages.error(request,'Hay errores en el formulario')
    else:
        form = PrestamoForm()
    return render(request,'prestamos/registrar_prestamo.html',{'form':form})

def detalle_prestamo(request,prestamo_id):
    prestamo = Prestamo.objects.get(id=prestamo_id)
    return render(request,'prestamos/detalle_prestamo.html',{'prestamo':prestamo})

def listar_prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request,'prestamos/listar_prestamos.html',{'prestamos':prestamos})

def registrar_devolucion(request,prestamo_id):
    prestamo = Prestamo.objects.get(id=prestamo_id)
    if request.method == 'POST':
        prestamo.fecha_devolucion = timezone.now()
        prestamo.save()
        return redirect('prestamos:listar_prestamos')
    else:
        return render(request,'prestamos/registrar_devolucion.html',{'prestamo':prestamo})
    
def eliminar_prestamo(request,prestamo_id):
    prestamo = Prestamo.objects.get(id=prestamo_id)
    if request.method == 'POST':
        prestamo.delete()
        return redirect('prestamos:listar_prestamos')
    else:
        return render(request,'prestamos/eliminar_prestamo.html',{'prestamo':prestamo})

def editar_prestamo(request,prestamo_id):
    prestamo = Prestamo.objects.get(id=prestamo_id)

    if request.method == 'POST':
        form = PrestamoForm(request.POST,instance=prestamo)
        if form.is_valid():
            prestamo_actualizado = form.save()
            return redirect('prestamos:detalle_prestamo', prestamo_actualizado.id)
        else:
            messages.error(request,'Hay errores en el formulario')
    else:
        form = PrestamoForm(instance=prestamo)
        return render(request,'prestamos/editar_prestamo.html',{'form':form,'prestamo':prestamo})

