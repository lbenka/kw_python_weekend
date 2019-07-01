from typing import List
from urllib.parse import urljoin
from datetime import date

import attr
from requests_html import HTMLSession

from lb.modules.provider_base import Provider
from lb.data_classes.response_journey import ResponseJourney


@attr.s
class Arriva(Provider):
    s: HTMLSession = attr.ib(factory=HTMLSession)
    homepage: str = attr.ib(default="https://www.arriva.com.hr/en-us/")

    def get_routes(
        self, source: str = "Split", destination: str = "Zagreb", departure: date = None, arrival: date = None
    ) -> List[ResponseJourney]:
        payload = {
            "post-type": "shop",
            "currentstepnumber": "1",
            "search-from": source,
            "search-to": destination,
            "search-datetime": departure.strftime("%d.%m.%Y"),  # "22.10.2018."
            "search-datetime-fixed": "",
            "return-date": "",
            "search-datetime-open": "",
            "ticket-type": "oneway",
        }

        r = self.s.post(urljoin(self.homepage, "choose-your-journey"), data=payload)

        journeys: List[ResponseJourney] = []
        for e in r.html.xpath('//*[@id="departures-group"]/div[@class="row tab-info"]'):

            route_time = e.xpath('//*/div[@class="col-sm-3 polazak-dolazak"]')[0].text
            departure, arrival = route_time.replace("Departure - Arrival", "").split("\n")[0].split(" - ")
            j = ResponseJourney(
                departure_datetime=departure, arrival_datetime=arrival, source=source, destination=destination
            )

            route_prices = [
                p.text for p in e.xpath("//*[@class='btn btn-green btn-small btn-block visible-md visible-lg']")
            ]
            for price_raw in route_prices:
                price, currency = price_raw.split()

                j.price = price
                j.currency = currency

            journeys.append(j)

        return journeys
