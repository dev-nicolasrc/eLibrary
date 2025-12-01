from django.db import models
from django.core.exceptions import ValidationError

class Prestamo(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    libro = models.ForeignKey('libros.Libro', on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null=True,blank=True)
    
    def __str__(self):
        estado = 'Prestado' if self.fecha_devolucion is None else 'Disponible' 
        return f'{self.libro} prestado a {self.usuario} (Estado del libro: {estado})'
    
    class Meta:
        verbose_name_plural = 'Prestamos'

