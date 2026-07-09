from spatula import URL
from platforms.civicclerk import BaseCivicClerkSearch

class LawtonAgendas(BaseCivicClerkSearch):
    source = URL("https://lawtonok.api.civicclerk.com/v1/Events")
    city_name = "Lawton"
    state_name = "OK"

    start_date = ["2026-01-01"]
    end_date = ["2026-12-01"]
    target_departments = {
        "City Council": "26",
        "City Planning Commission": "25",
        "Parks and Recreation Commission": "68"
    }

def get_scraper():
    return LawtonAgendas()