"""
Digital Oracle MCP Server
Based on FastMCP >= 2.0 framework
Wraps digital-oracle providers as MCP tools
"""
import json
import os
import sys
from dataclasses import asdict, is_dataclass
from typing import Any

from fastmcp import FastMCP

_SRC_DIR = os.path.join(os.path.dirname(__file__), "src")
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

from digital_oracle import (
    PolymarketProvider, PolymarketEventQuery,
    KalshiProvider, KalshiMarketQuery,
    YahooPriceProvider, PriceHistoryQuery,
    USTreasuryProvider, YieldCurveQuery,
    CftcCotProvider, CftcCotQuery,
    CoinGeckoProvider, CoinGeckoPriceQuery,
    EdgarProvider, EdgarInsiderQuery,
    BisProvider, BisRateQuery,
    DeribitProvider, DeribitFuturesCurveQuery,
    FearGreedProvider,
    CMEFedWatchProvider,
    YFinanceProvider, OptionsChainQuery,
    WebSearchProvider, WebSearchQuery,
    WorldBankProvider, WorldBankQuery,
    gather,
)

mcp = FastMCP("digital-oracle-mcp")

_EDGAR_EMAIL = os.environ.get("EDGAR_USER_EMAIL", "")


def serialize(obj: Any) -> str:
    """Serialize any object to JSON string"""
    if obj is None:
        return "null"
    if is_dataclass(obj) and not isinstance(obj, type):
        return json.dumps(asdict(obj), ensure_ascii=False, default=str)
    if isinstance(obj, (list, tuple)):
        return json.dumps(
            [asdict(i) if is_dataclass(i) else i for i in obj],
            ensure_ascii=False,
            default=str,
        )
    if isinstance(obj, dict):
        return json.dumps(obj, ensure_ascii=False, default=str)
    return json.dumps(str(obj), ensure_ascii=False)


# ============ MCP Tools ============

