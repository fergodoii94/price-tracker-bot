"""Simple, reusable product price tracker.

The project intentionally keeps the scraper store-agnostic: each website may need
its own CSS selector or parser because price markup differs between stores.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

import requests
from bs4 import BeautifulSoup


@dataclass(frozen=True)
class PriceResult:
    url: str
    price: Decimal
    target_price: Decimal

    @property
    def target_reached(self) -> bool:
        return self.price <= self.target_price


def parse_eur_price(value: str) -> Decimal:
    """Parse common European price formats such as €1.299,99 or 499,90."""
    cleaned = re.sub(r"[^0-9,.-]", "", value.strip())
    if not cleaned:
        raise InvalidOperation("Price contains no numeric value")

    if "," in cleaned and "." in cleaned:
        cleaned = cleaned.replace(".", "").replace(",", ".")
    elif "," in cleaned:
        cleaned = cleaned.replace(",", ".")

    return Decimal(cleaned)


def fetch_price(url: str, selector: str = "[data-price]") -> Decimal:
    """Fetch and parse a price from a CSS selector."""
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; PriceTracker/1.0)"},
        timeout=15,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    element = soup.select_one(selector)
    if element is None:
        raise ValueError(f"No price element found for selector: {selector}")

    raw_price = element.get("data-price") or element.get_text(" ", strip=True)
    return parse_eur_price(str(raw_price))


def track_price(url: str, target_price: Decimal, selector: str = "[data-price]") -> PriceResult:
    price = fetch_price(url, selector)
    return PriceResult(url=url, price=price, target_price=target_price)


if __name__ == "__main__":
    print("Price Tracker — configure a real product URL and selector before running.")
    print("Example selector: [data-price], .price, or the store-specific price element.")
