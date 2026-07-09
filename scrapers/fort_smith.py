from spatula import URL
from platforms.granicus import BaseGranicusRSSList

class FortSmithAgendas(BaseGranicusRSSList):
    source = URL("https://fortsmithar.granicus.com/ViewPublisherRSS.php?view_id=4&mode=agendas")
    
    city_name = "Fort Smith"
    state_name = "AR"

    target_departments = [
        "Parks and Recreation Commission",
        "Planning Commission and Board of Zoning Adjustment"
    ]
    target_years = ["2026"]

def get_scraper():
    return FortSmithAgendas()