from datetime import date
import attr
import requests
from typing import List 

from lb.data_classes.response_journey import ResponseJourney


@attr.s
class Provider:
    def get_routes(
        self,
        source: str = "Brno",
        destination: str = "Praha",
        departure: date = date(2019, 7, 24),
        arrival: date = date(2019, 7, 24),
    ) -> List[ResponseJourney]:
        raise NotImplementedError
