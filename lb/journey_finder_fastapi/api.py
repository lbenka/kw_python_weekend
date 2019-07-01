from fastapi import FastAPI
from datetime import datetime, timedelta
from typing import List

from lb.modules.fetch import fetch_provider
from lb.data_classes.response_journey import ResponseJourney

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/search/", response_model=List[ResponseJourney])
def get_routes_from_site(src: str, dst: str, when: str, provider: str = "regiojet"):
    when_parsed = datetime.strptime(when, "%Y/%m/%d")
    provider_class = fetch_provider(provider)
    routes = provider_class().get_routes(
        source=src, destination=dst, departure=when_parsed, arrival=when_parsed + timedelta(days=1)
    )
    return routes