@mcp.tool()
def get_polymarket_events(
    slug_contains: str | None = None,
    limit: int = 20,
    active: bool | None = True,
    closed: bool | None = False,
) -> str:
    """Query Polymarket prediction market events.

    Use when: the user asks probability questions about geopolitics, economics,
    conflicts, or any event where real money is being traded on the outcome.
    Examples: 'What's the probability of WW3?', 'Will Russia-Ukraine war end?',
    'Will there be a recession?'

    Args:
        slug_contains: Filter events by keyword in slug/title (fuzzy search)
        limit: Maximum number of events to return (default 20)
        active: Only active events (default True)
        closed: Include closed events (default False)
    """
    try:
        pm = PolymarketProvider()
        query = PolymarketEventQuery(
            slug_contains=slug_contains,
            limit=limit,
            active=active,
            closed=closed,
        )
        events = pm.list_events(query)
        return serialize(events)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_kalshi_markets(
    series_ticker: str | None = None,
    event_ticker: str | None = None,
    limit: int = 20,
    status: str = "open",
) -> str:
    """Query Kalshi US-regulated binary contracts.

    Use when: the user asks about US economic/political events with regulated
    prediction markets. Kalshi is SEC-regulated.
    Examples: 'Will Fed cut rates?', 'S&P 500 range this month?'

    Args:
        series_ticker: Filter by series (e.g. 'KXFED' for Fed, 'KXINX' for S&P 500)
        event_ticker: Filter by specific event ticker
        limit: Maximum number of markets to return (default 20)
        status: Market status filter (default 'open')
    """
    try:
        kalshi = KalshiProvider()
        query = KalshiMarketQuery(
            series_ticker=series_ticker,
            event_ticker=event_ticker,
            limit=limit,
            status=status,
        )
        markets = kalshi.list_markets(query)
        return serialize(markets)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_price_history(
    symbol: str,
    limit: int = 30,
) -> str:
    """Query Yahoo Finance price history for stocks, ETFs, futures, forex.

    Use when: the user asks about price trends, historical performance,
    or technical analysis of any traded asset.
    Examples: 'What's gold doing lately?', 'SPY trend?', 'BTC price history?'

    Args:
        symbol: Yahoo Finance symbol.
            - Futures: GC=F (gold), CL=F (crude oil), HG=F (copper)
            - Forex: EURUSD=X, USDJPY=X
            - US stocks/ETFs: SPY, QQQ, AAPL
            - European stocks: RHM.DE, BA.L
        limit: Number of daily bars to return (default 30)
    """
    try:
        yahoo = YahooPriceProvider()
        query = PriceHistoryQuery(symbol=symbol.upper(), limit=limit)
        history = yahoo.get_history(query)
        return serialize(history)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_yield_curve(
    year: int | None = None,
    curve_kind: str = "nominal",
) -> str:
    """Query US Treasury yield curve data.

    Use when: the user asks about interest rates, yield curve shape,
    recession signals, or inflation expectations.
    Examples: 'Is the yield curve inverted?', '10Y-2Y spread?', 'Real rates?'

    Args:
        year: Year for historical data (default: current year)
        curve_kind: 'nominal', 'real', 'bill', 'long_term' (default 'nominal')
    """
    try:
        treasury = USTreasuryProvider()
        query = YieldCurveQuery(year=year or 2026, curve_kind=curve_kind)
        curve = treasury.latest_yield_curve(query)
        return serialize(curve)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_cftc_positions(
    commodity_name: str | None = None,
    limit: int = 10,
) -> str:
    """Query CFTC Commitments of Traders futures positioning data.

    Use when: the user wants to know institutional (smart money) positioning
    direction in commodities, forex, or indices.
    Examples: 'Are specs bullish gold?', 'CFTC gold positioning?',
    'Managed money direction in crude?'

    Args:
        commodity_name: Filter by commodity (e.g. 'GOLD', 'CRUDE OIL', 'S&P 500')
        limit: Number of reports to return (default 10)
    """
    try:
        cftc = CftcCotProvider()
        query = CftcCotQuery(commodity_name=commodity_name, limit=limit)
        reports = cftc.list_reports(query)
        return serialize(reports)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_crypto_prices(
    coin_ids: str = "bitcoin,ethereum",
    limit: int = 10,
) -> str:
    """Query CoinGecko cryptocurrency prices and market data.

    Use when: the user asks about crypto asset prices, market cap,
    or on-chain metrics.
    Examples: 'BTC price?', 'Ethereum market cap?', 'Crypto sentiment?'

    Args:
        coin_ids: Comma-separated CoinGecko coin IDs (default 'bitcoin,ethereum')
        limit: Number of results (default 10)
    """
    try:
        coingecko = CoinGeckoProvider()
        ids = tuple(coin_ids.split(","))
        query = CoinGeckoPriceQuery(coin_ids=ids, limit=limit)
        prices = coingecko.get_prices(query)
        return serialize(prices)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_insider_trades(
    ticker: str,
    limit: int = 10,
) -> str:
    """Query SEC EDGAR insider trading transactions (Form 4).

    Use when: the user wants to know if company insiders are buying or selling.
    Examples: 'AAPL insider trades?', 'NVDA insider selling?', 'TSLA Form 4?'

    Args:
        ticker: Stock ticker symbol (e.g. 'AAPL', 'NVDA')
        limit: Number of transactions to return (default 10)
    """
    try:
        edgar = EdgarProvider(user_email=_EDGAR_EMAIL)
        query = EdgarInsiderQuery(ticker=ticker.upper(), limit=limit)
        trades = edgar.get_insider_transactions(query)
        return serialize(trades)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_policy_rates(
    countries: str = "US,CN",
    start_year: int = 2023,
) -> str:
    """Query BIS central bank policy rates.

    Use when: the user asks about monetary policy, interest rate trends,
    or credit conditions across major economies.
    Examples: 'Fed rate direction?', 'China rate policy?', 'Credit/GDP gap?'

    Args:
        countries: Comma-separated country codes (default 'US,CN')
        start_year: Start year for historical data (default 2023)
    """
    try:
        bis = BisProvider()
        codes = tuple(countries.split(","))
        query = BisRateQuery(countries=codes, start_year=start_year)
        rates = bis.get_policy_rates(query)
        return serialize(rates)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_futures_curve(
    currency: str = "BTC",
) -> str:
    """Query Deribit crypto futures term structure.

    Use when: the user asks about crypto market risk appetite, futures basis,
    or term structure contango/backwardation.
    Examples: 'BTC futures basis?', 'Crypto risk appetite?', 'BTC term structure?'

    Args:
        currency: 'BTC' or 'ETH' (default 'BTC')
    """
    try:
        deribit = DeribitProvider()
        query = DeribitFuturesCurveQuery(currency=currency.upper())
        curve = deribit.get_futures_term_structure(query)
        return serialize(curve)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_fear_greed_index() -> str:
    """Query CNN Fear & Greed Index (composite of 7 market signals).

    Use when: the user asks about overall market sentiment, fear/greed levels,
    or risk appetite timing.
    Examples: 'Market sentiment?', 'Fear & Greed?', 'Risk appetite?'
    """
    try:
        fear_greed = FearGreedProvider()
        index = fear_greed.get_index()
        return serialize(index)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_fed_rate_probs() -> str:
    """Query CME FedWatch for market-implied FOMC rate change probabilities.

    Use when: the user asks about Fed rate expectations, FOMC meeting outcomes,
    or interest rate path pricing.
    Examples: 'Fed rate expectations?', 'Fed cut probability?', 'FOMC market pricing?'

    Note: Requires yfinance. Install with: uv pip install yfinance
    """
    try:
        fedwatch = CMEFedWatchProvider()
        probs = fedwatch.get_probabilities()
        return serialize(probs)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_options_chain(
    ticker: str,
    expiration: str | None = None,
) -> str:
    """Query Yahoo Finance options chain with Black-Scholes Greeks.

    Use when: the user asks about options premiums, implied volatility,
    put/call ratios, max pain, or market maker positioning.
    Examples: 'NVDA options premium?', 'SPY IV?', 'Put/call ratio?', 'Max pain?'

    Requires: uv pip install yfinance

    Args:
        ticker: Stock ticker (e.g. 'SPY', 'NVDA', 'QQQ')
        expiration: Expiration date YYYY-MM-DD (default: nearest expiration)
    """
    try:
        yf = YFinanceProvider()
        query = OptionsChainQuery(ticker=ticker.upper(), expiration=expiration)
        chain = yf.get_chain(query)
        return serialize(chain)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def web_search(
    query: str,
    max_results: int = 5,
) -> str:
    """Search the web for supplementary financial data.

    Use when: the user asks about data not available via structured providers,
    such as VIX level, CDS spreads, BDI freight rates, war risk premiums.
    Examples: 'VIX current level?', 'US high yield spread?', 'BDI index?'

    Args:
        query: Search query
        max_results: Maximum number of results (default 5)
    """
    try:
        web = WebSearchProvider()
        result = web.search(WebSearchQuery(query=query, max_results=max_results))
        return result.text()
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def multi_signal_query(
    question: str,
    symbols: str = "GC=F,SPY",
    crypto_coins: str = "bitcoin,ethereum",
    commodities: str | None = None,
    tickers: str | None = None,
) -> str:
    """Fetch multiple data sources in parallel for cross-validation.

    Use when: the user asks complex questions requiring multiple data sources
    for analysis. This tool fetches price history, crypto prices, fear/greed,
    and yield curve in parallel.

    Args:
        question: The user's question (for context only, not processed)
        symbols: Comma-separated Yahoo Finance symbols (default 'GC=F,SPY')
        crypto_coins: Comma-separated CoinGecko coin IDs
        commodities: CFTC commodity names to query (optional)
        tickers: Stock tickers for options data (optional)
    """
    try:
        yahoo = YahooPriceProvider()
        coingecko = CoinGeckoProvider()
        fear_greed = FearGreedProvider()
        treasury = USTreasuryProvider()

        tasks = {}
        for sym in symbols.split(","):
            sym = sym.strip()
            if sym:
                tasks[f"price_{sym}"] = lambda s=sym: yahoo.get_history(
                    PriceHistoryQuery(symbol=s, limit=30)
                )

        for coin in crypto_coins.split(","):
            coin = coin.strip()
            if coin:
                tasks[f"crypto_{coin}"] = lambda c=coin: coingecko.get_prices(
                    CoinGeckoPriceQuery(coin_ids=(c,), limit=1)
                )

        tasks["fear_greed"] = lambda: fear_greed.get_index()
        tasks["yield_curve"] = lambda: treasury.latest_yield_curve()

        if commodities:
            cftc = CftcCotProvider()
            for comm in commodities.split(","):
                comm = comm.strip()
                if comm:
                    tasks[f"cftc_{comm}"] = lambda c=comm: cftc.list_reports(
                        CftcCotQuery(commodity_name=c, limit=4)
                    )

        if tickers:
            yf = YFinanceProvider()
            for tkr in tickers.split(","):
                tkr = tkr.strip()
                if tkr:
                    tasks[f"options_{tkr}"] = lambda t=tkr: yf.get_chain(
                        OptionsChainQuery(ticker=t)
                    )

        result = gather(tasks)
        return serialize({
            "results": result.results,
            "errors": {k: str(v) for k, v in result.errors.items()},
        })
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# ============ Main ============

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Digital Oracle MCP Server")
    parser.add_argument("--transport", choices=["stdio", "streamable-http", "sse"],
                        default="stdio", help="Transport mode")
    parser.add_argument("--host", default="0.0.0.0", help="Host for HTTP server")
    parser.add_argument("--port", type=int, default=8000, help="Port for HTTP server")
    args = parser.parse_args(sys.argv[1:])

    if args.transport == "stdio":
        mcp.run()
    else:
        mcp.run(
            transport=args.transport,
            host=args.host,
            port=args.port,
            stateless_http=True,
        )


def main_cloud():
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
        stateless_http=True,
    )


if __name__ == "__main__":
    main()
