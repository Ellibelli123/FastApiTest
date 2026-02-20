from fastapi import FastAPI

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})



@app.get("/")
def root():
    return {"status": "ok", "message": "Hello FastAPI"}


@app.get("/magnus")
def root():
    return {"status": "ok", "message": "Magnus Hello FastAPI"}


@app.get("/bookings")
def root():
    return {"status": "ok", "message": "Magnus Hello FastAPI"}


@app.put("/bookings")
def root():
    return {"status": "ok", "message": "Magnus Hello FastAPI"}
