import argparse
import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from olx_scraper.filter import Filter
from olx_scraper.scraper.ad_scraper import AdScraper

DEFAULT_FILTER_PATH = 'filter.json'


def scrape(url: str, from_date: datetime = None):
    """Scrape a OLX ad list page extracting data from each ad"""
    response = requests.get(
        url,
        headers={
            'User-Agent': (
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) '
                'Gecko/20100101 Firefox/96.0'
            )
        }
    )
    if response.status_code != 200:
        print(f'Erro ao tentar baixar a página ({response.status_code})')
    else:
        ad_filter = Filter.load_from_file(DEFAULT_FILTER_PATH)
        if from_date:
            ad_filter['from_date'] = from_date

        soup = BeautifulSoup(response.text, 'html.parser')
        ads = soup.find('ul', {'id': 'ad-list'})
        ad_scraper = AdScraper()
        scraped_ads = []
        for ad_element in ads.contents:
            ad_obj = ad_scraper.scrape(ad_element)
            if ad_obj is not None and ad_filter.should_filter(ad_obj):
                scraped_ads.append(ad_obj)

        with open('result.json', 'w', encoding='utf-8') as output_fp:
            json.dump(
                [ad_obj.serialized() for ad_obj in scraped_ads],
                output_fp,
                indent=2
            )
        print(f'{len(scraped_ads)} ads saved!')


def date(date_string: str) -> datetime:
    """Validate and convert a date from string to datetime.

    The date must be in the format MM/DD/YYYY.
    """
    return datetime.strptime(date_string, r'%m/%d/%Y')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape OLX ads.')
    parser.add_argument(
        'url',
        help=('Url of the page to scrape. Should be the search page with a '
              'list of ads.')
    )
    parser.add_argument(
        '--from-date',
        dest='from_date',
        type=date,
        default=None,
        help=('The date to start the search from. Will scrape only ads newer '
              'than this date. The format must be MM/DD/YYYY')
    )
    args = parser.parse_args()
    scrape(url=args.url, from_date=args.from_date)
