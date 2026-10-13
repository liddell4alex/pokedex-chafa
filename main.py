# Mi tarea xddd solo para probabr algo

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx

# Ruta de los templates
templates = Jinja2Templates(directory='templates')

# Instancia fastapi y pokeapi
app = FastAPI()
POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/?offset=20&limit=100"

# URL principal
@app.get("/")
def inicio(_request: Request):
    respuesta = httpx.get(POKEAPI_URL)  # Obtiene la pagina de pokemones
    # Verifica el estado de la petición 
    respuesta.raise_for_status()    # 200: bien, 404: error no encontrado, ...
    data = respuesta.json()

    pokemon = data['results']

    for p in pokemon:
        url = p['url'].rstrip("/")  # Elimina la ultima barra para facilitar extraccion del id
        p['id'] = int(url.split("/")[-1])   # Separo por / y tomo el ultimo elemento, este es el id
        p['imagen'] = (
            f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{p['id']}.png"
        )


    return templates.TemplateResponse(
        request=_request,
        name="index.html",
        context={"pokemon": pokemon}
    )