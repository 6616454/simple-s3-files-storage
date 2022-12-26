from starlette.testclient import TestClient

from src.main import build_app

import shortuuid


class CustomTestUser:
    def __init__(self) -> None:
        self.token: str = ""

    def set_token(self, token: str) -> None:
        self.token = token


user = CustomTestUser()


class TestMain:

    def setup_method(self):
        self.client = TestClient(build_app())

    def test_without_authentication(self):
        response = self.client.get('/url/user/status')

        assert response.status_code == 401

    def test_authentication(self):
        response = self.client.post('/auth/sign-up', json={
            'username': str(shortuuid.uuid()),
            'password': '123456',
            'password_correct': '123456'
        })

        token_type = response.json()['token_type']

        user.set_token(response.json()['access_token'])

        assert response.status_code == 200
        assert token_type == 'Bearer'

    def test_invalid_authentication(self):
        response = self.client.post('auth/sign-up', json={
            'username': str(shortuuid.uuid()),
            'password': '123456',
            'password_correct': '12345'
        })

        assert response.json()['detail'] == 'Credentials not valid'

    def test_create_url(self):
        response = self.client.post('/url', json={
            'original_url': 'original_url_test'
        }, headers={'Authorization': f'Bearer {user.token}'})

        assert response.status_code == 200
        assert 'short_url' in response.json()
