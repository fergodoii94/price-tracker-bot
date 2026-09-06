# Price Tracker Bot 🛒💰

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Requests](https://img.shields.io/badge/Requests-2.31+-blue.svg)](https://requests.readthedocs.io/)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-4.12+-green.svg)](https://www.crummy.com/software/BeautifulSoup/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Production-grade **E-commerce Price Monitoring Bot** for tracking product prices across retailers with automated alerts. Features robust HTTP handling, CSS selector extraction, European price parsing, Decimal arithmetic for accuracy, and store-agnostic design.

## 🎯 Key Features

✅ **Multi-store Monitoring** - Track prices across different retailers
✅ **Price Extraction** - CSS selector-based parsing
✅ **European Format Support** - Parse 1.299,99 format correctly
✅ **Decimal Precision** - Accurate money calculations
✅ **Type Safety** - Full type hints and dataclasses
✅ **Error Handling** - Graceful HTTP error recovery
✅ **Retry Logic** - Automatic backoff and retries
✅ **Production Ready** - Scheduled execution, logging, notifications

## 🚀 Quick Start

### Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Basic Usage
```python
from decimal import Decimal
from price_tracker import track_price

result = track_price(
    url="https://example.com/laptop",
    target_price=Decimal("999.99"),
    selector=".product-price"
)

if result.target_reached:
    print(f"Price alert! Laptop now: {result.price}")
else:
    print(f"Current price: {result.price}")
```

## 📊 Supported Price Formats

```python
# US Format
"$1,299.99" → 1299.99

# European Format
"1.299,99 €" → 1299.99

# Decimal Format
"1299.99" → 1299.99

# Multiple formats auto-detected and normalized
```

## 🔧 Configuration

### Store Configuration
```python
STORES = {
    "amazon": {
        "base_url": "https://www.amazon.com",
        "price_selector": ".a-price-whole",
        "timeout": 10,
        "headers": {"User-Agent": "Mozilla/5.0..."}
    },
    "ebay": {
        "base_url": "https://www.ebay.com",
        "price_selector": ".vi-VR-cvipPrice",
        "timeout": 10
    }
}
```

### Retry Configuration
```python
retry_config = {
    "max_retries": 3,
    "backoff_factor": 2,
    "timeout": 10,
    "status_forcelist": [429, 500, 502, 503, 504]
}
```

## 💻 API Reference

### PriceResult Dataclass
```python
@dataclass
class PriceResult:
    price: Decimal              # Extracted price
    target_price: Decimal       # Target price
    target_reached: bool        # Price <= target?
    url: str                    # Product URL
    store: str                  # Store name
    extracted_at: datetime      # Extraction timestamp
    currency: str               # Currency code
```

### Main Function
```python
def track_price(
    url: str,
    target_price: Decimal,
    selector: str,
    store: str = "generic",
    timeout: int = 10,
    parse_format: str = "auto"
) -> PriceResult:
    """
    Track product price against target.
    
    Args:
        url: Product URL
        target_price: Target price for alert
        selector: CSS selector for price element
        store: Store identifier
        timeout: Request timeout seconds
        parse_format: Price format ("us", "eu", "auto")
    
    Returns:
        PriceResult with tracking data
    """
```

## 📈 Scheduled Monitoring

### Using APScheduler
```python
from apscheduler.schedulers.background import BackgroundScheduler
from price_tracker import track_price

scheduler = BackgroundScheduler()

def monitor_price():
    result = track_price(
        url="https://example.com/laptop",
        target_price=Decimal("999.99"),
        selector=".price"
    )
    
    if result.target_reached:
        send_notification(result)

# Check every hour
scheduler.add_job(monitor_price, 'interval', hours=1)
scheduler.start()
```

### Using Celery
```python
from celery import Celery
from price_tracker import track_price

app = Celery('price_tracker')

@app.task
def monitor_price_task(url, target_price, selector):
    result = track_price(url, Decimal(target_price), selector)
    
    if result.target_reached:
        send_email_alert(result)
    
    return {
        "price": str(result.price),
        "target_reached": result.target_reached
    }

# Schedule every hour
from celery.schedules import crontab
app.conf.beat_schedule = {
    'monitor-every-hour': {
        'task': 'tasks.monitor_price_task',
        'schedule': crontab(minute=0),  # Every hour
    },
}
```

## 📊 Example Use Cases

### E-commerce Comparison
```python
from decimal import Decimal
from price_tracker import track_price

products = [
    {"url": "amazon.com/laptop", "target": Decimal("999.99")},
    {"url": "bestbuy.com/laptop", "target": Decimal("1099.99")},
    {"url": "newegg.com/laptop", "target": Decimal("949.99")}
]

for product in products:
    result = track_price(
        url=product["url"],
        target_price=product["target"],
        selector=".price"
    )
    print(f"{result.store}: {result.price} (Alert: {result.target_reached})")
```

### Bulk Price Export
```python
import csv
from price_tracker import track_price

with open('price_export.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Product', 'Store', 'Price', 'Target', 'Alert'])
    
    for product_url, target_price, selector, store in products_list:
        result = track_price(product_url, target_price, selector, store)
        writer.writerow([
            result.url,
            result.store,
            result.price,
            result.target_price,
            result.target_reached
        ])
```

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=term-missing

# Mock HTTP tests
pytest tests/test_price_extraction.py -v
```

**Coverage:** 92%+ with mocked HTTP responses

## 🏗️ Project Structure

```
price-tracker-bot/
├── src/
│   ├── __init__.py
│   ├── tracker.py        # Main tracking logic
│   ├── parser.py         # Price parsing
│   ├── schemas.py        # Data classes
│   ├── stores.py         # Store configurations
│   └── notifications.py  # Alert system
├── tests/
│   ├── test_tracker.py
│   ├── test_parser.py
│   └── test_stores.py
├── examples/
│   ├── basic_tracking.py
│   ├── scheduled_monitoring.py
│   └── email_alerts.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

## ⚠️ Important Notes

### Store Terms & Conditions
- Always check website `robots.txt`
- Respect rate limits and `User-Agent`
- Use appropriate delays between requests
- Consider using official APIs when available

### Markup Changes
- HTML selectors break when store updates layout
- Monitor selector validity regularly
- Use fallback selectors when possible
- Implement alerting for selector failures

## 🔄 Error Handling

```python
try:
    result = track_price(url, target_price, selector)
except requests.Timeout:
    logger.error(f"Request timeout for {url}")
except requests.HTTPError as e:
    logger.error(f"HTTP error: {e.response.status_code}")
except PriceSelectorError:
    logger.error(f"Could not extract price with selector: {selector}")
except InvalidPriceFormatError:
    logger.error(f"Could not parse price format")
```

## 📤 Notifications

### Email Alerts
```python
from price_tracker.notifications import send_email

send_email(
    to="user@example.com",
    subject=f"Price Alert: {result.url}",
    body=f"Price dropped to {result.price}!"
)
```

### Webhook Integration
```python
import requests

def send_webhook(result: PriceResult):
    requests.post(
        "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
        json={
            "text": f"Price Alert: {result.price}",
            "url": result.url
        }
    )
```

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 👨‍💻 Author

**Fernando Godoi**
- GitHub: [@fergodoii94](https://github.com/fergodoii94)
- Email: fergodoi94@gmail.com

**Expertise:** Web Scraping | Price Monitoring | Automation | Python

**Status:** ✅ Production Ready | **Reliability:** ✅ Robust Error Handling
