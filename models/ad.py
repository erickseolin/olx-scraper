from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass
class Ad:
    """Ad model"""
    title: str
    link: str
    img: str
    info: str
    value: str
    date: datetime
    location: str
    vendor_type: str

    def serialized(self) -> Dict[str, Any]:
        """Return the model in a serializable dict format."""
        return {
            'title': self.title,
            'link': self.link,
            'img': self.img,
            'info': self.info,
            'value': self.value,
            'date': self.date.isoformat(),
            'location': self.location,
            'vendor_type': self.vendor_type
        }
