from spatula import URL
from platforms.civicclerk import BaseCivicClerkSearch

class FayetteVilleAgendas(BaseCivicClerkSearch):
    source = URL("https://fayettevillear.api.civicclerk.com/v1/Events")
    city_name = "Fayetteville"
    state_name = "AR"

    start_date = ["2026-01-01"]
    end_date = ["2026-12-01"]
    target_departments = {
        "City Council": "26",
        "Planning Commission": "27",
        "Parks and Recreation Advisory Board": "47"
    }

def get_scraper():
    return FayetteVilleAgendas()