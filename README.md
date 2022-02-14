# Scraper for ads from OLX Website

Simple scraper for ads from the OLX Website.

## How to run

To run the scraper install the python requirements.

```
pip install -r requirements.txt
```

then run the scrape.py script with the url of the search

```
python scrape.py <url>
```

Example:

```
python scrape.py 'https://www.olx.com.br/imoveis/venda/casas?q=sobrado'
```

_Currently the scrape works only for **properties ads** in the **Brazilian portuguese website**._