import sys
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

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

    def print(self):
        """Print class attributes"""
        print(f'title: {self.title}')
        print(f'link: {self.link}')
        print(f'img: {self.img}')
        print(f'info: {self.info}')
        print(f'value: {self.value}')
        print(f'date: {self.date}')
        print(f'location: {self.location}')
        print(f'vendor_type: {self.vendor_type}')


def scrap(url):
    """Scrap a OLX ad list page extracting data from each ad"""
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
        soup = BeautifulSoup(response.text, 'html.parser')
        ads = soup.find('ul', {'id': 'ad-list'})

        for ad in ads.contents:
            ad = ad.a
            if ad is None:
                continue
            ad_link = ad.attrs['href']
            photos_div, data_div = ad.div.contents[:2]
            image_url = photos_div.find('img').attrs['src']
            description = data_div.find('h2').get_text()
            other_data = [span.get_text()
                          for span in data_div.find_all('span')]

            ad_obj = Ad(
                title=description,
                link=ad_link,
                img=image_url,
                info=other_data.pop(0),
                value=other_data.pop(0)
            )

            # discart previous value
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

            ad_obj.print()
            print()


if __name__ == '__main__':
    scrap(url=sys.argv[1])
