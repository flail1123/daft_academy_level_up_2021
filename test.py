import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

'''
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.parametrize("name", ["Zenek", "Marek", "Alojzy Niezdąży"])
def test_hello_name(name):
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.text == f'"Hello {name}"'


def test_counter():
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == "1"
    # 2nd Try
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == "2"


def test_register():
    response = client.post(f"/register")
    print(response)
'''


def test_logout():
    response = client.post(f"/login_token")
    response = client.delete(f"/logout_token?token=4dm1n+NotSoSecurePa$$")
    print(response)

test_logout()