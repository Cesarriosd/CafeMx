import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd

# Sample data (replace with your data or load from a CSV/database)
data = {
    "Localidad": ["Ixhuacán de los Reyes", "Santa María Yucuhiti", "Mexico City"],
    "Finca": ["Coralillo", 'La promesa IV', "Urban Garden"],
    "Latitude": [19.355278, 17.016667, 19.4326],
    "Longitude": [-97.1175, -97.808333, -99.1332],
    "Variedad": ["Sarchimor", "Ana café", "Typica"],
    "Productor": ["NA", "Rodolfo Feria García", "Local Farmer"],
    "Perfil": ["Frutal", 'Citrico', "Balanced"],
    "Variedad_details": ['https://varieties.worldcoffeeresearch.org/varieties/t5296', 'https://varieties.worldcoffeeresearch.org/es/variedades/anacafe-14', 'https://varieties.worldcoffeeresearch.org/varieties/typica'],
    "Estado": ['Veracruz', 'Oaxaca', 'CDMX'] 
}
df_columns_of_interest = ["Variedad", "Perfil",'Estado']
# Create a DataFrame
df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the initial center and zoom for Mexico City
initial_lat = 21.12908
initial_lon = -101.67374
initial_zoom = 3.9

# Layout of the dashboard
app.layout = html.Div([
    html.H1("CaféMx☕", style={"textAlign": "center"}),

    # Filters section (side by side)
    html.Div([
        # Category Filter
        html.Div([
            html.Label("Variedad"),
            dcc.Dropdown(
                id="Variedad-filtro",
                options=[{"label": cat, "value": cat} for cat in df["Variedad"].unique()],
                value=None,
                multi=True,
                placeholder="Selecciona una variedad"
            ),
        ], style={"width": "48%", "display": "inline-block", "marginRight": "2%"}),

        # City Filter
        html.Div([
            html.Label("Perfil"),
            dcc.Dropdown(
                id="Perfil-filtro",
                options=[{"label": empresa, "value": empresa} for empresa in df["Perfil"].unique()],
                value=None,
                multi=True,
                placeholder="Qué perfil prefieres?"
            ),
        ], style={"width": "48%", "display": "inline-block"}),
    ], style={"margin": "20px", "display": "flex"}),  # Use flexbox for side-by-side layout

    # Main content: Map on the left, Table on the right
    html.Div([
        # Map
        html.Div(
            dcc.Graph(id="mexico-map"),
            style={"width": "50%", "display": "inline-block"}
        ),

        # Table
        html.Div(
            dash_table.DataTable(
                id="data-table",
                columns=[
                    {"name": col, "id": col, "presentation": "markdown"} if col == "Variedad" else {"name": col, "id": col}
                    for col in df_columns_of_interest
                ],
                data=[
                    {**row, "Variedad": f'[{row["Variedad"]}]({row["Variedad_details"]})'}
                    for row in df.to_dict("records")
                ],
                style_table={"height": "600px", "overflowY": "auto"},
                style_cell={"textAlign": "left", "padding": "10px"},
                style_header={"backgroundColor": "lightgray", "fontWeight": "bold", "textAlign": "left", "padding": "10px", "fontFamily": "Arial, sans-serif"},
            ),
            style={"width": "50%", "display": "inline-block", "padding": "20px"}
        ),
    ], style={"display": "flex"}),
])

# Callback to update the map and table based on filters
@app.callback(
    [Output("mexico-map", "figure"),
     Output("data-table", "data")],
    [Input("Variedad-filtro", "value"),
     Input("Perfil-filtro", "value")]
)
def update_dashboard(selected_categories, selected_cities):
    # Filter data based on selected categories
    filtered_df = df.copy()
    if selected_categories:
        filtered_df = filtered_df[filtered_df["Variedad"].isin(selected_categories)]

    # Filter data based on selected cities
    if selected_cities:
        filtered_df = filtered_df[filtered_df["Perfil"].isin(selected_cities)]

    # Create the map with colors based on the Category column
    fig = px.scatter_mapbox(
        filtered_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Finca",
        hover_data=["Variedad", "Perfil"],
        color="Perfil",  # Color points by the Category column
        color_discrete_map={
            "Frutal": "rgb( 0, 255, 7 )",
            "Citrico": "rgb( 244, 208, 63 )",
            "Balanced": "green"
        },
        size_max=1000,
        zoom=initial_zoom,
        height=700,
        title="Map of Mexico",
        center=dict(lat=initial_lat, lon=initial_lon) # Set the initial center
    )
    fig.update_traces(marker=dict(size=10)) # Try a value like 20
    # Customize the map style
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )

    # Update the table data to include markdown for the link
    table_data = [
        {
            **row,
            "Variedad": f'[{row["Variedad"]}]({row["Variedad_details"]})'
        }
        for row in filtered_df.to_dict("records")
    ]

    return fig, table_data

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)