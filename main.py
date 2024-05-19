from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token
from config.database import engine, Base
from routers.movie import movie_router

app = FastAPI()
#Asiganmos nombre y version a la documentacion
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.3"

#Inlcuimos las rutas de las peliculas
app.include_router(movie_router)

#BASE DE DATOS
#creamos una bd
Base.metadata.create_all(bind=engine)

    
class User(BaseModel):
    email: str
    password: str


#podemos agrupar rutas por etiqueta (tags)
@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello PYTHON :)</h1>')

#Ruta para el inicio de sesion
@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.__dict__)
    return JSONResponse(status_code=200, content=token)



