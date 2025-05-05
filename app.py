import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Cargar datos
url = 'BDSuperstore.csv'
df = pd.read_csv(url, encoding='latin1')
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%Y')

# Inicializar la app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Layout
app.layout = dbc.Container([
    html.H1("Tablero de Ventas - Superstore", className="text-center my-4"),
    
    dbc.Row([
        dbc.Col([
            html.H5("Gráfico de líneas: Ventas por fecha"),
            dcc.Graph(id='line-graph'),
            dcc.DatePickerRange(
                id='date-range',
                min_date_allowed=df['Order Date'].min(),
                max_date_allowed=df['Order Date'].max(),
                start_date=df['Order Date'].min(),
                end_date=df['Order Date'].max()
            )
        ], width=6),

        dbc.Col([
            html.H5("Gráfico de barras: Ventas por categoría"),
            dcc.Graph(id='bar-graph'),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': r, 'value': r} for r in df['Region'].unique()],
                value=df['Region'].unique()[0]
            )
        ], width=6)
    ]),

    dbc.Row([
        dbc.Col([
            html.H5("Gráfico de pastel: Segmento de clientes"),
            dcc.Graph(id='pie-graph'),
            dcc.RadioItems(
                id='category-radio',
                options=[{'label': c, 'value': c} for c in df['Category'].unique()],
                value=df['Category'].unique()[0],
                inline=True
            )
        ], width=6),

        dbc.Col([
            html.H5("Dispersión: Ventas vs Ganancias"),
            dcc.Graph(id='scatter-graph'),
            html.Button("Cambiar color de fondo", id='bg-btn', n_clicks=0)
        ], width=6)
    ])
])

# Callbacks
@app.callback(
    Output('line-graph', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_line(start_date, end_date):
    dff = df[(df['Order Date'] >= start_date) & (df['Order Date'] <= end_date)]
    dff_grouped = dff.groupby('Order Date')['Sales'].sum().reset_index()
    fig = px.line(dff_grouped, x='Order Date', y='Sales', title='Ventas en el tiempo')
    fig.update_xaxes(rangeslider_visible=True)
    return fig

@app.callback(
    Output('bar-graph', 'figure'),
    Input('region-dropdown', 'value')
)
def update_bar(region):
    dff = df[df['Region'] == region]
    fig = px.bar(dff.groupby('Category')['Sales'].sum().reset_index(), x='Category', y='Sales',
                 title=f'Ventas por Categoría - Región {region}')
    return fig

@app.callback(
    Output('pie-graph', 'figure'),
    Input('category-radio', 'value')
)
def update_pie(category):
    dff = df[df['Category'] == category]
    fig = px.pie(dff, names='Segment', values='Sales', title=f'Segmentos - {category}')
    return fig

@app.callback(
    Output('scatter-graph', 'figure'),
    Input('bg-btn', 'n_clicks')
)
def update_scatter(n):
    fig = px.scatter(df, x='Sales', y='Profit', color='Sub-Category', title='Ventas vs Ganancias')
    if n % 2 == 1:
        fig.update_layout(paper_bgcolor='lightgrey')
    return fig

# Run
if __name__ == '__main__':
    app.run_server(debug=True)

