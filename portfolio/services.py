"""
Mock-сервіс цін на акції.
У реальному проєкті тут був би виклик до зовнішнього API (Yahoo Finance, Alpha Vantage тощо).
"""

MOCK_PRICES: dict[str, float] = {
    "AAPL": 189.30,
    "TSLA": 177.50,
    "GOOGL": 175.20,
    "MSFT": 415.80,
    "AMZN": 192.40,
    "NVDA": 875.00,
    "META": 520.10,
    "BRK.B": 398.60,
    "JPM": 196.20,
    "V": 278.90,
}

UNKNOWN_PRICE = 0.0


def get_price(ticker: str) -> float:
    """Повертає ціну за тікером. Якщо тікер невідомий — повертає 0."""
    return MOCK_PRICES.get(ticker.upper(), UNKNOWN_PRICE)


def calculate_asset_value(ticker: str, quantity: int) -> float:
    """Розраховує вартість активу: кількість × поточна ціна."""
    return get_price(ticker) * quantity