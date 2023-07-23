from dataclasses import dataclass

@dataclass
class Page:
    page_id: int
    title: str
    source: str
    latitude: float
    longitude: float
    description: str
    image_title: str
