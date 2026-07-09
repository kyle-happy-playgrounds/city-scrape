from spatula import URL
from platforms.civicclerk import BaseCivicClerkSearch

class PryorAgendas(BaseCivicClerkSearch):
    source = URL("https://pryorcreekok.api.civicclerk.com/v1/Events")
    city_name = "Pryor"
    state_name = "OK"

    start_date = ["2026-01-01"]
    end_date = ["2026-12-01"]
    target_departments = {
        "City Council": "26",
        "Park Board": "32",
        "Planning Commission": "35"
    }

def get_scraper():
    return PryorAgendas()