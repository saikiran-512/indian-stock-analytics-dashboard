from contextlib import contextmanager
from nicegui import ui, app
from dashboard import render_market_overview, render_top_performers
from stock_details import render_stock_details
from index_details import render_index_details
from about import render_about_page
import os

app.add_static_files('/assets', 'assets')

@contextmanager
def layout(page_title):
    ui.page_title(page_title)
    ui.dark_mode().enable()
    
    with ui.header().classes('bg-gray-900 border-b border-gray-700 items-center justify-between p-4'):
        with ui.row().classes('items-center gap-4'):
            ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
            ui.image('/assets/logo.jpg').classes('w-10 h-10 rounded-full border-2 border-gray-700 shadow-md')
            ui.label("Indian Stock Analytics").classes('text-2xl font-bold text-white tracking-tight')
            
    with ui.left_drawer(value=True).classes('bg-gray-900 border-r border-gray-800 p-4') as left_drawer:
        ui.label("Navigation").classes('text-gray-400 text-sm font-bold uppercase mb-4 tracking-wider mt-2')
        with ui.column().classes('w-full gap-2'):
            ui.button('Market Overview', icon='dashboard', on_click=lambda: ui.navigate.to('/')).classes('w-full justify-start text-lg').props('flat color=white')
            ui.button('Top Performers', icon='leaderboard', on_click=lambda: ui.navigate.to('/top-performers')).classes('w-full justify-start text-lg').props('flat color=white')
            ui.button('About', icon='info', on_click=lambda: ui.navigate.to('/about')).classes('w-full justify-start text-lg').props('flat color=white')
            
    with ui.column().classes('w-full max-w-7xl mx-auto p-4 md:p-8 min-h-screen pb-24'):
        yield
        
    with ui.footer().classes('bg-gray-900 border-t border-gray-800 p-6 flex-col items-center justify-center'):
        ui.label("Indian Stock Analytics Dashboard").classes('text-white font-bold text-lg')
        ui.label("Built using Python, NiceGUI, Plotly and yfinance.").classes('text-gray-400 text-sm mt-1')
        ui.label("© 2026 Saikiran").classes('text-gray-500 text-sm mt-2')

@ui.page('/')
def home_page():
    """Renders the market overview page."""
    with layout("Market Overview - Stock Analytics"):
        render_market_overview()

@ui.page('/top-performers')
def top_performers_page():
    """Renders the top performers analytics page."""
    with layout("Top Performers - Stock Analytics"):
        render_top_performers()

@ui.page('/about')
def about_page():
    """Renders the about page."""
    with layout("About - Stock Analytics"):
        render_about_page()

@ui.page('/index/{index_symbol}')
async def index_page(index_symbol: str):
    """Renders the detailed view for an index (gainers, losers)."""
    with layout(f"Index Details - Stock Analytics"):
        await render_index_details(index_symbol)

@ui.page('/stock/{symbol}')
async def stock_page(symbol: str):
    """Renders the detailed view for a specific stock."""
    with layout(f"{symbol} - Stock Analytics"):
        await render_stock_details(symbol)

# Tailwind configuration for custom colors or styles if needed
ui.add_head_html('''
<style>
    body {
        background-color: #111827; /* Tailwind gray-900 */
        color: #f3f4f6; /* Tailwind gray-100 */
    }
    .custom-ag-grid {
        --ag-background-color: #1f2937;
        --ag-header-background-color: #374151;
        --ag-row-hover-color: #4b5563;
        --ag-font-family: inherit;
        color: #f3f4f6;
    }
</style>
''', shared=True)

if __name__ in {"__main__", "__mp_main__"}:
    # Run the NiceGUI server on port 8080
    ui.run(
        title="Indian Stock Analytics Dashboard",
        dark=True,
        port=8080,
        favicon='assets/logo.jpg'
    )
