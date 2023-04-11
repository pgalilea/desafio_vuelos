
from typing import Literal

from pydantic import BaseModel, conint

class Vuelo(BaseModel):
	"Schema en bruto"
	aerolinea: str
	mes: conint(ge=1, le=12)
	tipo_vuelo: Literal['I', 'N']
	origen: str
	destino: str
	dia_semana: Literal['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
	temp_alta: Literal[0, 1]

class VueloFeat(BaseModel):
	"Schema transformado en features, listo para ingresar al modelo"
	aerolinea: int
	mes: conint(ge=1, le=12)
	tipo_vuelo: int
	origen: int
	destino: int
	dia_semana: int
	temp_alta: Literal[0, 1]

