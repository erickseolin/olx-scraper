from typing import Any, Dict


class Ad:
    """Ad model"""

    def __init__(self, **kwargs) -> None:
        self.title = kwargs.get('title')
        self.link = kwargs.get('link')
        self.img = kwargs.get('img')
        self.info = kwargs.get('info')
        self.value = kwargs.get('value')
        self.date = kwargs.get('date')
        self.location = kwargs.get('location')
        self.vendor_type = kwargs.get('vendor_type')

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
