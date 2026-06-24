import requests


BASE_URL = "http://127.0.0.1:8000"


def test_health_endpoint():
    response = requests.get(f"{BASE_URL}/health", timeout=10)

    print("Health status code:", response.status_code)
    print("Health response:", response.json())

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ask_endpoint():
    payload = {
        "question": "What library services are available to students?"
    }

    response = requests.post(f"{BASE_URL}/ask", json=payload, timeout=80)

    print("Ask status code:", response.status_code)
    print("Ask response:", response.json())

    assert response.status_code == 200
    assert "answer" in response.json()
    assert len(response.json()["answer"]) > 0


def test_empty_question_returns_400():
    payload = {"question": "   "}

    response = requests.post(f"{BASE_URL}/ask", json=payload, timeout=10)

    print("Empty-question status code:", response.status_code)
    print("Empty-question response:", response.json())

    assert response.status_code == 400
    assert "detail" in response.json()


if __name__ == "__main__":
    test_health_endpoint()
    test_ask_endpoint()
    test_empty_question_returns_400()
    print("All API tests passed successfully.")
