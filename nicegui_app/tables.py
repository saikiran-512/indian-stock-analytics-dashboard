from nicegui import ui

def create_analytics_table(data):
    """Creates a responsive, sortable, and paginated table for stock data."""
    if not data:
        ui.label("No data available.").classes('text-gray-400 italic')
        return

    # Create invisible native HTML links so navigation is handled 100% by the browser
    for row in data:
        symbol = row['Symbol']
        name = row['Company Name']
        # styled to inherit color and no underline so it looks like plain text
        link_style = "color: inherit; text-decoration: none; cursor: pointer; display: block; width: 100%;"
        row['Symbol_Link'] = f"<a href='/stock/{symbol}' style='{link_style}'>{symbol}</a>"
        row['Company_Link'] = f"<a href='/stock/{symbol}' style='{link_style}'>{name}</a>"

    columns = [
        {'headerName': 'Rank', 'field': 'Rank', 'width': 80, 'sortable': True},
        {'headerName': 'Symbol', 'field': 'Symbol_Link', 'sortable': True, 'filter': True},
        {'headerName': 'Company Name', 'field': 'Company_Link', 'flex': 1, 'sortable': True, 'filter': True},
        {
            'headerName': 'Current Price', 
            'field': 'Current Price', 
            'sortable': True,
            'valueFormatter': "value ? '₹' + value.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) : 'N/A'"
        },
        {
            'headerName': 'Return %', 
            'field': 'Return %', 
            'sortable': True,
            'cellStyle': "params.value >= 0 ? {color: '#10b981'} : {color: '#ef4444'}",
            'valueFormatter': "value ? value.toFixed(2) + '%' : 'N/A'"
        }
    ]

    # NiceGUI's aggrid wrapper
    grid = ui.aggrid({
        'columnDefs': columns,
        'rowData': data,
        'rowSelection': 'single',
        'pagination': True,
        'paginationPageSize': 25,
        'defaultColDef': {
            'resizable': True,
        }
    }, html_columns=[1, 2]).classes('w-full h-[500px] custom-ag-grid')
    
    ui.label("Click on any stock name or symbol to view full details.").classes('text-sm text-gray-500 mt-2')
