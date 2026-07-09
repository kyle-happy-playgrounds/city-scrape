from spatula import URL
from platforms.civicclerk import BaseCivicClerkSearch

class TulsaAgendas(BaseCivicClerkSearch):
    source = URL("https://tulsacook.api.civicclerk.com/v1/Events")
    city_name = "Tulsa"
    state_name = "OK"

    start_date = ["2026-01-01"]
    end_date = ["2026-12-01"]
    target_departments = {
        "General": "24",
        "Board of County Commissioners": "26",
        "Budget Board": "32",
        "TC Public Facilities Authority": "48"
    }

def get_scraper():
    return TulsaAgendas()