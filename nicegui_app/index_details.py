from nicegui import ui, run
import plotly.graph_objects as go
from data_service import get_top_performers, get_stock_history
from dashboard import fetch_index_data

async def render_index_details(symbol):
    loading = ui.column().classes('w-full items-center justify-center min-h-[50vh]')
    with loading:
        ui.spinner('dots', size='xl', color='blue')
        ui.label(f"Loading data for {symbol}...").classes('text-xl text-gray-400 mt-4 font-medium')
        
    try:
        val, change, pct = await run.io_bound(fetch_index_data, symbol)
        hist = await run.io_bound(get_stock_history, symbol, '1mo')
        all_perf = await run.io_bound(get_top_performers, 1)
    finally:
        loading.delete()
        
    name = "NIFTY 50" if symbol == '^NSEI' else "SENSEX 30"
    
    with ui.row().classes('w-full justify-between items-center mb-10'):
        ui.label(f"{name} Overview").classes('text-4xl font-extrabold tracking-tight text-white')
    ui.separator().classes('mb-12')
    
    # Overview
    with ui.row().classes('w-full gap-6 mb-16'):
        with ui.card().classes('flex-1 p-6 bg-gray-800 rounded-2xl border border-gray-700 text-center'):
            ui.label("Current Value").classes('text-gray-400 font-bold uppercase tracking-wide')
            ui.label(f"{val:,.2f}" if val else "N/A").classes('text-5xl font-black mt-2 text-white')
        with ui.card().classes('flex-1 p-6 bg-gray-800 rounded-2xl border border-gray-700 text-center'):
            ui.label("Today's Change").classes('text-gray-400 font-bold uppercase tracking-wide')
            color = 'text-green-400' if change and change >= 0 else 'text-red-400'
            sign = '+' if change and change >= 0 else ''
            ui.label(f"{sign}{change:.2f} ({sign}{pct:.2f}%)" if change else "N/A").classes(f'text-5xl font-black mt-2 {color}')

    # Chart
    hist = get_stock_history(symbol, period='1mo')
    if not hist.empty:
        dates = hist.index.astype(str).tolist()
        prices = hist['Close'].astype(float).tolist()
        line_color = '#10b981' if (change and change >= 0) else '#ef4444'
        fig = go.Figure(data=[go.Scatter(x=dates, y=prices, mode='lines', line=dict(color=line_color, width=3))])
        fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20), 
            template='plotly_dark', 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Date",
            yaxis_title="Index Value"
        )
        with ui.card().classes('w-full p-6 bg-gray-800 rounded-2xl mb-12 border border-gray-700'):
            with ui.row().classes('items-center gap-2 mb-4'):
                ui.icon('show_chart').classes('text-2xl text-blue-400')
                ui.label("1-Month Performance").classes('text-2xl font-bold text-white')
            ui.plotly(fig).classes('w-full h-[350px]')
            
    # Gainers and Losers
    with ui.row().classes('items-center gap-2 mb-6'):
        ui.icon('swap_vert').classes('text-3xl text-blue-400')
        ui.label("Today's Market Movers (Tracked Stocks)").classes('text-3xl font-bold text-white')
        
    gainers = [x for x in all_perf if x['Return %'] > 0][:5]
    losers = sorted([x for x in all_perf if x['Return %'] < 0], key=lambda k: k['Return %'])[:5]
    
    with ui.row().classes('w-full gap-8 items-start'):
        with ui.column().classes('flex-1 w-full'):
            with ui.row().classes('items-center gap-2 mb-4'):
                ui.icon('trending_up').classes('text-2xl text-green-400')
                ui.label("Top 5 Gainers").classes('text-2xl font-bold text-green-400')
            
            if not gainers:
                ui.label("No gainers today.").classes('text-gray-400 italic')
            for g in gainers:
                with ui.card().classes('w-full p-4 mb-2 bg-gray-800 border-l-4 border-green-500 rounded-xl cursor-pointer hover:bg-gray-700 transition-colors shadow-md').on('click', lambda s=g['Symbol']: ui.navigate.to(f'/stock/{s}')):
                    with ui.row().classes('w-full justify-between items-center'):
                        with ui.column().classes('gap-0'):
                            ui.label(g['Symbol']).classes('font-bold text-white text-lg')
                            ui.label(g['Company Name']).classes('text-sm text-gray-400')
                        ui.label(f"+{g['Return %']:.2f}%").classes('text-2xl font-black text-green-400')
                        
        with ui.column().classes('flex-1 w-full'):
            with ui.row().classes('items-center gap-2 mb-4'):
                ui.icon('trending_down').classes('text-2xl text-red-400')
                ui.label("Top 5 Losers").classes('text-2xl font-bold text-red-400')
                
            if not losers:
                ui.label("No losers today.").classes('text-gray-400 italic')
            for l in losers:
                with ui.card().classes('w-full p-4 mb-2 bg-gray-800 border-l-4 border-red-500 rounded-xl cursor-pointer hover:bg-gray-700 transition-colors shadow-md').on('click', lambda s=l['Symbol']: ui.navigate.to(f'/stock/{s}')):
                    with ui.row().classes('w-full justify-between items-center'):
                        with ui.column().classes('gap-0'):
                            ui.label(l['Symbol']).classes('font-bold text-white text-lg')
                            ui.label(l['Company Name']).classes('text-sm text-gray-400')
                        ui.label(f"{l['Return %']:.2f}%").classes('text-2xl font-black text-red-400')
