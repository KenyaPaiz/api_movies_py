from jwt import encode, decode

#Creamos un token y recibimos un diccionario
def create_token(data: dict):
    #asignamos lo que se va recibir (data), la llave y el algoritmo para generar el token
    token: str = encode(payload=data, key="my_secret_key", algorithm="HS256")
    return token


#Validar token y retornara un diccionario
def validate_token(token: str) -> dict:
    #decodificamos el token
    data: dict = decode(token, key="my_secret_key", algorithms=["HS256"])
    return data
    