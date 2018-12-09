from requests_html import HTMLSession

# Helpfull -> look it up
from urllib.parse import urljoin

from typing import List
import attr


@attr.s
class ResponseJourney:
    departure_datetime = attr.ib(default=None)
    arrival_datetime = attr.ib(default=None)
    source = attr.ib(default=None)
    destination = attr.ib(default=None)
    price = attr.ib(default=None)
    currency = attr.ib(default=None)


class ArrivaClient:
    homepage = "https://www.arriva.com.hr/en-us/"
    s = HTMLSession()

    def get_journeys(self, source: str = "Split", destination: str = "Zagreb", departure: str = "22.10.2018."):
        payload = {
            "post-type": "shop",
            "currentstepnumber": "1",
            "search-from": source,
            "search-to": destination,
            "search-datetime": departure,
            "search-datetime-fixed": "",
            "return-date": "",
            "search-datetime-open": "",
            "ticket-type": "oneway",
        }

        r = self.s.post(urljoin(self.homepage, "choose-your-journey"), data=payload)

        journeys: List[ResponseJourney] = []

        route_times = [
            e.text for e in r.html.find("#departures-group > div.row.tab-info > div.col-sm-3.polazak-dolazak")
        ]
        for route in route_times:
            departure, arrival = route.replace("Departure - Arrival", "").split("\n")[0].split(" - ")

            j = ResponseJourney(
                departure_datetime=departure, arrival_datetime=arrival, source=source, destination=destination
            )
            journeys.append(j)

        route_prices = [
            e.text for e in r.html.xpath("//*[@class='btn btn-green btn-small btn-block visible-md visible-lg']")
        ]
        for index, route in enumerate(route_prices):
            price, currency = route.split()

            journeys[index].price = price
            journeys[index].currency = currency

        return [attr.asdict(j) for j in journeys]


if __name__ == "__main__":
    journeys = ArrivaClient().get_journeys()
    for j in journeys:
        print(j)
