from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

class Item(BaseModel):
    nome: str
    genero: str | None = None
    temporadas: int | None = None

series = {
    1: {"nome": "Pretty Little Liars", "gênero": "Suspense", "temporadas": 7},
    2: {"nome": "New Girl", "gênero": "Comedy", "temporadas": 7},
    3: {"nome": "Succession", "gênero": "Drama", "temporadas": 4},
    4: {"nome": "The White Lotus", "gênero": "Drama", "temporadas": 3},
    5: {"nome": "Friends", "gênero": "Comedy", "temporadas": 10},
    6: {"nome": "The Office", "gênero": "Comedy", "temporadas": 9},
    7: {"nome": "Gossip Girl", "gênero": "Drama", "temporadas": 6},   
}

@app.get("/")
async def root():
    return series

class Series_id(int, Enum):
    PLL = 1
    newgirl = 2
    succession = 3
    twl = 4
    friends = 5
    theoffice = 6
    gossipgirl = 7

@app.get("/pesquisa/{pesquisa_id}", status_code=status.HTTP_200_OK)
async def busca_series(pesquisa_id: int):
    if pesquisa_id.value == "1":
        return {"Pretty Little Liars"}
    if pesquisa_id.value == "2":
        return {"New girl"}
    if pesquisa_id.value == "3":
        return {"Succession"}
    if pesquisa_id.value == "4":
        return {"The White Lotus"}
    if pesquisa_id.value == "5":
        return {"Friends"}
    if pesquisa_id.value == "6":
        return {"The Office"}
    if pesquisa_id.value == "7":
        return {"Gossip Girl"}

@app.get('/series/{item_id}', status_code=status.HTTP_200_OK)
async def serie(item_id: int):
    if item_id not in series:
        return {"Mensagem": "Série não encontrada"}
    return series[item_id]

@app.post('/criar/', status_code=status.HTTP_201_CREATED)
async def criar(item: Item):
    serie_id = max(series.keys(), default=0) + 1
    series[serie_id] = item.dict()
    return f'Item criado'

