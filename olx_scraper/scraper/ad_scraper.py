from datetime import datetime, timedelta

from olx_scraper.models import Ad

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


class AdScraper:
    def scrape(self, ad_element):
        """Scrape a single ad from an ad html element."""
        ad_link = ad_element.a
        if ad_link is None:
            return None
        ad_link_url = ad_link.attrs['href']
        photos_div, data_div = ad_link.div.contents[:2]
        image_url = photos_div.find('img').attrs['src']
        title = data_div.find('h2').get_text()
        other_data = [span.get_text() for span in data_div.find_all('span')]

        # discard previous ad value
        if other_data[0].startswith('R$'):
            other_data.pop(0)

        publication_day, publication_time = other_data.pop(
            -1).lower().split(', ')
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

        hour, minutes = publication_time.split(':')
        publication_datetime = publication_day.replace(
            hour=int(hour),
            minute=int(minutes)
        )

        location = other_data.pop(-1)
        if other_data:
            vendor_type = other_data.pop(-1)
        else:
            vendor_type = ''

        return Ad(
            title=title,
            link=ad_link_url,
            img=image_url,
            value=other_data.pop(0),
            date=publication_datetime,
            location=location,
            vendor_type=vendor_type,
            info=' | '.join(other_data[1::2])
        )
