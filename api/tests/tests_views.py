from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from api.models import Choice, Poll, Vote


User = get_user_model()


class APIPollTests(APITestCase):
    def setUp(self) -> None:
        """Подготовка прогона теста. Вызывается перед каждым тестом."""
        # Создаем тестового юзера.
        self.user = User.objects.create(
            username='test_user', password='Testpass12'
        )
        # Создаем токен для тестового юзера.
        self.token = Token.objects.create(user=self.user)
        # Создаем тестовый api клиент.
        self.token_client = APIClient()
        # Авторизуем клиент с помощью токена.
        self.token_client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_create_poll(self):
        """
        Убедитесь, что мы можем создать новый объект poll с вариантами choice.
        """
        url = reverse('create-poll')
        data = {
            'title': 'Тестовое голосование через API_Postgres',
            'description': 'Мое тестовое описание голосования',
            'choices': [
                {'text': 'Вариант_1'},
                {'text': 'Вариант_2'},
                {'text': 'Вариант_3'},
                {'text': 'Вариант_4'}
            ]
        }

        # Отправляем POST запрос.
        response = self.token_client.post(url, data, format='json')

        # Проводим проверку ответа.
        # Статус код должен быть равен 201.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Должен создаться 1 объект Poll.
        self.assertEqual(Poll.objects.count(), 1)
        # Должен создаться 1 объект Poll c указанным title.
        self.assertEqual(
            Poll.objects.get().title, 'Тестовое голосование через API_Postgres'
        )
        # Должно создаться 4 объекта Choice.
        self.assertEqual(Choice.objects.count(), 4)
        # Проверим, что один из объектов Choice создался c указанным text.
        self.assertEqual(Choice.objects.get(id=4).text, 'Вариант_4')

    def test_not_create_poll_with_bad_data(self):
        """Убедитесь, что мы не можем создать некорректный объект poll."""
        url = reverse('create-poll')
        data_bad_title = {
            'title': '',
            'choices': [
                {'text': 'Вариант_1'},
            ]
        }
        data_bad_choices = {
            'title': 'Тестовое голосование через API_Postgres',
            'choices': [
                {'text': ''},
            ]
        }

        # Отправляем POST запрос.
        response_bad_title = self.token_client.post(
            url, data_bad_title, format='json'
        )
        response_bad_choices = self.token_client.post(
            url, data_bad_choices, format='json'
        )

        # Проводим проверку ответа.
        # Статус код должен быть равен 400.
        self.assertEqual(
            response_bad_title.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response_bad_choices.status_code, status.HTTP_400_BAD_REQUEST
        )


class APIVoteTests(APITestCase):
    def setUp(self) -> None:
        """Подготовка прогона теста. Вызывается перед каждым тестом."""
        # Создаем тестового юзера.
        self.user = User.objects.create(
            username='test_user', password='Testpass12'
        )
        # Создаем токен для тестового юзера.
        self.token = Token.objects.create(user=self.user)
        # Создаем тестовый api клиент.
        self.token_client = APIClient()
        # Авторизуем клиент с помощью токена.
        self.token_client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        # Создаем тестовое голосование с вариантами ответов.
        self.poll = Poll.objects.create(
            title='Тестовое голосование', creator=self.user)
        self.choice_1 = Choice.objects.create(
            poll_id=self.poll, text='Вариант_1'
        )
        self.choice_2 = Choice.objects.create(
            poll_id=self.poll, text='Вариант_2'
        )

    def test_create_vote(self):
        """Убедитесь, что мы можем создать новый объект vote."""
        url = reverse('poll')
        data = {
            'poll_id': self.poll.id,
            'choice_id': self.choice_1.id
        }

        # Отправляем POST запрос.
        response = self.token_client.post(url, data, format='json')

        # Проводим проверку ответа.
        # Статус код должен быть равен 201.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Должен создаться 1 объект Vote.
        self.assertEqual(Vote.objects.count(), 1)
        # Должен создаться 1 объект Vote c указанным poll_id.
        self.assertEqual(
            Vote.objects.get().poll_id.title, 'Тестовое голосование'
        )
        # Должен создаться 1 объект Vote c указанным choice_id.
        self.assertEqual(
            Vote.objects.get().choice_id.text, 'Вариант_1'
        )

    def test_not_create_vote_with_bad_data(self):
        """Убедитесь, что мы не можем создать некорректный объект vote."""
        url = reverse('poll')
        data_bad_poll_id = {
            'poll_id': '',
            'choice_id': self.choice_1.id
        }
        data_bad_choice_id = {
            'poll_id': self.poll.id,
            'choice_id': ''
        }

        # Отправляем POST запрос.
        response_bad_poll_id = self.token_client.post(
            url, data_bad_poll_id, format='json'
        )
        response_bad_choices_id = self.token_client.post(
            url, data_bad_choice_id, format='json'
        )

        # Проводим проверку ответа.
        # Статус код должен быть равен 400.
        self.assertEqual(
            response_bad_poll_id.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response_bad_choices_id.status_code, status.HTTP_400_BAD_REQUEST
        )
