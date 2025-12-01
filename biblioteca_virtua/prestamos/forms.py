from django import forms
from .models import Prestamo
from libros.models import Libro
from django.db.models import Q, Exists, OuterRef

class PrestamoForm(forms.ModelForm):

    class Meta:
        model = Prestamo
        fields = ['usuario','libro']
        widgets = {'usuario': forms.Select(attrs={'class':'form-control'}),
                   'libro': forms.Select(attrs={'class':'form-control'}),}
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['usuario'].empty_label = 'Seleccione un Usuario'
        self.fields['libro'].empty_label = 'Seleccione un Libro'
        prestamo_activo = Prestamo.objects.filter(libro=OuterRef('pk'),fecha_devolucion__isnull=True)
        self.fields['libro'].queryset = Libro.objects.annotate(tiene_activo=Exists(prestamo_activo)).filter(tiene_activo=False)