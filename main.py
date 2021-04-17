from fastapi import FastAPI, Response, status
from hashlib import sha512

app = FastAPI()
app.counter = 0


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
def auth(password, password_hash, response: Response):
    if not password:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return
    hash_password = sha512(password.encode()).hexdigest()
    #print(password, password_hash, hash_password)
    if hash_password == password_hash:
        response.status_code = status.HTTP_204_NO_CONTENT
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


'''
@app.get("/hello/{name}")
async def hello_name_view(name: str):
    return f"Hello {name}"


@app.get("/counter")
def counter():
    app.counter += 1
    return app.counter
'''
