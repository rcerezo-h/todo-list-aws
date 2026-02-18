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
        # La API suele devolver {"statusCode": 200, "body": "..."}
        self.assertIn("body", data, "La respuesta no contiene 'body'")
        todos = json.loads(data["body"])
        self.assertIsInstance(todos, list, "El body no es una lista JSON")

        print("End - ReadOnly test List TODO")
