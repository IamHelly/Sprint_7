import allure
import requests
from data_courier import DataCreateCourier
from urls import Urls


class TestsCreateCourier:
    @allure.title('Проверка создания курьера')
    @allure.description('Проверка, что поле id приходит в теле ответа сервера. По окончании теста тестовые данные удаляются')
    def test_create_courier(self):
        payload = {
            "login": DataCreateCourier.login,
            "password": DataCreateCourier.password,
            "firstName": DataCreateCourier.firstName
        }
        requests.post(f"{Urls.BASE_URL}/api/v1/courier", data=payload)
        response = requests.post(f"{Urls.BASE_URL}/api/v1/courier/login", data=payload)
        id_courier = response.json()["id"]
        assert response.status_code == 200 and id_courier is not None
        requests.delete(f"{Urls.BASE_URL}/api/v1/courier/{id_courier}")

    @allure.title('Проверка, что нельзя создать двух одинаковых курьеров')
    @allure.description('Создание два раза курьера с одинаковым набором данных. Проверка получения ошибки и соответствующего ответа сервера '
                        'при повторной отправке запроса на создание того же курьера. По окончании теста тестовые данные удаляются')
    def test_not_create_two_identical_couriers(self):
        payload = {
            "login": DataCreateCourier.login,
            "password": DataCreateCourier.password,
            "firstName": DataCreateCourier.firstName
        }
        requests.post(f"{Urls.BASE_URL}/api/v1/courier", data=payload)
        response_first = requests.post(f"{Urls.BASE_URL}/api/v1/courier/login", data=payload)
        id_courier = response_first.json()["id"]
        response_second = requests.post(f"{Urls.BASE_URL}/api/v1/courier", data=payload)
        assert response_second.status_code == 409 and response_second.json()["message"] == "Этот логин уже используется. Попробуйте другой."
        requests.delete(f"{Urls.BASE_URL}/api/v1/courier/{id_courier}")

    @allure.title('Проверка создания курьера с передачей в ручку всех обязательных полей и возврата ответа при успешном запросе')
    @allure.description('Проверка, что при заполнении обязательных полей происходит создание курьера, а также в ответе сервера '
                        'получены верный код и тело. По окончании теста тестовые данные удаляются')
    def test_create_courier_with_all_required_fields(self):
        payload = {
            "login": DataCreateCourier.login,
            "password": DataCreateCourier.password
        }
        response = requests.post(f"{Urls.BASE_URL}/api/v1/courier", data=payload)
        assert response.status_code == 201 and response.json()["ok"] is True
        response_for_delete = requests.post(f"{Urls.BASE_URL}/api/v1/courier/login", data=payload)
        id_courier = response_for_delete.json()["id"]
        requests.delete(f"{Urls.BASE_URL}/api/v1/courier/{id_courier}")

    @allure.title('Проверка получения ошибки при создания курьера, если одно из обязательных полей отсутствует')
    @allure.description('Проверка, что в случае отсутствия в запросе одного из обязательных полей при создании курьера приходит ошибка, '
                        'а также в ответе сервера получены верный код и тело')
    def test_create_courier_without_one_of_required_fields(self):
        payload = {
            "login": DataCreateCourier.login
        }
        response = requests.post(f"{Urls.BASE_URL}/api/v1/courier", data=payload)
        assert response.status_code == 400 and response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title('Проверка получения ошибки при создания курьера с логином, который уже есть')
    @allure.description('Проверка, что в случае создания курьера с уже существующим логином приходит ошибка, а также в ответе сервера '
                        'получены верный код и тело. По окончании теста тестовые данные удаляются')
    def test_create_courier_with_existing_login(self):
        payload_first = {
            "login": DataCreateCourier.login,
            "password": DataCreateCourier.password,
            "firstName": DataCreateCourier.firstName
        }
        payload_second = {
            "login": DataCreateCourier.login,
            "password": "Aa123456",
            "firstName": "Noname"
        }
        requests.post(f"{Urls.BASE_URL}/api/v1/courier", data=payload_first)
        response = requests.post(f"{Urls.BASE_URL}/api/v1/courier", data=payload_second)
        assert response.status_code == 409 and response.json()["message"] == "Этот логин уже используется. Попробуйте другой."
        response_for_delete = requests.post(f"{Urls.BASE_URL}/api/v1/courier/login", data=payload_first)
        id_courier = response_for_delete.json()["id"]
        requests.delete(f"{Urls.BASE_URL}/api/v1/courier/{id_courier}")

