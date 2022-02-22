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

The retrieved ads will be saved in the _result.json_ file.

_Currently the scrape works only for **properties ads** in the **Brazilian portuguese website**._

## Filtering ads

It is possible to apply some filter to the ads to be retrieved by using a _filter.json_ file in the following format.

```
{
    "exclude": {
        "location": [        <-- filter out locations 
            <location 1>,
            <location 2>,
            ...
            <location N>
        ]
    }
}
```

It is also possible to filter ads newer than a given date using the argument _--from-date_:

```
python scrape.py <url> --from-date MM/DD/YYYY
```
