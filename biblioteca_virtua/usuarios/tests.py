import unittest
from unittest.mock import Mock, patch, MagicMock
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from .models import Usuario

class UsuarioModelTest(TestCase):
    """Tests de modelo - requieren DB"""
    def setUp(self):
        self.usuario = Usuario.objects.create(
            nombre='Juan Perez',
            correo='juan@example.com',
            edad=30
        )

    def test_usuario_creacion(self):
        self.assertEqual(self.usuario.nombre, 'Juan Perez')
        self.assertEqual(self.usuario.correo, 'juan@example.com')
        self.assertEqual(self.usuario.edad, 30)
        self.assertTrue(self.usuario.activo)

    def test_usuario_str(self):
        self.assertEqual(str(self.usuario), 'Juan Perez (juan@example.com)')


class UsuarioViewTest(unittest.TestCase):
    """Tests de vistas - usan mocks, NO requieren DB"""
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    @patch('usuarios.views.RegistroUsuarioForm')
    def test_registrar_usuario_post_valido(self, mock_form_class):
        mock_form = MagicMock()
        mock_form.is_valid.return_value = True
        mock_usuario = Mock()
        mock_usuario.id = 1
        mock_form.save.return_value = mock_usuario
        mock_form_class.return_value = mock_form
        
        response = self.client.post(reverse('usuarios:registrar_usuario'), {
            'nombre': 'Carlos Ruiz',
            'correo': 'carlos@example.com',
            'edad': 40
        })
        self.assertEqual(response.status_code, 302)

    @patch('usuarios.views.RegistroUsuarioForm')
    def test_registrar_usuario_post_invalido(self, mock_form_class):
        mock_form = MagicMock()
        mock_form.is_valid.return_value = False
        mock_form_class.return_value = mock_form
        
        response = self.client.post(reverse('usuarios:registrar_usuario'), {
            'nombre': '',
            'correo': 'invalid-email',
            'edad': -5
        })
        self.assertEqual(response.status_code, 200)

    @patch('usuarios.models.Usuario.objects')
    def test_confirmacion_usuario(self, mock_usuario_objects):
        from django.utils import timezone
        # No usar spec para evitar que Mock intercepte atributos definidos
        mock_usuario = Mock()
        mock_usuario.id = 1
        mock_usuario.nombre = 'Maria Lopez'
        mock_usuario.correo = 'maria@example.com'
        mock_usuario.edad = 25
        mock_usuario.fecha_registro = timezone.now()  # Fecha real para el template
        mock_usuario_objects.get.return_value = mock_usuario
        
        response = self.client.get(reverse('usuarios:confirmacion_usuario', args=[1]))
        self.assertEqual(response.status_code, 200)

