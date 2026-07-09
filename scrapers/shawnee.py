from spatula import URL
from platforms.civicclerk import BaseCivicClerkSearch

class ShawneeAgendas(BaseCivicClerkSearch):
    source = URL("https://shawneeok.api.civicclerk.com/v1/Events")
    city_name = "Shawnee"
    state_name = "OK"

    start_date = ["2026-01-01"]
    end_date = ["2026-12-01"]
    target_departments = {
        "Shawnee Beautification, Parks, and Recreation Committee": "30",
        "Planning Commission": "35"
    }

def get_scraper():
    return ShawneeAgendas()