import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import vizro

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout for the detailed page
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="details-content")
])

@app.callback(
    Output("details-content", "children"),
    [Input("url", "pathname")]
)
def display_detailed_page(pathname):
    if not pathname.startswith("/details/"):
        return dash.no_update

    country = pathname.split("/details/")[1]

    # Use Vizro to create detailed graphs for the selected country
    graphs = vizro.create_country_graphs(country)

    return html.Div([
        html.H2(f"Details for {country}"),
        *graphs
    ])

if __name__ == '__main__':
    app.run_server(debug=True)