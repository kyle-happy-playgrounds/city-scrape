from spatula import URL
from platforms.civicclerk import BaseCivicClerkSearch

class BentonvilleAgendas(BaseCivicClerkSearch):
    source = URL("https://bentonvillear.api.civicclerk.com/v1/Events")
    city_name = "Bentonville"
    state_name = "AR"

    start_date = ["2026-01-01"]
    end_date = ["2026-12-01"]
    target_departments = {
        "City Council": "26",
        "Planning Commission": "27",
        "Parks & Recreation Advisory Board": "28"
    }

def get_scraper():
    return BentonvilleAgendas()