from pathlib import Path

import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed" / "yearly"
app = dash.Dash(__name__)

old_countries = ["France", "Germany", "Italy", "Belgium", "Spain"]
available_years = [2024, 2020, 2000, 1980, 1960, 1940, 1920, 1910]


def load_data(year):
    file_path = DATA_DIR / f"clean_data_peryear{year}.csv"
    if not file_path.is_file():
        raise FileNotFoundError(
            f"Data for {year} was not found at {file_path}. "
            "Run src/cycling_globalisation/processing.py first."
        )

    df = pd.read_csv(file_path)
    df["type"] = df["country"].apply(
        lambda country: (
            "Old Countries" if country in old_countries else "New Countries"
        )
    )
    return df


app.layout = html.Div([
    html.H1("Dashboard - Globalisation du Cyclisme"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in available_years],
        value=available_years[0],
        clearable=False
    ),
    html.Div([
        dcc.Graph(id="stacked_histogram")
    ], style={'margin-bottom': '50px'}),
    html.Div([
        dcc.Graph(id="world-map")
    ])
])


@app.callback(
    Output('stacked_histogram', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_histogram(selected_year):
    df = load_data(selected_year)
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=df[df['type'] == 'Old Countries']['points'],
        name='pays traditionnels : France, Belgique, Espagne, Italy, Allemagne',
        marker_color='blue',
        xbins=dict(start=1, end=50000, size=5000)
    ))
    fig.add_trace(go.Histogram(
        x=df[df['type'] == 'New Countries']['points'],
        name='pays émergents',
        marker_color='green',
        xbins=dict(start=1, end=50000, size=5000)
    ))
    fig.update_layout(
        barmode='stack',
        title=f"Globalisation du Cyclisme - Distribution des Points ({selected_year})",
        xaxis_title="Points marqués",
        yaxis_title="Nombre de pays (log)",
        yaxis_type="log",
        xaxis_type="linear",
        legend_title="Type de pays"
    )
    return fig


@app.callback(
    Output('world-map', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_map(selected_year):
    df = load_data(selected_year)
    geo_data = (
        px.data.gapminder()
        .groupby('country')
        .first()
        .reset_index()[['country', 'iso_alpha']]
    )
    df = pd.merge(df, geo_data, on='country', how='left')
    fig = px.scatter_geo(
        df,
        locations="iso_alpha",
        size="points",
        hover_name="country",
        color="type",
        projection="natural earth",
        title=f"Points marqués par pays en {selected_year}",
        size_max=50,
        color_discrete_map={'Old Countries': 'blue', 'New Countries': 'green'}
    )
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        ),
        legend_title="Type de pays",
    )

    return fig


if __name__ == '__main__':
    app.run(debug=True, port=8051)

