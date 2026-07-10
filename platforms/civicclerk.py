from spatula import JsonListPage, Page, NullSource
from core.data_models import PublicDocument
from urllib.parse import urljoin, quote

class BaseCivicClerkSearch(Page):
    source = NullSource()

    def process_page(self):
        depts = getattr(self, "target_departments", {})
        start_dates = getattr(self, "start_date", ["2026-01-01"])
        end_dates = getattr(self, "end_date", ["2030-12-31"])

        s_date = start_dates[0]
        e_date = end_dates[0]

        dept_ids = ",".join(depts.values())
        reverse_depts = {str(v): k for k, v in depts.items()}

        if dept_ids:
            filter_str = f"categoryId in ({dept_ids}) and startDateTime ge {s_date} and startDateTime lt {e_date}"
        else:
            filter_str = f"startDateTime ge {s_date} and startDateTime lt {e_date}"
    
        base_url = self.source.url
        query_string = f"?$filter={quote(filter_str)}&$orderby=startDateTime asc, eventName asc"
        full_url = f"{base_url}{query_string}"
        first_page = BaseCivicClerkEvents(full_url)
        first_page.city_name = getattr(self, "city_name", "Unknown")
        first_page.state_name = getattr(self, "state_name", "Unknown")
        first_page.dept_map = reverse_depts
        yield first_page


class BaseCivicClerkEvents(JsonListPage):

    def get_source_from_input(self):
        return self.input

    def process_page(self):
        events = self.data.get("value", [])

        for item in events:
            processed = self.process_item(item)
            if processed:
                yield processed

        next_link = self.data.get("@odata.nextLink")
        if next_link:
            next_page = BaseCivicClerkEvents(next_link)
            next_page.city_name = getattr(self, "city_name", "Unknown")
            next_page.state_name = getattr(self, "state_name", "Unknown")
            next_page.dept_map = getattr(self, "dept_map", {})
            yield next_page
    
    def process_item(self, item):
        name = item.get("eventName", "Unknown")

        raw_date = item.get("eventDate", "")
        date_str = raw_date.split("T")[0] if raw_date else ""

        dept_id = str(item.get("categoryId", ""))
        dept_map = getattr(self, "dept_map", {})
        department_name = dept_map.get(dept_id, "Unknown Department")

        found_documents = {}

        published_files = item.get("publishedFiles", [])

        for file in published_files:
            doc_type_raw = file.get("type", "unknown").lower()
            doc_type = doc_type_raw.replace(" ", "_")
            file_id = file.get("fileId")
            file_url = f"Meetings/GetMeetingFileStream(fileId={file_id},plainText=false)"

            full_url = urljoin(self.source.url.removesuffix("Events"), file_url)
            found_documents[doc_type] = full_url

        if name and found_documents:
            record = PublicDocument(
                title=name,
                date_published=date_str,
                city=getattr(self, "city_name", "Unknown"),
                state=getattr(self,"state_name", "unknown"),
                platform="civicclerk",
                department=department_name,
                documents=found_documents
            )
            return record
    