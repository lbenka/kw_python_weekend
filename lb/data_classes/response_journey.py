from pydantic import BaseModel
from datetime import datetime


class ResponseJourney(BaseModel):
    departure_datetime: datetime = None
    arrival_datetime: datetime = None
    source: str = None
    destination: str = None
    price: str = None
    currency: str = None
