from django.db import models

class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    año_publicacion = models.DateField()

    def __str__(self):
        return f'{self.titulo} ({self.autor})'
    
    class Meta:
        verbose_name_plural = 'Libros'