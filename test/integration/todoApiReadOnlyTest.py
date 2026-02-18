import os
import requests

BASE_URL = os.environ.get("BASE_URL")


def test_list_todos_read_only():
        print("---------------------------------------")
            print("Starting - ReadOnly test List TODO")

                url = f"{BASE_URL}/todos"
                    response = requests.get(url, timeout=10)

                        print(f"Response status code: {response.status_code}")
                            print(f"Response body: {response.text}")

                                assert response.status_code == 200
                                    data = response.json()
                                        assert isinstance(data, list)

                                            print("End - ReadOnly test List TODO")


                                            def test_get_todo_read_only_if_exists():
                                                    print("---------------------------------------")
                                                        print("Starting - ReadOnly test Get TODO")

                                                            list_url = f"{BASE_URL}/todos"
                                                                list_response = requests.get(list_url, timeout=10)

                                                                    assert list_response.status_code == 200
                                                                        todos = list_response.json()

                                                                            if len(todos) > 0:
                                                                                        todo_id = todos[0]["id"]
                                                                                                get_url = f"{BASE_URL}/todos/{todo_id}"

                                                                                                        response = requests.get(get_url, timeout=10)

                                                                                                                print(f"GET Todo response: {response.status_code}")
                                                                                                                        print(f"GET Todo body: {response.text}")

                                                                                                                                assert response.status_code == 200
                                                                                                                                        todo = response.json()
                                                                                                                                                assert todo["id"] == todo_id

                                                                                                                                                    print("End - ReadOnly test Get TODO")

