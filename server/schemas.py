from datetime import date
from pydantic import BaseModel, ValidationError, validator
from typing import Optional


class Record(BaseModel):
    id: int
    country: str
    country_code: str
    population: Optional[int] = None 
    last_updated: str
    confirmed: int
    deaths : int
    recovered : int

    @validator('population')
    def size_is_some(cls, v):
        if v is None:
            return 0
        return float(v)

    class Config:
        orm_mode = True


