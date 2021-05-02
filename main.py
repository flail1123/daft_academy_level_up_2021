from fastapi import FastAPI, Response, status, Request, Cookie, Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from hashlib import sha512, sha256
from pydantic import BaseModel
from datetime import *
from fastapi.templating import Jinja2Templates
import secrets

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.id = 0
app.patients = []
app.secret_key = "asdjfkljbaodifjhioudfyahhhghyhhhhihrphaoudfshgryerawdioghperadghper"
app.login_session_token = ""
app.login_token_token = ""
security = HTTPBasic()

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
        return
    hash_password = sha512(password.encode()).hexdigest()
    if hash_password == password_hash:
        response.status_code = status.HTTP_204_NO_CONTENT
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


class NameSurname(BaseModel):
    name: str
    surname: str

@app.post("/register")
def register(name_surname: NameSurname, response: Response):
    app.id += 1
    name = name_surname.name
    surname = name_surname.surname
    today = datetime.now()
    days = 0
    for i in name+surname:
        if 65 <= ord(i) < 65 + 26 or 97 <= ord(i) < 97 + 26 or ord(i) == 45:
            days += 1
    vaccination_date = today + timedelta(days=days)
    response.status_code = status.HTTP_201_CREATED
    result = {
        "id": app.id,
        "name": name,
        "surname": surname,
        "register_date": today.strftime("%Y-%m-%d"),
        "vaccination_date": vaccination_date.strftime("%Y-%m-%d")
    }
    app.patients.append(result)
    return result

@app.get("/patient/{id}")
def patient(id : int, response: Response):
    if id < 1:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return
    if id <= app.id:
        return app.patients[id - 1]
    response.status_code = status.HTTP_404_NOT_FOUND



@app.get("/hello")
def hello(request: Request):
    current_date = date.today().strftime("%Y-%m-%d")
    return templates.TemplateResponse("hello.html", {"current_date": current_date, "request": request})



def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    return correct_username and correct_password


@app.post("/login_session")
def login_session(response: Response):
    credentials = Depends(security)
    if credentials.username != "4dm1n" or credentials.password != "NotSoSecurePa$$":
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return
    response.status_code = status.HTTP_201_CREATED
    response.set_cookie(key="session_token", value="fake-cookie-session-value")
    return


@app.post("/login_token")
def login_token(response: Response):
    credentials = Depends(security)
    if credentials.username != "4dm1n" or credentials.password != "NotSoSecurePa$$":
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return
    response.status_code = status.HTTP_201_CREATED
    return {"token": "fake-cookie-session-value"}


















