import redis
import simplejson as json
from datetime import date

import maya
import requests
from bs4 import BeautifulSoup, NavigableString, Tag

redis_config = {
    "host": "188.166.60.144",
    "password": "akd89DSk23Kldl0ram29",
    "port": 6379,
}


redis_pool = redis.ConnectionPool(**redis_config)

my_prefix = "lukasbenka:{}"


def put_into_redis(key: str, value: dict) -> None:
    redis_con = redis.StrictRedis(connection_pool=redis_pool)
    redis_con.set(my_prefix.format(key), json.dumps(value))


def parse_time(base: str, time: str):
    parsed = base.split(".")
    formated = "{year}-{month}-{day}".format(
        day=parsed[0], month=parsed[1], year=2000 + int(parsed[2])
    )
    return maya.parse("{base}T{time}".format(base=formated, time=time)).datetime()


class Regiojet(object):
    def __init__(self):
        self.s = requests.Session()
        # getting cookie
        self.s.get("https://www.regiojet.cz")
        self.cities = self.get_destination() or self.fetch_destination()

    def get_destination(self) -> list:
        redis_con = redis.StrictRedis(connection_pool=redis_pool)

        p = redis_con.pipeline()
        for k in redis_con.keys(my_prefix.format("*")):
            p.get(k)

        cities = p.execute()
        cities = [json.loads(c) for c in cities]
        return cities

    def fetch_destination(self) -> list:
        destination = self.s.get(
            "https://www.studentagency.cz/data/wc/ybus-form/destinations-cs.json"
        ).json()

        # parsing cities
        cities = []
        for d in destination["destinations"]:
            cities.extend(d["cities"])

        for c in cities:
            put_into_redis(key=c["id"], value=c)

        return cities

    def find_city_id(self, city_name: str) -> int:
        city = self._find_city_id(city_name)
        if not city:
            self.fetch_destination()

        return self._find_city_id(city_name)

    def _find_city_id(self, city_name: str) -> int:
        for c in self.cities:
            if c["name"] == city_name:
                return c["id"]

    # this is how type hinting looks like
    def get_route(
        self,
        source: int = None,
        destination: int = None,
        departure: date = None,
        arrival: date = None,
    ):
        self.s.get(
            "https://jizdenky.regiojet.cz/Booking/from/{source}/to/{destination}/tarif/REGULAR/departure/{departure}/"
            "retdep/{arrival}/return/false".format(
                source=source,
                destination=destination,
                departure=departure.strftime("%Y%m%d"),
                arrival=departure.strftime("%Y%m%d"),
            )
        )
        r = self.s.get(
            "https://jizdenky.regiojet.cz/Booking/from/{source}/to/{destination}/tarif/REGULAR/departure/{departure}/"
            "retdep/{arrival}/return/false?"
            "0-1.IBehaviorListener.0-mainPanel-routesPanel&_=1519468178299".format(
                source=source,
                destination=destination,
                departure=departure.strftime("%Y%m%d"),
                arrival=departure.strftime("%Y%m%d"),
            )
        )
        return r

    @staticmethod
    def parse_single_item(item: Tag, base_date: str):
        price_for_bus = item.find_all("div", "col_price")
        price_for_train = item.find_all("div", "detailButton col_price_no_basket_image")
        if price_for_bus:
            real_price_cur_combo = price_for_bus[0].get_text().strip().split()
            price = real_price_cur_combo[0]
            currency = real_price_cur_combo[1]
        else:
            real_price_cur_combo = price_for_train[0].get_text().strip().split()
            price = real_price_cur_combo[0]
            currency = real_price_cur_combo[3]

        return {
            "departure": parse_time(
                base_date, item.find_all("div", "col_depart")[0].contents[0]
            ),
            "arrival": parse_time(
                base_date, item.find_all("div", "col_arival")[0].contents[0]
            ),
            "space": item.find_all("div", "col_space")[0].get_text().strip(),
            "price": price,
            "currency": currency,
        }

    def parse_routes(self, routes):
        soup = BeautifulSoup(routes.content, "html.parser")
        parent_of_routes = soup.find_all(
            "div", "item_blue blue_gradient_our routeSummary free"
        )[0].parent

        current_date = None
        routes = []
        for element in parent_of_routes.children:
            if isinstance(element, NavigableString):
                continue
            elif element.name == "h2":
                current_date = element.get_text().split()[1]
            elif (
                " ".join(element.attrs["class"])
                == "item_blue blue_gradient_our routeSummary free"
            ):
                routes.append(self.parse_single_item(element, current_date))
        return routes

    def get_route_prices(
        self,
        source: str,
        destination: str,
        departure: date = None,
        arrival: date = None,
    ):
        source_id = self.find_city_id(source)
        dest_id = self.find_city_id(destination)

        raw_routes = self.get_route(source_id, dest_id, departure, arrival)
        return self.parse_routes(raw_routes)


if __name__ == "__main__":
    regio = Regiojet()
    routes = regio.get_route_prices(
        source="Brno",
        destination="Praha",
        departure=date(2018, 2, 24),
        arrival=date(2018, 2, 24),
    )
    print(routes)
