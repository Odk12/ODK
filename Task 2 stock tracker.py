#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
import os
from datetime import datetime

STOCK_PRICES: dict[str, float] = {
    "AAPL":  180.00,   # Apple
    "TSLA":  250.00,   # Tesla
    "GOOGL": 140.00,   # Alphabet
    "AMZN":  185.00,   # Amazon
    "MSFT":  415.00,   # Microsoft
    "NVDA":  875.00,   # NVIDIA
    "META":  505.00,   # Meta
    "NFLX":  630.00,   # Netflix
    "AMD":   165.00,   # AMD
    "INTC":   30.00,   # Intel
}

PORTFOLIO_FILE = "portfolio.csv"
SUMMARY_FILE   = "portfolio_summary.txt"


def show_available_stocks() -> None:
    print("\n  Available stocks:")
    print(f"  {'Ticker':<8} {'Company / Price (USD)':>25}")
    print("  " + "-" * 35)
    names = {
        "AAPL": "Apple",      "TSLA": "Tesla",     "GOOGL": "Alphabet",
        "AMZN": "Amazon",     "MSFT": "Microsoft", "NVDA":  "NVIDIA",
        "META": "Meta",       "NFLX": "Netflix",   "AMD":   "AMD",
        "INTC": "Intel",
    }
    for ticker, price in STOCK_PRICES.items():
        print(f"  {ticker:<8} {names[ticker]:<18} ${price:>8.2f}")
    print()


def get_portfolio_from_user() -> list[dict]:
    """Interactively collect stock name + quantity from the user."""
    portfolio = []
    print("\n  Enter your stock holdings.")
    print("  Type 'done' when finished, or 'list' to see available tickers.\n")

    while True:
        ticker = input("  Stock ticker (or 'done'/'list'): ").strip().upper()

        if ticker == "DONE":
            break

        if ticker == "LIST":
            show_available_stocks()
            continue

        if ticker not in STOCK_PRICES:
            print(f"  ⚠  '{ticker}' not found. Try 'list' to see valid tickers.")
            continue

        # Check for duplicates
        existing = next((s for s in portfolio if s["ticker"] == ticker), None)
        if existing:
            print(f"  ℹ  '{ticker}' already added (qty={existing['quantity']}). Use a new ticker.")
            continue

        while True:
            try:
                qty_str = input(f"  Quantity of {ticker}: ").strip()
                qty = float(qty_str)
                if qty <= 0:
                    raise ValueError
                break
            except ValueError:
                print("  ⚠  Please enter a positive number.")

        portfolio.append({"ticker": ticker, "quantity": qty})
        price = STOCK_PRICES[ticker]
        value = price * qty
        print(f"  ✅  Added {qty:g} × {ticker} @ ${price:.2f} = ${value:,.2f}\n")

    return portfolio


def calculate_totals(portfolio: list[dict]) -> list[dict]:
    """Enrich each holding with price and total value."""
    enriched = []
    for holding in portfolio:
        ticker = holding["ticker"]
        qty    = holding["quantity"]
        price  = STOCK_PRICES[ticker]
        value  = price * qty
        enriched.append({
            "ticker":   ticker,
            "quantity": qty,
            "price":    price,
            "value":    value,
        })
    return enriched


def display_portfolio(enriched: list[dict]) -> None:
    total = sum(h["value"] for h in enriched)

    print("\n" + "=" * 55)
    print("   YOUR PORTFOLIO SUMMARY")
    print("=" * 55)
    print(f"  {'Ticker':<8} {'Qty':>8} {'Price':>12} {'Total Value':>14}")
    print("  " + "-" * 47)
    for h in enriched:
        print(
            f"  {h['ticker']:<8} {h['quantity']:>8.2f} "
            f"${h['price']:>10.2f} ${h['value']:>12,.2f}"
        )
    print("  " + "-" * 47)
    print(f"  {'TOTAL PORTFOLIO VALUE':>40}  ${total:>12,.2f}")
    print("=" * 55 + "\n")


def save_to_csv(enriched: list[dict]) -> None:
    total = sum(h["value"] for h in enriched)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(PORTFOLIO_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", timestamp])
        writer.writerow([])
        writer.writerow(["Ticker", "Quantity", "Price (USD)", "Total Value (USD)"])
        for h in enriched:
            writer.writerow([h["ticker"], h["quantity"], h["price"], round(h["value"], 2)])
        writer.writerow([])
        writer.writerow(["", "", "TOTAL", round(total, 2)])

    print(f" Portfolio saved to '{PORTFOLIO_FILE}'")


def save_to_txt(enriched: list[dict]) -> None:
    total = sum(h["value"] for h in enriched)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(SUMMARY_FILE, "w") as f:
        f.write("=" * 55 + "\n")
        f.write("       ODURO — STOCK PORTFOLIO SUMMARY\n")
        f.write(f"       Generated : {timestamp}\n")
        f.write("=" * 55 + "\n\n")
        f.write(f"  {'Ticker':<8} {'Qty':>8} {'Price':>12} {'Total Value':>14}\n")
        f.write("  " + "-" * 47 + "\n")
        for h in enriched:
            f.write(
                f"  {h['ticker']:<8} {h['quantity']:>8.2f} "
                f"${h['price']:>10.2f} ${h['value']:>12,.2f}\n"
            )
        f.write("  " + "-" * 47 + "\n")
        f.write(f"  {'TOTAL':>40}  ${total:>12,.2f}\n")
        f.write("=" * 55 + "\n")

    print(f"   Summary saved to '{SUMMARY_FILE}'")


def main() -> None:
    print("\n" + "=" * 55)
    print("  ODURO STOCK PORTFOLIO TRACKER")
    print("=" * 55)

    show_available_stocks()
    portfolio = get_portfolio_from_user()

    if not portfolio:
        print("\n  No stocks entered. Exiting.")
        return

    enriched = calculate_totals(portfolio)
    display_portfolio(enriched)

    save = input("  Save results? (csv / txt / both / no): ").strip().lower()
    if save in ("csv", "both"):
        save_to_csv(enriched)
    if save in ("txt", "both"):
        save_to_txt(enriched)

    print("\n    Done! Thank you for using the Portfolio Tracker.\n")


if __name__ == "__main__":
    main()
    
    


# In[ ]:




