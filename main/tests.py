from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Material, Test, Question


class UserRegisterTest(APITestCase):
    def test_user_registration(self):
        url = reverse('user-register')
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'testuser@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')


class MaterialViewSetTest(APITestCase):
    def setUp(self):
        # Создаем тестовый материал
        self.material = Material.objects.create(title='Test Material', content='Test Content')
        # Создаем URL для нашего ViewSet
        self.url = reverse('material-list')

    def test_material_list(self):
        # Получаем список всех материалов
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_material_creation(self):
        # Тест на создание нового материала
        data = {
            'title': 'New Material',
            'content': 'New content'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Material.objects.count(), 2)
        self.assertEqual(Material.objects.latest('id').title, 'New Material')

    def test_material_detail(self):
        # Тест на получение детальной информации о материале
        url = reverse('material-detail', args=[self.material.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Material')

    def test_material_update(self):
        # Тест на обновление материала
        url = reverse('material-detail', args=[self.material.id])
        data = {
            'title': 'Updated Material',
            'content': 'Updated content'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.material.refresh_from_db()
        self.assertEqual(self.material.title, 'Updated Material')

    def test_material_deletion(self):
        # Тест на удаление материала
        url = reverse('material-detail', args=[self.material.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Material.objects.count(), 0)


class TestViewSetTestCase(APITestCase):
    def test_create_test(self):
        url = reverse('test-list')
        data = {'title': 'Математика', 'material': 'Математический анализ'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_tests(self):
        url = reverse('test-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_tests(self):
        url = f"{reverse('test-list')}?title=Математика&material=Математический анализ"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class QuestionViewSetTestCase(APITestCase):
    def test_create_question(self):
        test = Test.objects.create(
            title='Математика')  # Предположим, что Test это модель для тестов, и у неё есть нужные поля.
        url = reverse('question-list')
        data = {'text': '2+2=?', 'test': test.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_questions(self):
        url = reverse('question-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ChoiceViewSetTestCase(APITestCase):
    def test_create_choice(self):
        question = Question.objects.create(text='2+2=?')  # Предположим, что Question это модель для вопросов.
        url = reverse('choice-list')
        data = {'question': question.id, 'text': '4', 'is_correct': True}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_choices(self):
        url = reverse('choice-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
