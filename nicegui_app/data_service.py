import yfinance as yf
import pandas as pd

# Combined list of NIFTY 50 and SENSEX 30 symbols
symbols_list = [
    'ADANIENT.NS', 'ADANIPORTS.NS', 'APOLLOHOSP.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 
    'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BEL.NS', 'BHARTIARTL.NS', 
    'CIPLA.NS', 'COALINDIA.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'GRASIM.NS', 
    'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HINDALCO.NS', 'HINDUNILVR.NS', 
    'ICICIBANK.NS', 'ITC.NS', 'INFY.NS', 'INDIGO.NS', 'JSWSTEEL.NS', 'JIOFIN.NS', 
    'KOTAKBANK.NS', 'LT.NS', 'M&M.NS', 'MARUTI.NS', 'NTPC.NS', 'NESTLEIND.NS', 
    'ONGC.NS', 'POWERGRID.NS', 'RELIANCE.NS', 'SBILIFE.NS', 'SHRIRAMFIN.NS', 
    'SBIN.NS', 'SUNPHARMA.NS', 'TCS.NS', 'TATACONSUM.NS', 'TATASTEEL.NS', 
    'TECHM.NS', 'TITAN.NS', 'TRENT.NS', 'ULTRACEMCO.NS', 'WIPRO.NS'
]

# Cache the global close prices data to avoid redundant API calls
_cached_close_df = None
_cached_info = {}

def fetch_market_data():
    """Fetches 6 months of daily historical data for all tracked symbols."""
    global _cached_close_df
    if _cached_close_df is not None:
        return _cached_close_df

    data = yf.download(
        tickers=symbols_list,
        period="6mo",
        interval="1d",
        auto_adjust=True,
        progress=False
    )
    close_df = data['Close']
    close_df = close_df.dropna(how='all')
    _cached_close_df = close_df
    return close_df

def trailing_return(price_df, trading_days):
    """Calculates the percentage return over a given number of trading days."""
    if len(price_df) <= trading_days:
        return pd.Series(dtype=float)
    latest = price_df.iloc[-1]
    past = price_df.iloc[-1 - trading_days]
    return ((latest - past) / past * 100).round(2)

company_names = {
    'ADANIENT.NS': 'Adani Enterprises Ltd.', 'ADANIPORTS.NS': 'Adani Ports and Special Economic Zone Ltd.',
    'APOLLOHOSP.NS': 'Apollo Hospitals Enterprise Ltd.', 'ASIANPAINT.NS': 'Asian Paints Ltd.',
    'AXISBANK.NS': 'Axis Bank Ltd.', 'BAJAJ-AUTO.NS': 'Bajaj Auto Ltd.', 'BAJFINANCE.NS': 'Bajaj Finance Ltd.',
    'BAJAJFINSV.NS': 'Bajaj Finserv Ltd.', 'BEL.NS': 'Bharat Electronics Ltd.', 'BHARTIARTL.NS': 'Bharti Airtel Ltd.',
    'CIPLA.NS': 'Cipla Ltd.', 'COALINDIA.NS': 'Coal India Ltd.', 'DRREDDY.NS': 'Dr. Reddy\'s Laboratories Ltd.',
    'EICHERMOT.NS': 'Eicher Motors Ltd.', 'GRASIM.NS': 'Grasim Industries Ltd.', 'HCLTECH.NS': 'HCL Technologies Ltd.',
    'HDFCBANK.NS': 'HDFC Bank Ltd.', 'HDFCLIFE.NS': 'HDFC Life Insurance Company Ltd.', 'HINDALCO.NS': 'Hindalco Industries Ltd.',
    'HINDUNILVR.NS': 'Hindustan Unilever Ltd.', 'ICICIBANK.NS': 'ICICI Bank Ltd.', 'ITC.NS': 'ITC Ltd.',
    'INFY.NS': 'Infosys Ltd.', 'INDIGO.NS': 'InterGlobe Aviation Ltd.', 'JSWSTEEL.NS': 'JSW Steel Ltd.',
    'JIOFIN.NS': 'Jio Financial Services Ltd.', 'KOTAKBANK.NS': 'Kotak Mahindra Bank Ltd.', 'LT.NS': 'Larsen & Toubro Ltd.',
    'M&M.NS': 'Mahindra & Mahindra Ltd.', 'MARUTI.NS': 'Maruti Suzuki India Ltd.', 'NTPC.NS': 'NTPC Ltd.',
    'NESTLEIND.NS': 'Nestle India Ltd.', 'ONGC.NS': 'Oil & Natural Gas Corporation Ltd.', 'POWERGRID.NS': 'Power Grid Corporation of India Ltd.',
    'RELIANCE.NS': 'Reliance Industries Ltd.', 'SBILIFE.NS': 'SBI Life Insurance Company Ltd.', 'SHRIRAMFIN.NS': 'Shriram Finance Ltd.',
    'SBIN.NS': 'State Bank of India', 'SUNPHARMA.NS': 'Sun Pharmaceutical Industries Ltd.', 'TCS.NS': 'Tata Consultancy Services Ltd.',
    'TATACONSUM.NS': 'Tata Consumer Products Ltd.', 'TATASTEEL.NS': 'Tata Steel Ltd.', 'TECHM.NS': 'Tech Mahindra Ltd.',
    'TITAN.NS': 'Titan Company Ltd.', 'TRENT.NS': 'Trent Ltd.', 'ULTRACEMCO.NS': 'UltraTech Cement Ltd.',
    'WIPRO.NS': 'Wipro Ltd.'
}

def get_top_performers(trading_days):
    """Returns a formatted list of dictionaries with stock performance data."""
    close_df = fetch_market_data()
    returns = trailing_return(close_df, trading_days)
    
    # Sort by descending return
    top = returns.dropna().sort_values(ascending=False)
    
    results = []
    latest_prices = close_df.iloc[-1]
    
    rank = 1
    for symbol, ret in top.items():
        results.append({
            "Rank": int(rank),
            "Symbol": str(symbol),
            "Company Name": str(company_names.get(symbol, symbol)),
            "Current Price": float(latest_prices[symbol]),
            "Return %": float(ret),
            "Market Cap": None
        })
        rank += 1
        
    return results

def get_stock_info(symbol):
    """Fetches detailed company info for a single symbol."""
    if symbol in _cached_info:
        return _cached_info[symbol]
    
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        _cached_info[symbol] = info
        return info
    except Exception:
        return {}

def get_stock_history(symbol, period="6mo"):
    """Fetches historical data specifically for plotting charts."""
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period)
    return hist
