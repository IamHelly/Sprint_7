import allure
import requests
from urls import Urls


class TestGetOrders:
    @allure.title('Проверка, что в тело ответа возвращается список заказов')
    def test_get_order_list(self):
        response = requests.get(f"{Urls.BASE_URL}/api/v1/orders")
        assert response.status_code == 200 and response.json()["orders"] is not None
