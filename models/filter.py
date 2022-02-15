import json
from os.path import exists
from typing import Any, Dict

from models.ad import Ad


class Filter:
    """Filter model"""

    def __init__(self, ad_filter: Dict[str, Any]) -> None:
        self.filter_config = ad_filter

    def should_filter(self, ad: Ad):
        """Whether to filter the given ad"""
        to_exclude = self.filter_config.get('exclude', {})
        locations_to_exclude = to_exclude.get('location', [])

        return ad.location not in locations_to_exclude

    @staticmethod
    def load_from_file(filepath: str):
        """Load a filter from a file."""
        if exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as filter_fp:
                return Filter(json.load(filter_fp))

        return Filter({})
