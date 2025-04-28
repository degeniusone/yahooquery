<p align="center">
    <a href="#"><img src="docs/docs/img/full.png"></a>
</p>
<p align="center">
    <em>Python wrapper for an unofficial Yahoo Finance API</em>
</p>
<p align="center">
    <a href="https://travis-ci.com/dpguthrie/yahooquery" target="_blank">
        <img src="https://travis-ci.com/dpguthrie/yahooquery.svg?branch=master" alt="Build Status">
    </a>
    <a href="https://codecov.io/gh/dpguthrie/yahooquery" target="_blank">
        <img src="https://img.shields.io/codecov/c/github/dpguthrie/yahooquery" alt="Coverage">
    </a>
    <a href="https://pypi.org/project/yahooquery" target="_blank">
        <img src="https://badge.fury.io/py/yahooquery.svg" alt="Package version">
    </a>
    <a href="https://pepy.tech/project/yahooquery" target="_blank">
        <img src="https://pepy.tech/badge/yahooquery" alt="Downloads">
    </a>
</p>

---

**Documentation**: <a target="_blank" href="https://yahooquery.dpguthrie.com">https://yahooquery.dpguthrie.com</a>

**Interactive Demo**: <a target="_blank" href="https://yahooquery.streamlit.app/">https://yahooquery.streamlit.app/</a>

**Source Code**: <a target="_blank" href="https://github.com/dpguthrie/yahooquery">https://github.com/dpguthrie/yahooquery</a>

**Blog Post**: <a target="_blank" href="https://towardsdatascience.com/the-unofficial-yahoo-finance-api-32dcf5d53df">https://towardsdatascience.com/the-unofficial-yahoo-finance-api-32dcf5d53df</a>

---

## Overview

Yahooquery is a python interface to unofficial Yahoo Finance API endpoints. The package allows a user to retrieve nearly all the data visible via the Yahoo Finance front-end.

Some features of yahooquery:

- **Fast**: Data is retrieved through API endpoints instead of web scraping. Additionally, asynchronous requests can be utilized with simple configuration
- **Simple**: Data for multiple symbols can be retrieved with simple one-liners
- **User-friendly**: Pandas Dataframes are utilized where appropriate
- **Premium**: Yahoo Finance premium subscribers are able to retrieve data available through their subscription

## Requirements

Python 2.7, 3.5+

- [Pandas](https://pandas.pydata.org) - Fast, powerful, flexible and easy to use open source data analysis and manipulation tool
- [Requests](https://requests.readthedocs.io/en/master/) - The elegant and simple HTTP library for Python, built for human beings.
- [Requests-Futures](https://github.com/ross/requests-futures) - Asynchronous Python HTTP Requests for Humans

### Yahoo Finance Premium Subscribers

- [Selenium](https://www.selenium.dev/selenium/docs/api/py/) - Web browser automation

  Selenium is only utilized to login to Yahoo, which is done when the user passes certain keyword arguments. Logging into Yahoo enables users who are subscribers to Yahoo Finance Premium to retrieve data only accessible to premium subscribers.

## Installation

If you're a Yahoo Finance premium subscriber and would like to retrieve data available through your subscription, do the following:

```bash
pip install yahooquery[premium]
```

Otherwise, omit the premium argument:

```bash
pip install yahooquery
```

## Example

The majority of the data available through the unofficial Yahoo Finance API is related to a company, which is represented in yahooquery as a `Ticker`. You can instantiate the `Ticker` class by passing the company's ticker symbol. For instance, to get data for Apple, Inc., pass `aapl` as the first argument to the `Ticker` class:

```python
from yahooquery import Ticker

aapl = Ticker('aapl')

aapl.summary_detail
```

## Multiple Symbol Example

The `Ticker` class also makes it easy to retrieve data for a list of symbols with the same API. Simply pass a list of symbols as the argument to the `Ticker` class.

```python
from yahooquery import Ticker

symbols = ['fb', 'aapl', 'amzn', 'nflx', 'goog']

faang = Ticker(symbols)

faang.summary_detail
```

## TradingView Screener API Endpoints

The backend now provides a comprehensive REST API for TradingView Screener data. These endpoints allow you to query, explore, and format data for use in your frontend widgets or applications.

### Endpoints

- **GET `/api/screener/columns`**  
  Returns a list of all available columns/fields for screener queries.

- **GET `/api/screener/models`**  
  Returns a list of available models for advanced queries.

- **POST `/api/screener/query`**  
  Run advanced screener queries with custom selection, filtering, sorting, limits, and offsets.  
  **Example request body:**
  ```json
  {
    "select": ["name", "close", "volume"],
    "where": [
      {"column": "volume", "op": ">", "value": 1000000}
    ],
    "order_by": {"column": "volume", "ascending": false},
    "limit": 10
  }
  ```

- **GET `/api/screener/technical_rating?rating=0.7`**  
  Converts a numeric technical rating into a human-readable string (e.g., "Strong Buy").

- **GET `/api/screener/predefined?screen_ids=most_actives,day_gainers&count=25`**  
  Returns results from predefined TradingView screeners.  
  Example `screen_ids`: `most_actives`, `day_gainers`, etc.

### Usage
- All endpoints return JSON.
- Use `/api/screener/columns` to dynamically build field selectors in your frontend.
- Use `/api/screener/query` for custom, advanced queries.
- Use `/api/screener/predefined` for common market screens.

### API Documentation
- Visit `http://localhost:8000/docs` while the backend is running for interactive API docs and testing.

## License

This project is licensed under the terms of the MIT license.
