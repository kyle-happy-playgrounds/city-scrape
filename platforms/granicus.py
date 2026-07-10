from spatula import Page
from core.data_models import PublicDocument
from datetime import datetime
from urllib.parse import urljoin
import lxml.etree
import dataclasses

class BaseGranicusRSSList(Page):

    def process_page(self):
        xml_root = lxml.etree.fromstring(self.response.content)
        
        for item in xml_root.xpath("//item"):
            title = item.findtext("title", "").strip()
            link_url = item.findtext("link", "").strip()
            
            if not title:
                continue

            pub_date_text = item.findtext("pubDate", "") or item.xpath("string(*[local-name()='pubDate'])")
            date_published_iso = ""
            if pub_date_text:
                dt = datetime.strptime(pub_date_text, "%a, %d %b %Y %H:%M:%S %z")
                date_published_iso = dt.strftime("%Y-%m-%d")

            target_depts = getattr(self, "target_departments", [])
            department_name = "Unknown"
            if target_depts:
                matched_dept = next((dept for dept in target_depts if dept.lower() in title.lower()), None)
                if not matched_dept:
                    continue
                department_name = matched_dept

            target_years = getattr(self, "target_years", [])
            if target_years and not any(year in title or year in date_published_iso for year in target_years):
                continue

            base_url = str(self.source.url) if hasattr(self.source, 'url') else str(self.source)
            found_documents = {"agenda": urljoin(base_url, link_url)} if link_url else {}

            yield dataclasses.asdict(PublicDocument(
                title=title,
                date_published=date_published_iso,
                city=getattr(self, "city_name", "Unknown"),
                state=getattr(self, "state_name", "Unknown"),
                platform="granicus",
                department=department_name,
                documents=found_documents
            ))