from requests_html import HTMLSession
from datetime import datetime

s = HTMLSession()


def get_destinations() -> dict:
    r = s.get("https://www.alsa.com/en/web/bus/home")
    r = s.get(
        "https://www.alsa.com/en/c/portal/layout?p_l_id=70167&p_p_cacheability=cacheLevelPage&p_p_id=JourneySearchPortlet_WAR_Alsaportlet&p_p_lifecycle=2&p_p_resource_id=JsonGetOrigins&locationMode=1&_=1536402460713"
    )

    return r.json()


def _get_routes(src: dict, dst: dict, when: datetime) -> dict:
    query = {
        "accessible": "0",
        "code": "",
        "p_p_state": "normal",
        "passengerType-4": "0",
        "_returnDate": "",
        "originStationNameId": src.get("name"),
        "destinationStationNameId": dst.get("name"),
        "originStationId": src.get("id"),
        "destinationStationId": dst.get("id"),
        "jsonAlsaPassPassenger": "",
        "departureDate": when.strftime("%m/%d/%Y"),
        "locationMode": "1",
        "p_p_col_count": "3",
        "passengerType-1": "1",
        "passengerType-2": "0",
        "passengerType-3": "0",
        "returnDate": "",
        "passengerType-5": "0",
        "travelType": "OUTWARD",
        "_departureDate": when.strftime("%m/%d/%Y"),
        "p_p_id": "PurchasePortlet_WAR_Alsaportlet",
        "numPassengers": "1",
        "regionalZone": "",
        "LIFERAY_SHARED_isTrainTrip": "false",
        "p_p_lifecycle": "1",
        "serviceType": "",
        "jsonVoucherPassenger": "",
        "_PurchasePortlet_WAR_Alsaportlet_javax.portlet.action": "searchJourneysAction",
        "promoCode": "",
        "p_p_mode": "view",
        "p_p_col_id": "column-1",
        "p_auth": "khT041BH",
    }
    r = s.get("https://www.alsa.com/en/web/bus/checkout", params=query)
    next_url = r.html.find("data-sag-journeys-component", first=True).attrs.get("sag-journeys-table-body-url")
    r = s.get(next_url)
    return r.json()


def get_routes(src_name: str, dst_name: str, when: datetime):
    dests = get_destinations()

    for d in dests:
        if src_name in d.get("name"):
            src = d
        if dst_name in d.get("name"):
            dst = d

    routes = _get_routes(src, dst, when)
    return routes
