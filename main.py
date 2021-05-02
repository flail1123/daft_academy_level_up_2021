from fastapi import FastAPI, Response, status, Request, Cookie, Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from hashlib import sha512, sha256
from pydantic import BaseModel
from datetime import *
from typing import Optional
from fastapi.templating import Jinja2Templates
import secrets
from fastapi.responses import PlainTextResponse
from fastapi.responses import RedirectResponse

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
    for i in name + surname:
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
def patient(id: int, response: Response):
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
    correct_username = secrets.compare_digest(credentials.username, "stanleyjobson")
    correct_password = secrets.compare_digest(credentials.password, "swordfish")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username + "+" +credentials.password


@app.post("/login_session")
def login_session(response: Response, token: str = Depends(get_current_username)):
    response.status_code = status.HTTP_201_CREATED
    response.set_cookie(key="session_token", value=token)
    return


@app.post("/login_token")
def login_token(response: Response, token: str = Depends(get_current_username)):
    response.status_code = status.HTTP_201_CREATED
    return {"token": token}


def return_message(format, request, message):
    if format == "json":
        return {"message": message}
    elif format == "html":
        return templates.TemplateResponse("hello.html", {"message": message, request: request})
    else:
        return PlainTextResponse(message)


@app.get("/welcome_session")
def welcome_session(response: Response, request: Request, format: str = "", ads_id: Optional[str] = Cookie(None)):
    if ads_id != None and (ads_id != app.login_session_token or app.login_session_token == ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(ads_id),
            headers={"WWW-Authenticate": "Basic"},
        )
    response.status_code = status.HTTP_200_OK

    return return_message(format, request, "Welcome!")

@app.get("/welcome_token")
def welcome_token(response: Response, request: Request, format: str = "", token: str = ""):
    if token != None and (token != app.login_token_token or app.login_token_token == ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(token),
            headers={"WWW-Authenticate": "Basic"},
        )
    response.status_code = status.HTTP_200_OK
    return return_message(format, request, "Welcome!")



@app.delete("/logout_session")
def logout_session(response: Response, request: Request, format: str = "", ads_id: Optional[str] = Cookie(None)):
    if ads_id != app.login_session_token or app.login_session_token == "":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="session",
            headers={"WWW-Authenticate": "Basic"},
        )
    response.status_code = status.HTTP_303_SEE_OTHER
    app.login_session_token = ""
    return RedirectResponse("/logged_out?format="+str(format))

@app.delete("/logout_token")
def logout_token(response: Response, request: Request, format: str = "", token: str = ""):
    if token != app.login_token_token or app.login_token_token == "":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token",
            headers={"WWW-Authenticate": "Basic"},
        )
    response.status_code = status.HTTP_303_SEE_OTHER
    app.login_token_token = ""
    return RedirectResponse("/logged_out?format="+str(format))



@app.get("/logged_out")
def logged_out(response: Response, request: Request, format: str = ""):
    response.status_code = status.HTTP_200_OK
    return return_message(format, request, "Logged out!")
