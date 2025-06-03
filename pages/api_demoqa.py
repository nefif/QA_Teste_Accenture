# pages/api_demoqa.py

import requests

class DemoQAAPI:
    BASE_URL = "https://demoqa.com"

    @staticmethod
    def criar_usuario(username: str, password: str) -> requests.Response:
        """
        POST /Account/v1/User
        Body: { "userName": username, "password": password }
        """
        url = f"{DemoQAAPI.BASE_URL}/Account/v1/User"
        return requests.post(url, json={"userName": username, "password": password})

    @staticmethod
    def gerar_token(username: str, password: str) -> requests.Response:
        """
        POST /Account/v1/GenerateToken
        Body: { "userName": username, "password": password }
        """
        url = f"{DemoQAAPI.BASE_URL}/Account/v1/GenerateToken"
        return requests.post(url, json={"userName": username, "password": password})

    @staticmethod
    def verificar_autorizacao(token: str) -> requests.Response:
        """
        GET /Account/v1/Authorized
        Header: Authorization: Bearer <token>
        """
        url = f"{DemoQAAPI.BASE_URL}/Account/v1/Authorized"
        headers = {"Authorization": f"Bearer {token}"}
        return requests.get(url, headers=headers)

    @staticmethod
    def listar_livros() -> requests.Response:
        """
        GET /BookStore/v1/Books
        """
        url = f"{DemoQAAPI.BASE_URL}/BookStore/v1/Books"
        return requests.get(url)

    @staticmethod
    def adicionar_livros(user_id: str, token: str, isbns: list) -> requests.Response:
        """
        POST /BookStore/v1/Books
        Header: Authorization: Bearer <token>
        Body: { "userId": user_id, "collectionOfIsbns": [ {"isbn": isbn1}, {"isbn": isbn2} ] }
        """
        url = f"{DemoQAAPI.BASE_URL}/BookStore/v1/Books"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "userId": user_id,
            "collectionOfIsbns": [{"isbn": i} for i in isbns]
        }
        return requests.post(url, headers=headers, json=payload)

    @staticmethod
    def detalhes_usuario(user_id: str, token: str) -> requests.Response:
        """
        GET /Account/v1/User/{user_id}
        Header: Authorization: Bearer <token>
        """
        url = f"{DemoQAAPI.BASE_URL}/Account/v1/User/{user_id}"
        headers = {"Authorization": f"Bearer {token}"}
        return requests.get(url, headers=headers)
