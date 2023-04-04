from pathlib import Path
from typing import List

import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load

from app import config as cfg

app = FastAPI(title='Predecir retraso de vuelos')

class Vuelo(BaseModel):
    aerolinea: int
    mes: int
    tipo_vuelo: int
    origen: int
    destino: int
    dia_semana: int

@app.on_event("startup")
def load_clf():
	app.model = load(Path('models', cfg.MODEL))

@app.get('/', summary='Inicio')
def home():
	return {'welcome': 'Home'}

@app.post('/predict-delay', summary='Predecir retraso')
def predict_delay(flights: List[Vuelo]):

	flight_arr = np.array([[
		v.aerolinea,
    	v.mes,
		v.tipo_vuelo,
		v.origen,
		v.destino,
		v.dia_semana] for v in flights])
	
	pr = app.model.predict_proba(flight_arr)

	preds = np.column_stack((np.argmax(pr, axis=1), np.max(pr, axis=1)))
	pred_dct = [{'pred':int(row[0]), 'prob':np.round(row[1], 3)} for row in preds]

	return pred_dct