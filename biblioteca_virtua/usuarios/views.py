from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import RegistroUsuarioForm
from .models import Usuario


def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            return redirect('usuarios:confirmacion_usuario',usuario_id=usuario.id)
        else:
            messages.error(request, f'Hay errores en el formulario.')
    else:
        form=RegistroUsuarioForm()
    
    return render(request, 'usuarios/registrar_usuario.html',{'form':form})

def confirmacion_usuario(request,usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    return render(request, 'usuarios/confirmacion.html',{'usuario':usuario})
