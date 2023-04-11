from pathlib import Path
from typing import List

import numpy as np
from fastapi import FastAPI
from joblib import load

from app.models import Vuelo, VueloFeat
from app import config as cfg

app = FastAPI(title='Predecir retraso de vuelos')

@app.on_event("startup")
def load_clf():
	app.model = load(Path('models', cfg.MODEL))
	app.feat_map = load(Path('models', cfg.FEAT_MAP))

@app.get('/', summary='Inicio')
def home():
	return {'welcome': 'Home'}

@app.post('/predict-delay', summary='Predecir retraso')
async def predict_delay(flights: List[VueloFeat]):
	"""Endpoint para realizar predicción de retraso."""

	flight_arr = np.array([[
		v.aerolinea,
		v.mes,
		v.tipo_vuelo,
		v.origen,
		v.destino,
		v.dia_semana,
		v.temp_alta] for v in flights])
	
	pr = app.model.predict_proba(flight_arr)

	preds = np.column_stack((np.argmax(pr, axis=1), np.max(pr, axis=1)))
	pred_dct = [{'pred':int(row[0]), 'prob':np.round(row[1], 3)} for row in preds]

	return pred_dct

@app.post('/feature-extract', summary='Feature extraction')
async def feture_extract(flights: List[Vuelo]) -> List[VueloFeat]:
	"""
	Endpoint para transformar información de un vuelo antes de realizar la predicción
	
	Payload entrada de ejemplo:

	[{
		"aerolinea": "Grupo LATAM",
		"mes": 12,
		"tipo_vuelo": "I",
		"origen": "Santiago",
		"destino": "Miami",
		"dia_semana": "Lunes",
		"temp_alta": 0
	},
	{
		"aerolinea": "Sky Airline",
		"mes": 4,
		"tipo_vuelo": "N",
		"origen": "Santiago",
		"destino": "Puerto Montt",
		"dia_semana": "Sabado",
		"temp_alta": 1
	}]
	"""

	flight_mpd = [VueloFeat(**{
		'aerolinea': app.feat_map['aerolinea'].transform([v.aerolinea])[0],
		'mes': v.mes,
		'tipo_vuelo': app.feat_map['tipo_vuelo'].transform([v.tipo_vuelo])[0],
		'origen': app.feat_map['origen'].transform([v.origen])[0],
		'destino': app.feat_map['destino'].transform([v.destino])[0],
		'dia_semana': app.feat_map['dia_semana'].transform([v.dia_semana])[0],
		'temp_alta': v.temp_alta}) for v in flights]
	
	return flight_mpd
