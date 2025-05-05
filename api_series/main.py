from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from fastapi import FastAPI, HTTPException, status
from typing import List

app = FastAPI()

class Item(BaseModel):
    nome: str
    genero: str | None = None
    temporadas: int | None = None

series = {
    1: {"nome": "Pretty Little Liars", "genero": "Suspense", "temporadas": 7},
    2: {"nome": "New Girl", "genero": "Comedy", "temporadas": 7},
    3: {"nome": "Succession", "genero": "Drama", "temporadas": 4},
    4: {"nome": "The White Lotus", "genero": "Drama", "temporadas": 3},
    5: {"nome": "Friends", "genero": "Comedy", "temporadas": 10},
    6: {"nome": "The Office", "genero": "Comedy", "temporadas": 9},
    7: {"nome": "Gossip Girl", "genero": "Drama", "temporadas": 6},   
}

# Lista todas as séries cadastradas no banco de dados 
@app.get("/", description="Lista todas as séries cadastradas no banco de dados", status_code=status.HTTP_200_OK)
async def root():
    return series

# Pesquisa uma série com base em seu Id e a retorna
@app.get('/series/{item_id}', description="Busca uma série usando seu id como parâmetro", status_code=status.HTTP_200_OK)
async def serie(item_id: int):
    if item_id not in series:
        return {"Mensagem": "Série não encontrada"}
    return series[item_id]

# Cria uma nova série e adiciona no banco de dados
@app.post('/criar/', description="Cria um novo resgistro de série no banco de dados com os dados de nome, genero e número de temporadas", status_code=status.HTTP_201_CREATED)
async def criar(item: Item):
    serie_id = max(series.keys(), default=0) + 1
    series[serie_id] = item.dict()
    return f'Item criado'

# Atualiza os dados de uma série a partir de seu id que é passado como parâmetro
@app.put("/series/{item_id}", description="Atualiza os dados de uma série específica usando seu id como parâmetro", status_code=status.HTTP_200_OK)
async def atualizar_serie(item_id: int, item: Item, serie: str | None = None):
    serie_atualizada = {"item_id": item_id, **item.dict()}
    if serie:
        serie_atualizada.update({"serie": serie})
        return f'Série atualizada com sucesso {serie_atualizada}'
    if serie not in series:
        raise HTTPException(status_code=404, detail="Item not found")

# Deleta uma série usando seu id como parâmetro
@app.delete("/series/{item_id}", description="Deleta uma série específica do banco de dados usando seu id como prâmetro", status_code=status.HTTP_200_OK)
async def deletar_serie(item_id: int):
    if item_id in series:
        del series[item_id]
        return f"Série {item_id} excluída com sucesso"
    return f"Série {item_id} não foi encontrada"
