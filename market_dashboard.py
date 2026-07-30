import io
import pandas as pd
import yfinance as yf
import streamlit as st

st.set_page_config(page_title="Market Top Gainers", layout="wide")

st.title("Top 5 Gainers: Nifty 50 & Sensex 30")

@st.cache_data(ttl=300) # Cache data for 5 minutes
def load_data():
    csv_data = """Company Name,Industry,Symbol,Series,ISIN Code
Adani Enterprises Ltd.,Metals & Mining,ADANIENT,EQ,INE423A01024
Adani Ports and Special Economic Zone Ltd.,Services,ADANIPORTS,EQ,INE742F01042
Apollo Hospitals Enterprise Ltd.,Healthcare,APOLLOHOSP,EQ,INE437A01024
Asian Paints Ltd.,Consumer Durables,ASIANPAINT,EQ,INE021A01026
Axis Bank Ltd.,Financial Services,AXISBANK,EQ,INE238A01034
Bajaj Auto Ltd.,Automobile and Auto Components,BAJAJ-AUTO,EQ,INE917I01010
Bajaj Finance Ltd.,Financial Services,BAJFINANCE,EQ,INE296A01032
Bajaj Finserv Ltd.,Financial Services,BAJAJFINSV,EQ,INE918I01026
Bharat Electronics Ltd.,Capital Goods,BEL,EQ,INE263A01024
Bharti Airtel Ltd.,Telecommunication,BHARTIARTL,EQ,INE397D01024
Cipla Ltd.,Healthcare,CIPLA,EQ,INE059A01026
Coal India Ltd.,Oil Gas & Consumable Fuels,COALINDIA,EQ,INE522F01014
Dr. Reddy's Laboratories Ltd.,Healthcare,DRREDDY,EQ,INE089A01031
Eicher Motors Ltd.,Automobile and Auto Components,EICHERMOT,EQ,INE066A01021
Eternal Ltd.,Consumer Services,ETERNAL,EQ,INE758T01015
Grasim Industries Ltd.,Construction Materials,GRASIM,EQ,INE047A01021
HCL Technologies Ltd.,Information Technology,HCLTECH,EQ,INE860A01027
HDFC Bank Ltd.,Financial Services,HDFCBANK,EQ,INE040A01034
HDFC Life Insurance Company Ltd.,Financial Services,HDFCLIFE,EQ,INE795G01014
Hindalco Industries Ltd.,Metals & Mining,HINDALCO,EQ,INE038A01020
H हिंदुस्तान Unilever Ltd.,Fast Moving Consumer Goods,HINDUNILVR,EQ,INE030A01027
ICICI Bank Ltd.,Financial Services,ICICIBANK,EQ,INE090A01021
ITC Ltd.,Fast Moving Consumer Goods,ITC,EQ,INE154A01025
Infosys Ltd.,Information Technology,INFY,EQ,INE009A01021
InterGlobe Aviation Ltd.,Services,INDIGO,EQ,INE646L01027
JSW Steel Ltd.,Metals & Mining,JSWSTEEL,EQ,INE019A01038
Jio Financial Services Ltd.,Financial Services,JIOFIN,EQ,INE758E01017
Kotak Mahindra Bank Ltd.,Financial Services,KOTAKBANK,EQ,INE237A01036
Larsen & Toubro Ltd.,Construction,LT,EQ,INE018A01030
Mahindra & Mahindra Ltd.,Automobile and Auto Components,M&M,EQ,INE101A01026
Maruti Suzuki India Ltd.,Automobile and Auto Components,MARUTI,EQ,INE585B01010
Max Healthcare Institute Ltd.,Healthcare,MAXHEALTH,EQ,INE027H01010
NTPC Ltd.,Power,NTPC,EQ,INE733E01010
Nestle India Ltd.,Fast Moving Consumer Goods,NESTLEIND,EQ,INE239A01024
Oil & Natural Gas Corporation Ltd.,Oil Gas & Consumable Fuels,ONGC,EQ,INE213A01029
Power Grid Corporation of India Ltd.,Power,POWERGRID,EQ,INE752E01010
Reliance Industries Ltd.,Oil Gas & Consumable Fuels,RELIANCE,EQ,INE002A01018
SBI Life Insurance Company Ltd.,Financial Services,SBILIFE,EQ,INE123W01016
Shriram Finance Ltd.,Financial Services,SHRIRAMFIN,EQ,INE721A01047
State Bank of India,Financial Services,SBIN,EQ,INE062A01020
Sun Pharmaceutical Industries Ltd.,Healthcare,SUNPHARMA,EQ,INE044A01036
Tata Consultancy Services Ltd.,Information Technology,TCS,EQ,INE467B01029
Tata Consumer Products Ltd.,Fast Moving Consumer Goods,TATACONSUM,EQ,INE192A01025
Tata Motors Passenger Vehicles Ltd.,Automobile and Auto Components,TMPV,EQ,INE155A01022
Tata Steel Ltd.,Metals & Mining,TATASTEEL,EQ,INE081A01020
Tech Mahindra Ltd.,Information Technology,TECHM,EQ,INE669C01036
Titan Company Ltd.,Consumer Durables,TITAN,EQ,INE280A01028
Trent Ltd.,Consumer Services,TRENT,EQ,INE849A01020
UltraTech Cement Ltd.,Construction Materials,ULTRACEMCO,EQ,INE481G01011
Wipro Ltd.,Information Technology,WIPRO,EQ,INE075A01022"""

    df_1 = pd.read_csv(io.StringIO(csv_data), usecols=["Symbol"])
    df_1['Symbol'] = df_1['Symbol'].astype(str).str.strip() + '.NS'

    df_2 = ['ADANIPORTS.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'BAJFINANCE.NS','BAJAJFINSV.NS', 'BEL.NS',
            'BHARTIARTL.NS', 'ETERNAL.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS',
            'INDIGO.NS', 'INFY.NS', 'ITC.NS', 'KOTAKBANK.NS', 'LT.NS', 'M&M.NS', 'MARUTI.NS', 'NTPC.NS',
            'POWERGRID.NS', 'RELIANCE.NS', 'SBIN.NS', 'SUNPHARMA.NS', 'TCS.NS', 'TATASTEEL.NS', 'TECHM.NS',
            'TITAN.NS', 'TRENT.NS', 'ULTRACEMCO.NS']

    df_3 = sorted(list(set(df_1["Symbol"]) | set(df_2)))

    data = yf.download(
        tickers=df_3,
        period="3mo",
        interval="1d",
        auto_adjust=True,
        progress=False
    )
    
    close_df = data['Close']
    close_df = close_df.dropna(how='all')
    return close_df

