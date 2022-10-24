import json
from os.path import exists

from olx_scraper.models import Ad


class Filter(dict):
    """Filter model"""

    def should_filter(self, ad: Ad) -> bool:
        """Whether to keep the given ad."""
        to_exclude = self.get('exclude', {})
        locations_to_exclude = to_exclude.get('location', [])

        if ad.location in locations_to_exclude:
            return False

        if self.get('from_date') and ad.date < self['from_date']:
            return False

        return True

    @staticmethod
    def load_from_file(filepath: str) -> 'Filter':
        """Load a filter from a file."""
        if exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as filter_fp:
                return Filter(json.load(filter_fp))

        return Filter()
