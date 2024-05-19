from models.movie import Movie as MovieModel

class MovieService():
    #Asignamos un contructor para que cada vez se utilice el servicio se conecte a la base de datos
    def __init__(self, db) -> None:
        self.db = db
        
    def get_movies(self):
        results = self.db.query(MovieModel).all()
        return results