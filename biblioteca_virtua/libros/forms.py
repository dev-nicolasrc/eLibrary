from django import forms
from .models import Libro

class LibroForm(forms.ModelForm):

    class Meta:
        model = Libro
        fields = ['titulo','autor','año_publicacion']
        widgets = { 'titulo': forms.TextInput(attrs={'class':'form-control','placeholder': 'Titulo'}),
                    'autor': forms.TextInput(attrs={'class':'form-control','placeholder': 'Nombre Autor'}),
                    'año_publicacion': forms.DateInput(attrs={'type':'date','class':'form-control'},format='%Y-%m-%d')}