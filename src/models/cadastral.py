from pydantic import BaseModel


class CadastralParams(BaseModel):
    cadastral_number: int
    latitude: float
    longitude: float