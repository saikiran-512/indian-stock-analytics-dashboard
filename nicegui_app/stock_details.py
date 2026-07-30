from nicegui import ui, run
import plotly.graph_objects as go
from data_service import get_stock_info, get_stock_history, trailing_return, fetch_market_data, company_names
from utils import format_currency, format_large_number, format_percentage

async def render_stock_details(symbol):
    loading = ui.column().classes('w-full items-center justify-center min-h-[50vh]')
    with loading:
        ui.spinner('dots', size='xl', color='blue')
        ui.label(f"Loading data for {symbol}...").classes('text-xl text-gray-400 mt-4 font-medium')
        
    try:
        info = await run.io_bound(get_stock_info, symbol)
        hist = await run.io_bound(get_stock_history, symbol, '1y')
        all_close = await run.io_bound(fetch_market_data)
    finally:
        loading.delete()
        
    if not info and hist.empty:
        ui.label(f"Could not load data for {symbol}").classes('text-red-400 text-xl')
        return

    company_name = info.get('longName', company_names.get(symbol, symbol))
    current_price = hist['Close'].iloc[-1] if not hist.empty else info.get('currentPrice', None)

    # Header
    with ui.row().classes('w-full justify-between items-end mb-10'):
        with ui.column().classes('gap-1'):
            ui.label(company_name).classes('text-5xl font-extrabold tracking-tight text-white')
            ui.label(symbol).classes('text-2xl text-gray-400 font-medium')
        with ui.column().classes('items-end gap-1'):
            ui.label(format_currency(current_price)).classes('text-4xl font-bold text-green-400')
            ui.label(f"{info.get('sector', 'N/A')} | {info.get('industry', 'N/A')}").classes('text-lg text-gray-400')

    ui.separator().classes('mb-10')

    # Chart
    with ui.row().classes('w-full flex-wrap gap-8'):
        with ui.column().classes('w-full'):
            with ui.row().classes('items-center gap-2 mb-6'):
                ui.icon('show_chart').classes('text-3xl text-blue-400')
                ui.label("1-Year Price History").classes('text-3xl font-bold text-white')
                
            if not hist.empty:
                dates = hist.index.astype(str).tolist()
                prices = hist['Close'].astype(float).tolist()
                fig = go.Figure(data=[go.Scatter(x=dates, y=prices, mode='lines', line=dict(color='#3b82f6', width=2))])
                fig.update_layout(
                    margin=dict(l=20, r=20, t=20, b=20),
                    template='plotly_dark',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis_title="Date",
                    yaxis_title="Price (₹)"
                )
                with ui.card().classes('w-full p-2 bg-gray-800 border border-gray-700 rounded-2xl'):
                    ui.plotly(fig).classes('w-full h-[450px]')
            else:
                ui.label("No chart data available.").classes('text-gray-400')

    # Company Information
    with ui.row().classes('items-center gap-2 mt-16 mb-6'):
        ui.icon('domain').classes('text-3xl text-blue-400')
        ui.label("Company Information").classes('text-3xl font-bold text-white')
        
    with ui.row().classes('w-full gap-4 flex-wrap'):
        def info_card(icon_name, label, value):
            with ui.card().classes('flex-1 min-w-[150px] bg-gray-800 border border-gray-700 p-6 rounded-2xl items-center text-center hover:-translate-y-1 transition-all shadow-md'):
                ui.icon(icon_name).classes('text-4xl text-blue-400 opacity-90 mb-3')
                ui.label(label).classes('text-gray-400 font-medium text-sm uppercase tracking-wide')
                ui.label(value).classes('text-2xl font-bold text-white mt-1')

        info_card('business', 'Sector', info.get('sector', 'N/A'))
        info_card('factory', 'Industry', info.get('industry', 'N/A'))
        info_card('account_balance', 'Market Cap', format_large_number(info.get('marketCap')))
        info_card('analytics', 'P/E Ratio', f"{info.get('trailingPE', 'N/A'):.2f}" if isinstance(info.get('trailingPE'), (int, float)) else "N/A")
        info_card('keyboard_double_arrow_up', '52W High', format_currency(info.get('fiftyTwoWeekHigh')))
        info_card('keyboard_double_arrow_down', '52W Low', format_currency(info.get('fiftyTwoWeekLow')))
        info_card('payments', 'Dividend Yield', format_percentage(info.get('dividendYield', 0) * 100 if info.get('dividendYield') else None))

    # Performance Summary
    with ui.row().classes('items-center gap-2 mt-16 mb-6'):
        ui.icon('speed').classes('text-3xl text-blue-400')
        ui.label("Performance Summary").classes('text-3xl font-bold text-white')
    with ui.row().classes('w-full gap-4'):
        # Calculate returns
        if symbol in all_close.columns:
            symbol_close = all_close[[symbol]]
            ret_1d = trailing_return(symbol_close, 1).get(symbol)
            ret_1w = trailing_return(symbol_close, 5).get(symbol)
            ret_15d = trailing_return(symbol_close, 11).get(symbol)
            ret_1m = trailing_return(symbol_close, 21).get(symbol)
        else:
            ret_1d = ret_1w = ret_15d = ret_1m = None

        for period, ret in [("1 Day", ret_1d), ("1 Week", ret_1w), ("15 Days", ret_15d), ("1 Month", ret_1m)]:
            with ui.card().classes('flex-1 bg-gray-800 items-center justify-center py-4 rounded-xl'):
                ui.label(period).classes('text-gray-400 font-medium')
                color = 'text-green-400' if ret and ret >= 0 else 'text-red-400'
                ui.label(format_percentage(ret)).classes(f'text-2xl font-bold {color}')

    # Description
    ui.label("Company Description").classes('text-2xl font-bold mt-8 mb-4')
    desc = info.get('longBusinessSummary', 'No description available.')
    ui.label(desc).classes('text-gray-300 leading-relaxed text-lg mb-8')
