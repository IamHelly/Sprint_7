import allure
import requests
from data_courier import DataLoginCourier
from urls import Urls


class TestLoginCourier:
    @allure.title('Проверка, что курьер может авторизоваться, а также что в запросе переданы все обязательные поля '
                  'и в теле ответа возвращается id')
    @allure.description('Проверка, что при логине курьера передаются оба обязательных поля, '
                        'а также в ответе сервера получены верный код и поле id')
    def test_courier_authorization_with_all_required_fields(self):
        payload = {
            "login": DataLoginCourier.login,
            "password": DataLoginCourier.password
        }
        response = requests.post(f"{Urls.BASE_URL}/api/v1/courier/login", data=payload)
        assert response.status_code == 200 and response.json()["id"] is not None

    @allure.title('Проверка получения ошибки при авторизации курьера с неправильно указанным логином')
    @allure.description('Проверка, что в случае отправки запроса авторизации с неверным логином приходит ошибка, '
                        'а также в ответе сервера получены верный код и тело.')
    def test_courier_not_authorized_with_wrong_login(self):
        payload = {
            "login": "Volandemort98",
            "password": DataLoginCourier.password
        }
        response = requests.post(f"{Urls.BASE_URL}/api/v1/courier/login", data=payload)
        assert response.status_code == 404 and response.json()["message"] == "Учетная запись не найдена"

    @allure.title('Проверка получения ошибки при авторизации курьера с неправильно указанным паролем')
    @allure.description('Проверка, что в случае отправки запроса авторизации с неверным паролем приходит ошибка, '
                        'а также в ответе сервера получены верный код и тело.')
    def test_courier_not_authorized_with_wrong_password(self):
        payload = {
            "login": DataLoginCourier.login,
            "password": "Aa123456"
        }
        response = requests.post(f"{Urls.BASE_URL}/api/v1/courier/login", data=payload)
        assert response.status_code == 404 and response.json()["message"] == "Учетная запись не найдена"

    @allure.title('Проверка получения ошибки при авторизации курьера с отсутствием одного из обязательных полей')
    @allure.description('Проверка, что в случае отправки запроса авторизации без логина приходит ошибка, '
                        'а также в ответе сервера получены верный код и тело.')
    def test_courier_not_authorized_without_one_of_required_fields(self):
        payload = {
            "password": DataLoginCourier.password
        }
        response = requests.post(f"{Urls.BASE_URL}/api/v1/courier/login", data=payload)
        assert response.status_code == 400 and response.json()["message"] == "Недостаточно данных для входа"

    @allure.title('Проверка получения ошибки при попытке авторизации под несуществующим пользователем')
    @allure.description('Проверяем, что при попытке авторизации под несуществующим пользователем приходит ошибка, '
                        'а также в ответе сервера получены верный код и тело.')
    def test_courier_not_authorized_with_not_existent_user(self):
        payload = {
            "login": "Volandemort98",
            "password": "Aa123456"
        }
        response = requests.post(f"{Urls.BASE_URL}/api/v1/courier/login", data=payload)
        assert response.status_code == 404 and response.json()["message"] == "Учетная запись не найдена"
        