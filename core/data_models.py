from dataclasses import dataclass

@dataclass
class PublicDocument:
    title: str
    date_published: str
    city: str
    state: str
    platform: str
    department: str
    documents: dict