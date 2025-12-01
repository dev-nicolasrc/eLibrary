import unittest
from unittest.mock import Mock, patch, MagicMock
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from .models import Libro
from datetime import date

class LibroModelTest(TestCase):
    """Tests de modelo - requieren DB para validar ORM"""
    def setUp(self):
        self.libro = Libro.objects.create(
            titulo='El Principito',
            autor='Antoine de Saint-Exupéry',
            año_publicacion=date(1943, 4, 6)
        )

    def test_libro_creacion(self):
        self.assertEqual(self.libro.titulo, 'El Principito')
        self.assertEqual(self.libro.autor, 'Antoine de Saint-Exupéry')
        self.assertEqual(self.libro.año_publicacion, date(1943, 4, 6))

    def test_libro_str(self):
        self.assertEqual(str(self.libro), 'El Principito (Antoine de Saint-Exupéry)')


class LibroViewTest(unittest.TestCase):
    """Tests de vistas - usan mocks, NO requieren DB"""
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    @patch('libros.models.Libro.objects')
    def test_listar_libros(self, mock_libro_objects):
        # No usar spec para evitar que Mock intercepte atributos definidos
        mock_libro = Mock()
        mock_libro.id = 1  # Valor real para el template
        mock_libro.titulo = '1984'
        mock_libro.autor = 'George Orwell'
        mock_libro.año_publicacion = date(1949, 6, 8)  # Fecha real para el template
        mock_libro_objects.all.return_value = [mock_libro]
        
        response = self.client.get(reverse('libros:listar_libros'))
        self.assertEqual(response.status_code, 200)

    @patch('libros.models.Libro.objects')
    def test_detalle_libro(self, mock_libro_objects):
        # No usar spec para evitar que Mock intercepte atributos definidos
        mock_libro = Mock()
        mock_libro.id = 1
        mock_libro.titulo = '1984'
        mock_libro.autor = 'George Orwell'
        mock_libro.año_publicacion = date(1949, 6, 8)  # Fecha real para el template
        mock_libro_objects.get.return_value = mock_libro
        
        response = self.client.get(reverse('libros:detalle_libro', args=[1]))
        self.assertEqual(response.status_code, 200)

    @patch('libros.views.LibroForm')
    def test_registrar_libro_post_valido(self, mock_form_class):
        mock_form = MagicMock()
        mock_form.is_valid.return_value = True
        mock_libro = Mock()
        mock_libro.id = 1
        mock_form.save.return_value = mock_libro
        mock_form_class.return_value = mock_form
        
        response = self.client.post(reverse('libros:registrar_libro'), {
            'titulo': 'Cien años de soledad',
            'autor': 'Gabriel García Márquez',
            'año_publicacion': '1967-05-30'
        })
        self.assertEqual(response.status_code, 302)

    @patch('libros.views.LibroForm')
    def test_registrar_libro_post_invalido(self, mock_form_class):
        mock_form = MagicMock()
        mock_form.is_valid.return_value = False
        mock_form_class.return_value = mock_form
        
        response = self.client.post(reverse('libros:registrar_libro'), {
            'titulo': '',
            'autor': 'Autor',
            'año_publicacion': '2023-01-01'
        })
        self.assertEqual(response.status_code, 200)

    @patch('libros.views.LibroForm')
    @patch('libros.models.Libro.objects')
    def test_editar_libro(self, mock_libro_objects, mock_form_class):
        # No usar spec para evitar que Mock intercepte atributos definidos
        mock_libro = Mock()
        mock_libro.id = 1
        mock_libro.titulo = '1984'
        mock_libro.autor = 'George Orwell'
        mock_libro.año_publicacion = date(1949, 6, 8)
        mock_libro_objects.get.return_value = mock_libro
        
        mock_form = MagicMock()
        mock_form.is_valid.return_value = True
        mock_libro_actualizado = Mock()
        mock_libro_actualizado.id = 1
        mock_form.save.return_value = mock_libro_actualizado
        mock_form_class.return_value = mock_form
        
        response = self.client.post(reverse('libros:editar_libro', args=[1]), {
            'titulo': '1984 (Editado)',
            'autor': 'George Orwell',
            'año_publicacion': '1949-06-08'
        })
        self.assertEqual(response.status_code, 302)

    @patch('libros.models.Libro.objects')
    def test_eliminar_libro(self, mock_libro_objects):
        # No usar spec para evitar que Mock intercepte atributos definidos
        mock_libro = Mock()
        mock_libro.id = 1
        mock_libro_objects.get.return_value = mock_libro
        
        response = self.client.post(reverse('libros:eliminar_libro', args=[1]))
        self.assertEqual(response.status_code, 302)
        mock_libro.delete.assert_called_once()

