from spatula import Page, JsonListPage, NullSource, URL
from core.data_models import PublicDocument
import dataclasses
import json
import re
from datetime import datetime

class BaseLaserficheSearch(Page):
    source = NullSource()

    def process_page(self):
        api_url = getattr(self, "api_url", "")
        repo_name = getattr(self, "repo_name", "")
        target_folders = getattr(self, "target_folders", [])

        for folder in target_folders:
            payload = {
                "repoName": repo_name,
                "folderId": folder["folder_id"],
                "getNewListing": True,
                "start": 0,
                "end": 100, 
                "sortColumn": "",
                "sortAscending": True
            }

            post_url = URL(
                api_url, 
                method="POST", 
                data=json.dumps(payload), 
                headers={"Content-Type": "application/json"}
            )

            list_page = BaseLaserficheApiBrowse(post_url)
            
            list_page.city_name = getattr(self, "city_name", "Unknown")
            list_page.state_name = getattr(self, "state_name", "Unknown")
            list_page.repo_name = repo_name
            list_page.doc_type_mapping = folder.get("doc_type", "unknown")
            
            list_page.department = folder.get("department", "unknown")
            yield list_page


class BaseLaserficheApiBrowse(JsonListPage):
    def get_source_from_input(self): 
        return self.input
    def process_page(self):

            response_data = self.data.get("data") or {}
            results = response_data.get("results") or []
            
            for item in results:
                if not item:
                    continue

                processed = self.process_item(item)
                if processed:
                    yield processed

    def process_item(self, item):
        item_name = item.get("name", "")
        doc_id = item.get("entryId")
        
        if not item_name or not doc_id:
            return None
            
        base_url = self.source.url.split("FolderListingService.aspx")[0]
        repo_name = getattr(self, "repo_name", "") 
        
        doc_url = f"{base_url}DocView.aspx?id={doc_id}&repo={repo_name}&openpdf=true"
        
        doc_type = getattr(self, "doc_type_mapping", "unknown")
        if "agenda" in item_name.lower(): doc_type = "agenda"
        elif "minutes" in item_name.lower(): doc_type = "minutes"
        elif "packet" in item_name.lower(): doc_type = "agenda_packet"
        
        return dataclasses.asdict(PublicDocument(
            title=item_name,
            date_published=self._extract_date(item_name),
            city=getattr(self, "city_name", "Unknown"),
            state=getattr(self, "state_name", "Unknown"),
            platform="laserfiche",
            department=getattr(self, "department", "unknown"),
            documents={doc_type: doc_url}
        ))

    def _extract_date(self, text: str) -> str:
        iso_match = re.search(r'\d{4}[-.]\d{2}[-.]\d{2}', text)
        if iso_match: return iso_match.group(0).replace(".", "-")
            
        us_match = re.search(r'\b(\d{1,2})[-/.](\d{1,2})[-/.](\d{2,4})\b', text)
        if us_match:
            try:
                m, d, y = us_match.groups()
                y_int = int(y)
                if len(y) == 2:
                    y_int += 2000
                return datetime(y_int, int(m), int(d)).date().isoformat()
            except ValueError:
                pass
        return ""