from platforms.legistar import BaseLegistarSearch

class BrokenArrowAgendas(BaseLegistarSearch):
    source = "https://brokenarrow.legistar.com/Calendar.aspx"
    city_name = "Broken Arrow"
    state_name = "OK"

    target_years = ["2026"]
    target_departments = {
        "Planning Commission": "29298",
        "Broken Arrow City Council": "29289"
    }


def get_scraper():
    return BrokenArrowAgendas()