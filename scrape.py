import json
import sys
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from models import Ad, Filter

DEFAULT_FILTER_PATH = 'filter.json'
MONTHS = {
    'jan': 1,
    'fev': 2,
    'mar': 3,
    'abr': 4,
    'mai': 5,
    'jun': 6,
    'jul': 7,
    'ago': 8,
    'set': 9,
    'out': 10,
    'nov': 11,
    'dez': 12,
}


def scrape_ad(ad_element):
    """Scrape a single ad from an ad html element."""
    ad_link = ad_element.a
    if ad_link is None:
        return None
    ad_link_url = ad_link.attrs['href']
    photos_div, data_div = ad_link.div.contents[:2]
    image_url = photos_div.find('img').attrs['src']
    title = data_div.find('h2').get_text()
    other_data = [span.get_text() for span in data_div.find_all('span')]

    ad_obj = Ad(
        title=title,
        link=ad_link_url,
        img=image_url,
        info=other_data.pop(0),
        value=other_data.pop(0)
    )

    # discard previous ad value
    if other_data[0].startswith('R$'):
        other_data.pop(0)

    publication_day = other_data.pop(0).lower()
    if publication_day == 'hoje':
        publication_day = datetime.today()
    elif publication_day == 'ontem':
        publication_day = datetime.today() - timedelta(days=1)
    else:
        day, month_str = publication_day.split(' ')
        publication_day = datetime(
            year=datetime.today().year,
            month=MONTHS[month_str],
            day=int(day)
        )

    hour, minutes = other_data.pop(0).split(':')
    publication_datetime = publication_day.replace(
        hour=int(hour),
        minute=int(minutes)
    )

    ad_obj.date = publication_datetime
    ad_obj.location = other_data.pop(0)
    if other_data:
        ad_obj.vendor_type = other_data.pop(0)

    return ad_obj


def scrape(url):
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

        soup = BeautifulSoup(response.text, 'html.parser')
        ads = soup.find('ul', {'id': 'ad-list'})
        scraped_ads = []
        for ad_element in ads.contents:
            ad_obj = scrape_ad(ad_element)
            if ad_obj is not None and ad_filter.should_filter(ad_obj):
                scraped_ads.append(ad_obj)

        with open('result.json', 'w', encoding='utf-8') as output_fp:
            json.dump(
                [ad_obj.serialized() for ad_obj in scraped_ads],
                output_fp,
                indent=2
            )
        print(f'{len(scraped_ads)} ads saved!')


if __name__ == '__main__':
    scrape(url=sys.argv[1])
