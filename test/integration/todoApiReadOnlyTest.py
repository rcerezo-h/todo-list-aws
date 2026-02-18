import os
import json
import requests
import unittest

BASE_URL = os.environ.get("BASE_URL", "")

class TestApiReadOnly(unittest.TestCase):

    def test_api_listtodo_readonly(self):
        print("---------------------------------------")
        print("Starting - ReadOnly test List TODO")

        url = BASE_URL + "/todos"
        response = requests.get(url)

        self.assertEqual(response.status_code, 200, f"Error en GET {url}")

        data = response.json()

        # Aceptar ambos formatos:
        # 1) Lambda proxy: {"statusCode":200,"body":"[...]"}
        # 2) Respuesta directa: [...]
        if isinstance(data, dict) and "body" in data:
            todos = json.loads(data["body"])
        else:
            todos = data

        self.assertIsInstance(todos, list, "La respuesta no es una lista de TODOs")

        print("End - ReadOnly test List TODO")
