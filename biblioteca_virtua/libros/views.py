from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LibroForm
from .models import Libro


def listar_libros(request):
    libros = Libro.objects.all()
    return render(request,'libros/listar_libros.html',{'libros':libros})

def detalle_libro(request,libro_id):
    libro = Libro.objects.get(id=libro_id)
    return render(request,'libros/detalle_libro.html',{'libro':libro})

def registrar_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            libro = form.save()
            messages.success(request, f"'{libro.titulo}' ha sido registrado correctamente en el sistema.")
            return redirect('libros:detalle_libro',libro_id=libro.id)
        else:
            messages.error(request,'Hay errores en el formulario')
    else:
        form=LibroForm()

    return render(request,'libros/registrar_libro.html',{'form':form})

def editar_libro(request,libro_id):
    libro = Libro.objects.get(id=libro_id)

    if request.method == 'POST':
        form = LibroForm(request.POST,instance=libro)
        if form.is_valid():
            libro_actualizado = form.save()
            return redirect('libros:detalle_libro', libro_id=libro_actualizado.id)
    else:
        form = LibroForm(instance=libro)
        return render(request,'libros/editar_libro.html',{'form':form,'libro':libro})

def eliminar_libro(request,libro_id):
    libro = Libro.objects.get(id=libro_id)
    if request.method == 'POST':
        libro.delete()
        return redirect('libros:listar_libros')
    else:
        return render(request,'libros/eliminar_libro.html',{'libro':libro})
