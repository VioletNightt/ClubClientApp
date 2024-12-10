from datetime import datetime, timedelta

class BusinessLogic:
    def __init__(self, network_layer):
        self.network_layer = network_layer
        self.token = None
        self.user_role = None
        self.token_expiry = None
        self.login = None
        self.password = None

    def authenticate_user(self, login, password):
        if not self.login or not self.password:
            self.login = login
            self.password = password
        response = self.network_layer.post(
            "/auth/login",
            json={"login_or_email": login, "password": password}
        )
        if response["status"] == 200:
            self.token = response["data"]["access_token"]
            self.token_expiry = datetime.now() + timedelta(minutes=30)
            self.user_role = response["data"]["role"]
            self.network_layer.set_token(self.token)
            return {"success": True}
        return {"success": False, "error": response["detail"]}

    def refresh_token(self):
        """Перезапрашивает токен, используя сохраненные учетные данные."""
        if not self.login or not self.password:
            raise Exception("Необходим повторный вход: учетные данные отсутствуют.")

        if self.is_token_expired:
            self.authenticate_user(self.login, self.password)

    def is_token_expired(self):
        """Проверяет, истек ли токен."""
        return self.token_expiry is None or datetime.now() > self.token_expiry - timedelta(seconds=60)

    def register_user(self, login, email, phone, password):
        response = self.network_layer.post(
            "/auth/register_client",
            json={"login": login, "email": email, "phone": phone, "password": password}
        )

        if response["status"] == 200:
            return {"success": True, "message": response["data"]["message"]}
        return {"success": False, "error": response["detail"]}

    def get_available_computers(self):
        """Получает список доступных компьютеров или текущего арендованного."""
        self.refresh_token()
        try:
            headers = self.network_layer.get_headers()
            response = self.network_layer.get("/computers/available_or_rented", headers=headers)
            if response["status"] == 200:
                return response["data"]
            else:
                raise Exception(response["detail"])
        except Exception as e:
            raise Exception(f"Ошибка загрузки компьютеров: {str(e)}")

    def rent_computer(self, computer_id, duration, unit):
        """Арендует компьютер."""
        self.refresh_token()
        headers = self.network_layer.get_headers()
        params = {"computer_id": computer_id, "duration": f"{duration}{unit[0].lower()}"}
        response = self.network_layer.post("/computers/rent", headers=headers, params=params)
        if response["status"] != 200:
            raise Exception(response["detail"])
        return response["data"]


    def get_menu_items(self):
        """Получает список всех блюд меню ресторана."""
        self.refresh_token()
        headers = self.network_layer.get_headers()
        response = self.network_layer.get("/menu", headers=headers)
        if response["status"] == 200:
            return response["data"]
        else:
            raise Exception(response["detail"])

    def create_order(self, items):
        """Создает заказ для клиента."""
        self.refresh_token()
        headers = self.network_layer.get_headers()
        payload = {"items": items}
        response = self.network_layer.post("/orders", headers=headers, json=payload)
        if response["status"] == 200:
            return {"success": True, "message": response["data"]["message"]}
        return {"success": False, "error": response["detail"]}

    def get_user_orders(self):
        """Получает список заказов текущего клиента и обогащает данные о заказанных товарах."""
        self.refresh_token()
        headers = self.network_layer.get_headers()
        response = self.network_layer.get("/orders", headers=headers)
        if response["status"] != 200:
            raise Exception(response["detail"])

        orders = response["data"]

        menu_response = self.network_layer.get("/menu", headers=headers)
        if menu_response["status"] != 200:
            raise Exception(menu_response["detail"])

        menu_mapping = {
            item["id"]: {"name": item["name"], "price": item["price"]}
            for item in menu_response["data"]
        }

        for order in orders:
            for item in order["items"]:
                if item["item_id"] in menu_mapping:
                    item["name"] = menu_mapping[item["item_id"]]["name"]
                    item["price"] = menu_mapping[item["item_id"]]["price"]
                else:
                    item["name"] = "Неизвестный товар"
                    item["price"] = 0.0

        return orders
