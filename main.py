from typing import List, Union

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pyswip import Prolog
from sql import db

prolog = Prolog()
prolog.consult('knowledge.pl')
from_prolog = False

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnimalSimptoms(BaseModel):
    animal: str
    simptoms: Union[List[str], None]


@app.get('/')
def version():
    return JSONResponse({'message': 'ok', 'version': '0.01'})


@app.get('/animals')
async def animals():
    if from_prolog:
        animals = [animal['Animal'] for animal in list(prolog.query('animal(Animal)'))]
    else:
        animals = db.get_animals()
    return JSONResponse({'message': 'ok', 'animals': animals})


@app.get('/animals/{animal}/tips')
async def animal_tips(animal: str):
    if from_prolog:
        tips = list(prolog.query(f'tip({animal}, Short, Long)'))
    else:
        tips = db.get_tips(animal)
    return JSONResponse({'message': 'ok', 'animal': animal, 'tips': tips})


@app.get('/animals/{animal}/equipments')
async def animal_equipments(animal: str):
    equipments = [equipment['Equipment'] for equipment in list(prolog.query(f'equipment({animal}, Equipment)'))]
    return JSONResponse({'message': 'ok', 'animal': animal, 'equipments': equipments})


@app.get('/animals/{animal}/diseases')
async def animal_diseases(animal: str):
    if from_prolog:
        diseases = list(prolog.query(f'disease({animal}, Disease, Description)'))
    else:
        diseases = db.get_diseases(animal)
    return JSONResponse({'message': 'ok', 'animal': animal, 'diseases': diseases})


@app.get('/animals/{animal}/simptoms')
async def animal_simptoms(animal: str):
    if from_prolog:
        simptoms = [simptom['Simptom'] for simptom in list(prolog.query(f'simptom({animal}, Disease, Simptom)'))]
    else:
        simptoms = db.get_simptoms(animal)

    simptoms = list(set(simptoms))
    simptoms.sort()
    return JSONResponse({'message': 'ok', 'animal': animal, 'simptoms': simptoms})


@app.get('/animals/{animal}/{disease}/simptoms')
async def animal_simptoms_of_disease(animal: str, disease: str):
    if from_prolog:
        simptoms = [simptom['Simptom'] for simptom in list(prolog.query(f"simptom({animal}, '{disease}', Simptom)"))]
    else:
        simptoms = db.get_simptoms_of_diseases(animal, disease)
    return JSONResponse({'message': 'ok', 'animal': animal, 'simptoms': simptoms})


@app.post('/animals')
async def animal_diseases_by_simptoms(param_animal_simptoms: AnimalSimptoms):
    animal = param_animal_simptoms.animal
    simptoms = param_animal_simptoms.simptoms

    if prolog:
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
    else:
        response = db.get_diseases_by_simptoms(animal, simptoms)
        response['message'] = 'ok'
        response['animal'] = animal

        return JSONResponse(response)



if __name__ == '__main__':
    uvicorn.run("main:app", port=5000, log_level="info")
