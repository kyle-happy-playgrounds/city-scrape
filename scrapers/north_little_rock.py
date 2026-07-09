from platforms.laserfiche import BaseLaserficheSearch
from spatula import URL

class NorthLittleRockAgendas(BaseLaserficheSearch):
    city_name = "North Little Rock"
    state_name = "AR"
    repo_name = "r-caf858ef"
    

    api_url = "https://portal.laserfiche.com/Portal/FolderListingService.aspx/GetFolderListing2"
    
    target_folders = [
            {
                "folder_id": 755671,
                "doc_type": "minutes",
                "description": "2026 City Council Minutes"
            }
        ]
    
def get_scraper():
    return NorthLittleRockAgendas()