from typing import List

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pyswip import Prolog

prolog = Prolog()
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
def version():
    return JSONResponse({'message': 'ok', 'version': '0.01'})


@app.get('/animals')
async def animals():
    animals = [animal['Animal'] for animal in list(prolog.query('animal(Animal)'))]
    return JSONResponse({'message': 'ok', 'animals': animals})


@app.get('/animals/{animal}/tips')
async def animal_tips(animal: str):
    tips = list(prolog.query(f'tip({animal}, Short, Long)'))
    return JSONResponse({'message': 'ok', 'animal': animal, 'tips': tips})


@app.get('/animals/{animal}/equipments')
async def animal_equipments(animal: str):
    equipments = [equipment['Equipment'] for equipment in list(prolog.query(f'equipment({animal}, Equipment)'))]
    return JSONResponse({'message': 'ok', 'animal': animal, 'equipments': equipments})


@app.get('/animals/{animal}/diseases')
async def animal_diseases(animal: str):
    diseases = list(prolog.query(f'disease({animal}, Disease, Description)'))
    return JSONResponse({'message': 'ok', 'animal': animal, 'diseases': diseases})


@app.get('/animals/{animal}/simptoms')
async def animal_simptoms(animal: str):
    simptoms = [simptom['Simptom'] for simptom in list(prolog.query(f'simptom({animal}, Disease, Simptom)'))]
    return JSONResponse({'message': 'ok', 'animal': animal, 'simptoms': simptoms})


@app.get('/animals/{animal}/{disease}/simptoms')
async def animal_simptoms_by_simptoms(animal: str, disease: str):
    simptoms = [simptom['Simptom'] for simptom in list(prolog.query(f"simptom({animal}, '{disease}', Simptom)"))]
    return JSONResponse({'message': 'ok', 'animal': animal, 'simptoms': simptoms})


@app.post('/animals/')
async def animal_diseases_by_simptoms(animal: str, simptoms: List[str]):
    diseases = []
    score = {}
    diseases_simptoms = {}

    for simptom in simptoms:
        diseases_from_simptom = [disease['Disease'] for disease in
                                 list(prolog.query(f"simptom({animal}, Disease, '{simptom}')."))]
        for disease in diseases_from_simptom:
            diseases_simptoms[disease] = [simptom] if diseases_simptoms.get(disease, None) is None else \
                diseases_simptoms[disease] + [simptom]

        diseases += diseases_from_simptom

    for disease in diseases:
        score[disease] = diseases.count(disease)

    return JSONResponse(
        {'message': 'ok', 'animal': animal, 'diseases_simptoms': diseases_simptoms, 'diseases': list(set(diseases)),
         'score': score})


if __name__ == '__main__':
    uvicorn.run("main:app", port=5000, log_level="info")
