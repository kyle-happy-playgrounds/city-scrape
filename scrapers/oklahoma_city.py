from spatula import URL
from platforms.primegov import BasePrimeGovArchived

class OklahomaCityAgendas(BasePrimeGovArchived):
    # Pass the API endpoint discovered in the Network tab
    source = URL("https://okc.primegov.com/api/v2/PublicPortal/ListArchivedMeetings?year=2026")
    
    city_name = "Oklahoma City"
    state_name = "OK"
    client_slug = "okc"

    target_committees = {
        "City Council": 1, 
        "Bond Advisory": 16, 
        "Park Commission": 70
    }

def get_scraper():
    return OklahomaCityAgendas()