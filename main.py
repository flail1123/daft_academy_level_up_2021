from fastapi import FastAPI, Response, status
from hashlib import sha512
from pydantic import BaseModel
from datetime import *

app = FastAPI()
app.id = 0


@app.get("/")
def root_view():
    return {"message": "Hello world!"}


@app.post("/method")
def method(response: Response):
    response.status_code = status.HTTP_201_CREATED
    return {"method": "POST"}


@app.get("/method")
def method():
    return {"method": "GET"}


@app.put("/method")
def method():
    return {"method": "PUT"}


@app.delete("/method")
def method():
    return {"method": "DELETE"}


@app.options("/method")
def method():
    return {"method": "OPTIONS"}



@app.get("/auth")
def auth(password=None, password_hash=None, response: Response = None):
    if not password:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        print("401++")
        return
    hash_password = sha512(password.encode()).hexdigest()
    #print(password, password_hash, hash_password)
    if hash_password == password_hash:
        response.status_code = status.HTTP_204_NO_CONTENT
        print("204")
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        print("401")


class NameSurname(BaseModel):
    name: str
    surname: str

@app.post("/register")
def register(name_surname: NameSurname, response: Response):
    app.id += 1
    name = name_surname.name
    surname = name_surname.surname
    today = datetime.now()
    #print(today.strftime("%Y-%m-%d"))
    vaccination_date = today + timedelta(days=len(name) - name.count(" ") + len(surname))
    response.status_code = status.HTTP_201_CREATED
    return {
        "id": app.id,
        "name": name,
        "surname": surname,
        "register_date": today.strftime("%Y-%m-%d"),
        "vaccination_date": vaccination_date.strftime("%Y-%m-%d")
    }

'''
@app.get("/hello/{name}")
async def hello_name_view(name: str):
    return f"Hello {name}"


@app.get("/counter")
def counter():
    app.counter += 1
    return app.counter
'''
