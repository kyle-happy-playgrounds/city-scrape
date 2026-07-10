from platforms.laserfiche import BaseLaserficheSearch
from spatula import URL

class OwassoAgendas(BaseLaserficheSearch):
    city_name = "Owasso"
    state_name = "OK"
    repo_name = "City-of-Owasso"
    

    api_url = "https://weblink.cityofowasso.com/WebLink/FolderListingService.aspx/GetFolderListing2"
    
    target_folders = [
            {
                "folder_id": 310006,
                "doc_type": "minutes",
                "description": "2026 City Council Minutes",
                "department": "City Council"
            },
            {
                "folder_id": 310004, 
                "doc_type": "agenda",
                "description": "2026 City Council Agendas",
                "department": "City Council"
            },
            {
                "folder_id": 310091, 
                "doc_type": "agenda",
                "description": "2026 Planning Commission Agenda",
                "department": "Planning Commission"
            },
            {
                "folder_id": 310785, 
                "doc_type": "minutes",
                "description": "2026 Planning Commission Agenda",
                "department": "Planning Commission"
            }
        ]
    
def get_scraper():
    return OwassoAgendas()