from spatula import JsonListPage
from core.data_models import PublicDocument
import dataclasses

class BasePrimeGovArchived(JsonListPage):
    def process_page(self):

        meeting_array = self.data if isinstance(self.data, list) else []

        target_committees = getattr(self, "target_committees", {})
        self.reverse_committees = {v: k for k, v in target_committees.items()}
        
        for item in meeting_array:
            parsed_doc = self.process_item(item)
            if parsed_doc:
                yield parsed_doc

    def process_item(self, item):
        committee_id = item.get("committeeId")
        
        if self.reverse_committees and committee_id not in self.reverse_committees:
            return None
            
        department_name = self.reverse_committees.get(committee_id, "Unknown")

        title = item.get("title", "Unknown").strip()
        
        date_time_str = item.get("dateTime", "")
        date_published_iso = date_time_str.split("T")[0] if "T" in date_time_str else date_time_str

        found_documents = {}
        client_slug = getattr(self, "client_slug", "")
        
        pdf_base_url = f"https://{client_slug}.primegov.com/Public/CompiledDocument?meetingTemplateId="

        for doc in item.get("documentList", []):
            doc_name = doc.get("templateName", "").lower()
            doc_id = doc.get("templateId")
            
            doc_url = f"{pdf_base_url}{doc_id}&compileOutputType=1"

            if "packet" in doc_name:
                found_documents["agenda_packet"] = doc_url
            elif "agenda" in doc_name:
                found_documents["agenda"] = doc_url
            elif "minute" in doc_name:
                found_documents["minutes"] = doc_url

        # 4. Map to Standard Model
        return dataclasses.asdict(PublicDocument(
            title=title,
            date_published=date_published_iso,
            city=getattr(self, "city_name", "Unknown"),
            state=getattr(self, "state_name", "Unknown"),
            platform="primegov",
            department=department_name,
            documents=found_documents
        ))