def trailing_return(price_df, trading_days):
    if len(price_df) <= trading_days:
        return pd.Series(dtype=float)
    latest = price_df.iloc[-1]
    past = price_df.iloc[-1 - trading_days]
    return ((latest - past) / past * 100).round(2)

with st.spinner('Fetching latest market data from Yahoo Finance...'):
    try:
        close_df = load_data()
        
        ret_1d = trailing_return(close_df, 1)
        ret_1w = trailing_return(close_df, 5)
        ret_15d = trailing_return(close_df, 11)
        ret_1m = trailing_return(close_df, 21)

        def format_top5(ret_series):
            top5 = ret_series.dropna().sort_values(ascending=False).head(5).reset_index()
            top5.columns = ['Symbol', 'Return (%)']
            top5['Return (%)'] = top5['Return (%)'].apply(lambda x: f"{x:.2f}%")
            return top5

        top5_1d = format_top5(ret_1d)
        top5_1w = format_top5(ret_1w)
        top5_15d = format_top5(ret_15d)
        top5_1m = format_top5(ret_1m)

        if 'selected_symbol' not in st.session_state:
            st.session_state.selected_symbol = None

        def draw_button_table(df, prefix):
            st.markdown(
                "<div style='display: flex; font-weight: bold; padding-bottom: 5px; border-bottom: 1px solid #ddd; margin-bottom: 10px;'>"
                "<div style='flex: 1;'>Symbol</div><div style='flex: 1;'>Return</div></div>",
                unsafe_allow_html=True
            )
            for _, row in df.iterrows():
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button(row['Symbol'], key=f"{prefix}_{row['Symbol']}", use_container_width=True):
                        st.session_state.selected_symbol = row['Symbol']
                with col2:
                    st.write(f"<div style='padding-top: 5px;'>{row['Return (%)']}</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top 5 Gainers (1 Day)")
            draw_button_table(top5_1d, '1d')
            st.write("")
            st.subheader("Top 5 Gainers (15 Days)")
            draw_button_table(top5_15d, '15d')
            
        with col2:
            st.subheader("Top 5 Gainers (1 Week)")
            draw_button_table(top5_1w, '1w')
            st.write("")
            st.subheader("Top 5 Gainers (1 Month)")
            draw_button_table(top5_1m, '1m')
            
        st.caption("Data fetches automatically and refreshes every 5 minutes.")
        
        @st.cache_data(ttl=3600)
        def get_symbol_details(symbol):
            try:
                return yf.Ticker(symbol).info
            except:
                return {}

        selected_symbol = st.session_state.selected_symbol
        if selected_symbol:
            st.markdown("---")
            st.subheader(f"{selected_symbol} - Details & Chart")
            
            if selected_symbol in close_df.columns:
                st.line_chart(close_df[selected_symbol].dropna(), height=300)

            with st.spinner("Fetching details..."):
                info = get_symbol_details(selected_symbol)
                if info:
                    dcol1, dcol2 = st.columns(2)
                    dcol1.write(f"**Name:** {info.get('longName', 'N/A')}")
                    dcol1.write(f"**Sector:** {info.get('sector', 'N/A')}")
                    dcol1.write(f"**Industry:** {info.get('industry', 'N/A')}")
                    
                    dcol2.write(f"**Previous Close:** {info.get('previousClose', 'N/A')}")
                    market_cap = info.get('marketCap')
                    if market_cap:
                        dcol2.write(f"**Market Cap:** ₹{market_cap:,.0f}")
                        
                    st.write(f"**Description:** {info.get('longBusinessSummary', 'N/A')}")
                else:
                    st.warning("Could not fetch extended details for this symbol.")
        
        if st.button("Refresh Data Manually"):
            st.cache_data.clear()
            st.rerun()

    except Exception as e:
        st.error(f"Error loading data: {e}")
