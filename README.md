# Price Tracker Bot

A small Python utility for monitoring product prices and comparing them with a target threshold. Built as a reusable foundation for shopping automation.

## Why this project

Price monitoring is a practical automation problem: fetch a product page, extract a price reliably, normalize European number formats, and decide whether the target has been reached.

## Features

- HTTP requests with timeout and status validation
- CSS-selector based price extraction
- European price parsing (`1.299,99` → `1299.99`)
- `Decimal` arithmetic for money values
- Typed `PriceResult` domain object
- Store-agnostic design instead of hard-coding one retailer

## Run

```bash
pip install requests beautifulsoup4
python main.py
```

Before integrating a retailer, provide a real product URL and the correct price selector. Store markup changes over time, so selectors must be maintained per website.

## Example

```python
from decimal import Decimal
from main import track_price

result = track_price(
    "https://example.com/product",
    Decimal("500.00"),
    selector=".price",
)

print(result.price, result.target_reached)
```

## Engineering Notes

The project deliberately avoids pretending that one HTML selector works across every store. A production version could add scheduled jobs, persistent price history, notifications, retries/backoff, and retailer-specific adapters.

## Stack

Python · Requests · BeautifulSoup · Decimal · Dataclasses
