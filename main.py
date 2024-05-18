from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel

app = FastAPI()
#Asiganmos nombre y version a la documentacion
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.3"

#BASE DE DATOS
#creamos una bd
Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    #este metodo devolvera el token generado,utilizando HTTPBearer
    async def __call__(self, request: Request):
        #devuelve las creenciales del usuario
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales Invalidas")
        

class User(BaseModel):
    email: str
    password: str

#esquema de datos
class Movie(BaseModel):
    #puede ser un campo opcional y a la vez entero
    id: Optional[int] = None
    title: str = Field(max_length=15, min_length=5)
    overview: str = Field(max_length=50, min_length=15)
    #con la abreviatura "le" se especifica que el numero sea menor a 2024
    year: int = Field(le=2024)
    rating: float = Field(ge=1, le=10) #ge: mayor o igual que, le: menor o igual que
    category: str = Field(min_lenght = 5, max_lengh = 15)
    
    #creamos un diccionario de ejemplo y lo genera en la documentacion
    model_config = {
        "json_schema_extra": {
                "examples": [
                {
                    'id': 1,
                    'title' : 'Crepusculo',
                    'overview' : 'The twilight is almost better than sunday',
                    'year' : 2022,
                    'rating' : 9.5,
                    'category' : 'Phantasy'
                }
            ]
        }
    }

#creamos una lista
movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
    
    {
        "id": 2,
        "title": "Goku Batalla de dioses",
        "overview": "goku y vegeta se aman",
        "year": "2009",
        "rating": 7.8,
        "category": "aventura"
    }
]

#podemos agrupar rutas por etiqueta (tags)
@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello</h1>')

#Ruta para el inicio de sesion
@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.__dict__)
    return JSONResponse(status_code=200, content=token)

#Ruta protegida
@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

#ruta con parametro y validacion, validamos el id que debe estar en el rango del 1 al 100
@app.get('/movie/{id}', tags=['movies'])
def get_movie_id(id: int = Path(ge=1, le=100)):
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(content="No existe esa movie")
        
#parametros query
#Asignamos "/" al final para indicar que necesitamos un parametro query
@app.get('/movies/', tags=['movies'], status_code=200)

#Cuando asignamos una funcion con parametro y en la ruta no se asigna, automaticamente FastAPI lo toma como parametro query
def get_movies_by_category(category: str = Query(min_length=5, max_length=15), year: int = Query(le= 2024)):
    for item in movies:
        if item["category"] == category:
            return JSONResponse(status_code=200, content=item)
    return JSONResponse(status_code=404, content="No hay movies con esa categoria")

#Metodo POST
@app.post('/movies', tags=['movies'], status_code=201)
#El body() indica que van hacer parametros para el cuerpo de la peticion y no se detectan como parametros query

#utiiizamos el esquema
def create_movie(movie: Movie):
    #insertamos un diccionarion con append (datos de la pelicula)
    movies.append(movie.model_dump())
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la pelicula"})

#metodo PUT
@app.put('/movies/{id}', tags=['movies'], status_code=200)

def update_movie(id: int, movie: Movie):
    for item in movies:
        if item['id'] == id:
            item['id'] = id
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la pelicula"})

#Ruta DELETE
@app.delete('/movies/{id}', tags=['movies'], status_code=200)
def delete_movie(id: int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la pelicula"})

