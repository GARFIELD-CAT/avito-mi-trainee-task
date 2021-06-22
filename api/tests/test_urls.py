from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase

from api.models import Choice, Poll

User = get_user_model()


class APIUrlTests(APITestCase):
    def setUp(self) -> None:
        """Подготовка прогона теста. Вызывается перед каждым тестом."""
        # Создаем тестового юзера.
        self.user_token = User.objects.create(
            username='test_user_token', password='Testpass12'
        )
        # Создаем пользователя без токена.
        self.user = User.objects.create(
            username='test_user', password='Testpass12'
        )
        # Создаем тестовый api клиент без токена.
        self.client: APIClient = APIClient()

        self.client.login(
            username=self.user.username, password=self.user.password
        )
        # Создаем токен для тестового юзера.
        self.token: Token = Token.objects.create(user=self.user_token)
        # Создаем тестовый api клиент с токеном.
        self.token_client: APIClient = APIClient()
        # Авторизуем клиент с помощью токена.
        self.token_client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.url_names = {
            'create_poll': '/api/v1/createPoll/',
            'create_vote': '/api/v1/poll/',
            'get_result': '/api/v1/getResult/',
        }
        self.poll = Poll.objects.create(
            title='Голосование_1', creator=self.user_token
        )
        self.choice = Choice.objects.create(
            poll_id=self.poll, text='Вариант голосования'
        )

    def test_create_poll_url_available_to_the_user_with_a_token(self) -> None:
        """Адрес createPoll доступен пользователю с токеном."""
        url = self.url_names['create_poll']
        data = {
            'title': 'Тестовое голосование через API_Postgres',
            'description': 'Мое тестовое описание голосования',
            'choices': [
                {'text': 'Вариант_1'}
            ]
        }

        # Отправляем POST запрос.
        response: Response = self.token_client.post(url, data, format='json')

        # Проводим проверку ответа.
        # Статус код должен быть равен 201.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_vote_url_available_to_the_user_with_a_token(self) -> None:
        """Адрес poll доступен пользователю с токеном."""
        url = self.url_names['create_vote']
        data = {
            'poll_id': self.poll.id,
            'choice_id': self.choice.id,
        }

        # Отправляем POST запрос.
        response: Response = self.token_client.post(url, data, format='json')

        # Проводим проверку ответа.
        # Статус код должен быть равен 201.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_result_url_available_to_the_user_with_a_token(self) -> None:
        """Адрес getResult доступен пользователю с токеном."""
        url = self.url_names['get_result']
        data = {
            'poll_id': self.poll.id,
        }

        # Отправляем POST запрос.
        response: Response = self.token_client.post(url, data, format='json')

        # Проводим проверку ответа.
        # Статус код должен быть равен 200.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_is_not_available_to_the_user_without_a_token(self) -> None:
        """Адреса не доступены пользователю без токена."""
        data = {}

        for url in self.url_names.values():
            with self.subTest(url=url):
                # Отправляем POST запрос.
                response: Response = self.client.post(url, data, format='json')

                # Проводим проверку ответа.
                # Статус код должен быть равен 401.
                self.assertEqual(
                    response.status_code, status.HTTP_401_UNAUTHORIZED
                )
