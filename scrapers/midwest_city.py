from spatula import URL
from platforms.civicclerk import BaseCivicClerkSearch

class MidwestCityAgendas(BaseCivicClerkSearch):
    source = URL("https://midwestcityok.api.civicclerk.com/v1/Events")
    city_name = "Midwest City"
    state_name = "OK"

    start_date = ["2026-01-01"]
    end_date = ["2026-12-01"]
    target_departments = {
        "City Council": "26",
        "Park and Recreation Board": "34",
        "Planning Commission": "35"
    }

def get_scraper():
    return MidwestCityAgendas()