from nicegui import ui

def render_about_page():
    with ui.row().classes('items-center gap-2 mb-6 mt-4'):
        ui.icon('info').classes('text-4xl text-blue-400')
        ui.label("About This Project").classes('text-4xl font-bold text-white')
        
    with ui.card().classes('w-full max-w-4xl bg-gray-800 rounded-3xl p-8 border border-gray-700 shadow-xl mx-auto'):
        # Project Objective
        ui.label("Project Objective").classes('text-2xl font-bold text-blue-400 mb-2')
        ui.label(
            "This Indian Stock Analytics Dashboard was developed as an academic project to demonstrate the seamless integration of real-time financial data fetching, processing, and visualization entirely using Python. The objective is to provide a comprehensive, clean, and highly interactive overview of major indices like NIFTY 50 and SENSEX 30, alongside the performance tracking of individual equities."
        ).classes('text-lg text-gray-300 leading-relaxed mb-8')
        
        # Technologies Used
        ui.label("Technologies Used").classes('text-2xl font-bold text-blue-400 mb-2')
        with ui.row().classes('gap-4 mb-8 flex-wrap'):
            techs = ["Python 3", "NiceGUI", "Plotly", "TailwindCSS", "Pandas", "AG Grid"]
            for tech in techs:
                ui.label(tech).classes('bg-gray-700 text-white px-4 py-2 rounded-full font-semibold shadow-sm border border-gray-600')
                
        # Data Source
        ui.label("Data Source").classes('text-2xl font-bold text-blue-400 mb-2')
        ui.label("All financial data, including historical prices, index values, and company profiles, is retrieved dynamically from Yahoo Finance via the open-source yfinance library.").classes('text-lg text-gray-300 leading-relaxed mb-8')
        
        ui.separator().classes('my-6')
        
        # Author
        with ui.row().classes('items-center gap-2 justify-center w-full'):
            ui.icon('code').classes('text-3xl text-gray-400')
            ui.label("Designed & Developed by:").classes('text-xl text-gray-400')
            ui.label("Saikiran Jogu").classes('text-2xl font-extrabold text-white tracking-wide ml-1')
