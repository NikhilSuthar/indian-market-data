"""
NSE Trading Calendar — compute settlement number and trading day info.

Settlement number = {YYYY}{NNN} where NNN = cumulative NSE trading days
from Jan 1 of that year (inclusive of the date itself).

Examples verified:
    2026-04-17 → 2026070
    2026-05-21 → 2026093
    2026-05-22 → 2026094
"""

from datetime import date, timedelta

# ─── NSE Holidays by year ─────────────────────────────────────────────────────
# Source: https://www.nseindia.com/resources/exchange-communication-holidays
# Add future years as needed

NSE_HOLIDAYS = {
    2024: {
        date(2024, 1, 22),  # Ram Lalla Pran Pratishtha
        date(2024, 1, 26),  # Republic Day
        date(2024, 3, 25),  # Holi
        date(2024, 3, 29),  # Good Friday
        date(2024, 4, 11),  # Id-Ul-Fitr (Ramzan Id)
        date(2024, 4, 14),  # Dr Ambedkar Jayanti / Ram Navami
        date(2024, 4, 17),  # Ram Navami
        date(2024, 4, 21),  # Ram Navami (adjusting for Sunday)
        date(2024, 5, 23),  # Lok Sabha Election
        date(2024, 6, 17),  # Bakri Id
        date(2024, 7, 17),  # Muharram
        date(2024, 8, 15),  # Independence Day
        date(2024, 10, 2),  # Gandhi Jayanti
        date(2024, 11, 1),  # Diwali Laxmi Pujan
        date(2024, 11, 15), # Gurunanak Jayanti
        date(2024, 11, 20), # Maharashtra Assembly Election
        date(2024, 12, 25), # Christmas
    },
    2025: {
        date(2025, 2, 26),  # Mahashivratri
        date(2025, 3, 14),  # Holi
        date(2025, 3, 31),  # Id-Ul-Fitr
        date(2025, 4, 10),  # Shri Ram Navami
        date(2025, 4, 14),  # Dr Ambedkar Jayanti
        date(2025, 4, 18),  # Good Friday
        date(2025, 5, 1),   # Maharashtra Day
        date(2025, 8, 15),  # Independence Day
        date(2025, 8, 27),  # Ganesh Chaturthi
        date(2025, 10, 2),  # Dussehra / Gandhi Jayanti
        date(2025, 10, 20), # Diwali Laxmi Pujan
        date(2025, 10, 21), # Diwali Balipratipada
        date(2025, 11, 5),  # Gurunanak Jayanti
        date(2025, 12, 25), # Christmas
    },
    2026: {
        date(2026, 1, 1),   # New Year's Day
        date(2026, 1, 26),  # Republic Day
        date(2026, 2, 26),  # Mahashivratri
        date(2026, 3, 14),  # Holi
        date(2026, 3, 31),  # Id-Ul-Fitr
        date(2026, 4, 3),   # Good Friday
        date(2026, 4, 10),  # Dr Ambedkar Jayanti
        date(2026, 4, 14),  # Ram Navami (Tue)
        date(2026, 5, 1),   # Maharashtra Day
        date(2026, 8, 15),  # Independence Day
        date(2026, 10, 2),  # Gandhi Jayanti / Dussehra
        date(2026, 11, 9),  # Diwali Laxmi Pujan
        date(2026, 11, 25), # Gurunanak Jayanti
        date(2026, 12, 25), # Christmas
    },
}


def is_trading_day(d: date) -> bool:
    """Return True if the given date is an NSE trading day."""
    if d.weekday() >= 5:  # Saturday or Sunday
        return False
    holidays = NSE_HOLIDAYS.get(d.year, set())
    return d not in holidays


def count_trading_days(from_date: date, to_date: date) -> int:
    """Count NSE trading days from from_date to to_date (both inclusive)."""
    count = 0
    d = from_date
    while d <= to_date:
        if is_trading_day(d):
            count += 1
        d += timedelta(days=1)
    return count


def get_settno(trade_date: date) -> str:
    """
    Get the NSE settlement number for a given trading date.

    Settlement number = YYYY + 3-digit cumulative trading days from Jan 1.

    Args:
        trade_date: A date object for the trading day.

    Returns:
        str: Settlement number e.g. "2026094" for 2026-05-22

    Raises:
        ValueError: If the date is not a trading day.

    Example:
        >>> from nsedata.calendar import get_settno
        >>> from datetime import date
        >>> get_settno(date(2026, 5, 22))
        '2026094'
        >>> get_settno(date(2026, 4, 17))
        '2026070'
    """
    if not is_trading_day(trade_date):
        raise ValueError(
            f"{trade_date} is not an NSE trading day "
            f"(weekend or holiday). Use the previous trading day."
        )

    jan1 = date(trade_date.year, 1, 1)
    n = count_trading_days(jan1, trade_date)
    return f"{trade_date.year}{n:03d}"


def get_settno_str(date_str: str) -> str:
    """
    Get settlement number from a YYYY-MM-DD string.

    Example:
        >>> get_settno_str("2026-05-22")
        '2026094'
    """
    from datetime import datetime
    d = datetime.strptime(date_str, "%Y-%m-%d").date()
    return get_settno(d)


def prev_trading_day(d: date) -> date:
    """Return the previous NSE trading day."""
    d = d - timedelta(days=1)
    while not is_trading_day(d):
        d -= timedelta(days=1)
    return d
