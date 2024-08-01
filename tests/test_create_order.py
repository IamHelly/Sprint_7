import allure
import pytest
import requests
from data_order import DataCreateOrder
from urls import Urls


class TestCreateOrder:
    @pytest.mark.parametrize('color', [DataCreateOrder.color_black, DataCreateOrder.color_grey, DataCreateOrder.color_black_and_grey, DataCreateOrder.color_is_none])
    @allure.title('Проверка создания заказа с различными условиями выбора цвета')
    @allure.description('Проверка создания заказа: 1) с указанием одного из цветов — BLACK или GREY, 2) с указанием обоих цветов, '
                        '3) без указания цвета. Проверка, что тело ответа содержит track.')
    def test_create_order_with_different_colors(self, color):
        payload = {
            "firstName": DataCreateOrder.firstName,
            "lastName": DataCreateOrder.lastName,
            "address": DataCreateOrder.address,
            "metroStation": DataCreateOrder.metroStation,
            "phone": DataCreateOrder.phone,
            "deliveryDate": DataCreateOrder.deliveryDate,
            "rentTime": DataCreateOrder.rentTime,
            "color": color,
            "comment": DataCreateOrder.comment
        }
        response = requests.post(f"{Urls.BASE_URL}/api/v1/orders", json=payload)
        assert response.status_code == 201 and response.json()["track"] is not None
        print(response.json()["track"])