from nicegui import ui
import yfinance as yf
from utils import get_current_date_time, format_currency, format_percentage
from data_service import get_top_performers, symbols_list, company_names
from tables import create_analytics_table

def fetch_index_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="2d")
        if len(hist) >= 2:
            prev_close = hist['Close'].iloc[-2]
            current = hist['Close'].iloc[-1]
            change = current - prev_close
            pct_change = (change / prev_close) * 100
            return current, change, pct_change
        return None, None, None
    except:
        return None, None, None

def create_summary_card(title, value, change=None, pct_change=None, icon_name="stacked_line_chart", link=None):
    card = ui.card().classes('w-full md:flex-1 min-w-[250px] p-6 bg-gray-800 text-white shadow-xl rounded-2xl cursor-pointer transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl border border-gray-700')
    if link:
        card.on('click', lambda: ui.navigate.to(link))
    with card:
        with ui.row().classes('w-full justify-between items-center'):
            ui.label(title).classes('text-xl font-bold text-gray-400 uppercase tracking-wide')
            ui.icon(icon_name).classes('text-3xl text-blue-500 opacity-90')
            
        ui.label(str(value) if value is not None else "N/A").classes('text-4xl font-extrabold mt-4')
        
        if change is not None and pct_change is not None:
            color = 'text-green-400' if change >= 0 else 'text-red-400'
            sign = '+' if change >= 0 else ''
            icon_dir = 'trending_up' if change >= 0 else 'trending_down'
            with ui.row().classes('items-center gap-1 mt-2'):
                ui.icon(icon_dir).classes(f'text-lg {color}')
                ui.label(f"{sign}{change:.2f} ({sign}{pct_change:.2f}%)").classes(f'text-lg font-semibold {color}')

def render_market_overview():
    # Header Section
    with ui.row().classes('w-full justify-between items-center mb-16 bg-gray-800 p-8 rounded-3xl shadow-2xl border border-gray-700'):
        with ui.row().classes('items-center gap-6'):
            ui.icon('insights').classes('text-6xl text-blue-500 drop-shadow-md')
            with ui.column().classes('gap-1'):
                ui.label("Indian Stock Analytics").classes('text-5xl font-black tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400')
                ui.label("Real-time NIFTY 50 & SENSEX 30 performance").classes('text-xl text-gray-400 font-medium')
        with ui.row().classes('items-center gap-2 bg-gray-900 px-4 py-2 rounded-full border border-gray-700'):
            ui.icon('schedule').classes('text-gray-400 text-xl')
            ui.label(get_current_date_time()).classes('text-md text-gray-300 font-semibold')

    # Summary Cards
    with ui.row().classes('w-full items-center gap-2 mb-8'):
        ui.icon('dashboard').classes('text-2xl text-blue-400')
        ui.label("Market Overview").classes('text-3xl font-bold')
        
    with ui.row().classes('w-full gap-6 mb-16 flex-wrap'):
        # NIFTY 50
        nifty_val, nifty_change, nifty_pct = fetch_index_data('^NSEI')
        create_summary_card(
            "NIFTY 50", 
            f"{nifty_val:,.2f}" if nifty_val else "N/A", 
            nifty_change, 
            nifty_pct,
            "show_chart",
            link="/index/^NSEI"
        )
        
        # SENSEX
        sensex_val, sensex_change, sensex_pct = fetch_index_data('^BSESN')
        create_summary_card(
            "SENSEX 30", 
            f"{sensex_val:,.2f}" if sensex_val else "N/A", 
            sensex_change, 
            sensex_pct,
            "bar_chart",
            link="/index/^BSESN"
        )
        
        # Total Tracked
        create_summary_card("Total Stocks", len(symbols_list), icon_name="list_alt")

    # Search Box
    with ui.card().classes('w-full mb-20 p-8 bg-gray-800 rounded-3xl shadow-xl border border-gray-700'):
        ui.label("Search Stocks").classes('text-3xl font-bold mb-6 ml-2 text-white')
        
        results_container = ui.column().classes('w-full gap-2 px-2 mt-4')
        
        def update_search(e):
            query = e.value.lower() if e.value else ""
            results_container.clear()
            if not query:
                return
            
            matches = []
            for sym, name in company_names.items():
                clean_sym = sym.replace('.NS', '')
                if query in clean_sym.lower() or query in name.lower():
                    matches.append((clean_sym, name, sym))
            
            with results_container:
                if not matches:
                    ui.label("No matches found.").classes('text-gray-400 italic ml-2')
                for clean_sym, name, raw_sym in matches[:5]:
                    with ui.card().classes('w-full p-4 bg-gray-900 border border-gray-700 hover:bg-gray-700 cursor-pointer rounded-xl transition-colors shadow-sm').on('click', lambda s=raw_sym: ui.navigate.to(f"/stock/{s}")):
                        with ui.column().classes('gap-0'):
                            ui.label(clean_sym).classes('text-xl font-bold text-white')
                            ui.label(name).classes('text-md text-gray-400')

        with ui.row().classes('w-full items-center gap-4 px-2'):
            ui.icon('search').classes('text-4xl text-blue-400')
            ui.input(placeholder='Type to search by symbol or company name...', on_change=update_search).classes('flex-grow text-xl font-medium')

def render_top_performers():
    # Custom Analytics Section
    with ui.row().classes('w-full items-center gap-2 mb-6 mt-4'):
        ui.icon('leaderboard').classes('text-4xl text-blue-400')
        ui.label("Top Performers Analytics").classes('text-4xl font-bold')
    
    with ui.tabs().classes('w-full') as tabs:
        tab_1d = ui.tab('1 Day')
        tab_1w = ui.tab('1 Week')
        tab_15d = ui.tab('15 Days')
        tab_1m = ui.tab('1 Month')

    with ui.tab_panels(tabs, value=tab_1d).classes('w-full bg-transparent'):
        with ui.tab_panel(tab_1d):
            with ui.spinner('dots', size='lg'):
                data_1d = get_top_performers(1)
            create_analytics_table(data_1d)

        with ui.tab_panel(tab_1w):
            with ui.spinner('dots', size='lg'):
                data_1w = get_top_performers(5)
            create_analytics_table(data_1w)
            
        with ui.tab_panel(tab_15d):
            with ui.spinner('dots', size='lg'):
                data_15d = get_top_performers(11)
            create_analytics_table(data_15d)
            
        with ui.tab_panel(tab_1m):
            with ui.spinner('dots', size='lg'):
                data_1m = get_top_performers(21)
            create_analytics_table(data_1m)
