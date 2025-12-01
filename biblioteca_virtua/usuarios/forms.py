from django import forms
from .models import Usuario

class RegistroUsuarioForm(forms.ModelForm):
 
 class Meta:
    model = Usuario
    fields = ['nombre', 'correo', 'edad']
    widgets = { 'nombre': forms.TextInput(attrs={'class':'form-control','placeholder': 'Tu nombre completo'}),
                'correo': forms.EmailInput(attrs={'class':'form-control','placeholder': 'tu@email.com'}),
                'edad': forms.NumberInput(attrs={'class':'form-control','min':'18','max':'120'})}