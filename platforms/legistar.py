from spatula import HtmlPage, HtmlListPage, CSS, URL
from core.data_models import PublicDocument
import json
from datetime import datetime

class BaseLegistarSearch(HtmlPage):

    def process_page(self):
        viewstate = self.root.xpath("//input[@name='__VIEWSTATE']/@value")
        viewstate_gen = self.root.xpath("//input[@name='__VIEWSTATEGENERATOR']/@value")
        event_validation = self.root.xpath("//input[@name='__EVENTVALIDATION']/@value")

        if not viewstate:
            return
        
        base_form_data = {
            "__VIEWSTATE": viewstate[0],
            "__VIEWSTATEGENERATOR": viewstate_gen[0] if viewstate_gen else "",
            "__EVENTVALIDATION": event_validation[0] if event_validation else "",
            "__EVENTTARGET": "", 
            "__EVENTARGUMENT": "",
        }

        target_depts = getattr(self, "target_departments", {})
        for year in getattr(self, "target_years", []):
            for dept_name, dept_id in target_depts.items():
                form_data = base_form_data.copy()
                form_data["ctl00$ContentPlaceHolder1$lstYears"] = year
                year_state = {
                    "logEntries": [],
                    "value": "",
                    "text": year,
                    "enabled": True,
                    "checkedIndices": [],
                    "checkedItemsTextOverflows": False
                }
                form_data["ctl00_ContentPlaceHolder1_lstYears_ClientState"] = json.dumps(year_state)

                form_data["ctl00$ContentPlaceHolder1$lstBodies"] = dept_name
                dept_state = {
                    "logEntries": [],
                    "value": dept_id,
                    "text": "",
                    "enabled": True,
                    "checkedIndices": [],
                    "checkedItemsTextOverflows": False
                }
                form_data["ctl00_ContentPlaceHolder1_lstBodies_ClientState"] = json.dumps(dept_state)
                
                post_url = URL(self.source.url, method="POST", data=form_data)
                list_page = BaseLegistarList(post_url)
                list_page.city_name = getattr(self, "city_name", "Unknown")
                list_page.state_name = getattr(self, "state_name", "Unknown")

                list_page.department = dept_name
                
                yield list_page


class BaseLegistarList(HtmlListPage):
    selector = CSS("table.rgMasterTable tbody tr")
    def get_source_from_input(self):
        return self.input
    
    def process_page(self):
        for processed in super().process_page():
            if processed:
                yield processed

    def process_item(self, item):
        #First and Second Column
        name_nodes = item.xpath("./td[1]")
        date_nodes = item.xpath("./td[2]")

        if not name_nodes or not date_nodes:
            return None
        
        name = name_nodes[0].text_content().strip()
        date_str = date_nodes[0].text_content().strip()
        doc_date_string = datetime.strptime(date_str, "%m/%d/%Y").date().isoformat()

        doc_columns = {
            7: "agenda",
            8: "agenda_packet",
            9: "minutes"
        }
        found_documents = {}
        for col_index, doc_type in doc_columns.items():
            links = item.xpath(f"./td[{col_index}]//a")
            if links:
                url = links[0].get("href", "")
                if url:
                    found_documents[doc_type] = url

        if name and found_documents:      
            doc = PublicDocument(
                title=name,
                date_published=doc_date_string,
                city=getattr(self, "city_name", "Unknown"),
                state=getattr(self,"state_name", "unknown"),
                department=getattr(self, "department", "unknown"),
                platform="legistar",
                documents=found_documents
            )

            return doc
        else:
            return None
    