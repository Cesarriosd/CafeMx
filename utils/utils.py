import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Sample data (replace with your data or load from a CSV/database)
data = {
    "City": ["La ventosa", "Alvaro Obregón", "Jalcomulco"],
    "Latitude": [16.552777777778 , 16.297222, 19.331944],
    "Longitude": [-94.947222222222, -95.084722,  -96.7625],
    "Compañias extractivistas": [2, 0, 1],
    "Categoría": ["Parque Eólico", "Parque Eólico", "Presa"],
}
data = {
    "City": ["La ventosa", "Guadalajara", "Monterrey", "Cancun", "Tijuana"],
    "Latitude": [16.552777777778 , 20.6597, 25.6866, 21.1619, 32.5149],
    "Longitude": [-94.947222222222, -103.3496, -100.3161, -86.8515, -117.0382],
    "Population": [1, 1495182, 1135512, 888797, 1300983],
    "Category": ["Parque Eólico", "Metropolitan", "Industrial", "Tourism", "Border"],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("ExtractivismoMx", style={"textAlign": "center"}),
    
    # Filters
    html.Div([
        html.Label("Categorias:"),
        dcc.Dropdown(
            id="category-filter",
            options=[{"label": cat, "value": cat} for cat in df["Category"].unique()],
            value=None,
            multi=True,
            placeholder="Select a category"
        ),
        html.Label("Filter by Population Range:"),
        dcc.RangeSlider(
            id="population-slider",
            min=df["Population"].min(),
            max=df["Population"].max(),
            step=100000,
            marks={i: str(i) for i in range(df["Population"].min(), df["Population"].max() + 1, 500000)},
            value=[df["Population"].min(), df["Population"].max()]
        ),
    ], style={"margin": "20px"}),
    
    # Map
    dcc.Graph(id="mexico-map"),
])

# Callback to update the map based on filters
@app.callback(
    Output("mexico-map", "figure"),
    [Input("category-filter", "value"),
     Input("population-slider", "value")]
)
def update_map(selected_categories, population_range):
    # Filter data based on selected categories
    filtered_df = df.copy()
    if selected_categories:
        filtered_df = filtered_df[filtered_df["Category"].isin(selected_categories)]
    
    # Filter data based on population range
    filtered_df = filtered_df[
        (filtered_df["Population"] >= population_range[0]) &
        (filtered_df["Population"] <= population_range[1])
    ]
    
    # Create the map
    fig = px.scatter_mapbox(
        filtered_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="City",
        hover_data=["Population", "Category"],
        zoom=4,
        height=600,
        title="Map of Mexico"
    )
    
    # Customize the map style
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )
    
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)