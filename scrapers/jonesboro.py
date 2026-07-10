from platforms.legistar import BaseLegistarSearch

class JonesboroAgendas(BaseLegistarSearch):
    source = "https://jonesboro.legistar.com/Calendar.aspx"
    city_name = "Jonesboro"
    state_name = "AR"

    target_years = ["2026"]
    target_departments = {
        "Metropolitan Area Planning Commission": "5950",
        "City Council": "5943"
    }

def get_scraper():
    return JonesboroAgendas()