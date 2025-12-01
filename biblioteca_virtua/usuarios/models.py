from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    edad = models.IntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nombre} ({self.correo})'

    class Meta:
        verbose_name_plural = 'Usuarios'