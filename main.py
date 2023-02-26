from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pyswip import Prolog

prolog = Prolog()
# print(prolog.assertz("father(michael,john)"))
prolog.consult('knowledge.pl')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return JSONResponse({'message': 'Hello World'})


@app.get('/animals')
async def animals():
    animals = [animal['Animal'] for animal in list(prolog.query('animal(Animal)'))]
    return JSONResponse({'message': 'ok', 'animals': animals})


@app.get('/animals/{animal}/tips')
async def animal_tips(animal: str):
    tips = list(prolog.query(f'tip({animal}, Short, Long)'))
    return JSONResponse({'message': 'ok', 'animal': animal, 'tips': tips})


@app.get('animals/{animal}/diseases')
async def animal_diseases(animal: str):
    diseases = [disease['Disease'] for disease in list(prolog.query(f'disease({animal}, Disease'))]
    return JSONResponse({'message': 'ok', 'animal': animal, 'diseases': diseases})


if __name__ == '__main__':
    uvicorn.run("main:app", port=5000, log_level="info")
