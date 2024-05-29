import dash
from dash import html
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css",
    ],
)
app.layout = dbc.Container(
    html.Header(
        dbc.Container(
            dbc.Nav(
                [
                    dbc.NavItem(
                        dbc.NavLink(
                            html.I(
                                className="fa-solid fa-house",
                                style={"font-size": "1.5rem", "color": "#097192"},
                            ),
                            href="#",
                        ),
                        className="d-flex align-items-center w-25",
                    ),
                    dbc.NavItem(
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.DropdownMenu(
                                        label="Dropdown 1",
                                        children=[
                                            dbc.DropdownMenuItem("Action 1", href="#"),
                                            dbc.DropdownMenuItem("Action 2", href="#"),
                                            dbc.DropdownMenu(
                                                label="Submenu",
                                                children=[
                                                    dbc.DropdownMenuItem(
                                                        "Sub-action 1", href="#"
                                                    ),
                                                    dbc.DropdownMenuItem(
                                                        "Sub-action 2", href="#"
                                                    ),
                                                ],
                                                in_navbar=True,
                                                nav=True,
                                            ),
                                        ],
                                        className="me-2",
                                    ),
                                ),
                                dbc.Col(
                                    dbc.DropdownMenu(
                                        label="Dropdown 2",
                                        children=[
                                            dbc.DropdownMenuItem("Action", href="#"),
                                            dbc.DropdownMenuItem(
                                                "Another action", href="#"
                                            ),
                                            dbc.DropdownMenuItem(
                                                "Something else here", href="#"
                                            ),
                                        ],
                                        className="me-2",
                                    ),
                                ),
                            ],
                            className="g-2",
                        ),
                        className="d-flex align-items-center w-75",
                    ),
                ],
                className="d-flex justify-content-between align-items-center",
            ),
            fluid=True,
            style={
                "background-color": "rgba(255, 255, 255, 0.8)"
            },  # Fondo transparente
        )
    ),
    dbc.Container(
        
    )
)

if __name__ == "__main__":
    app.run_server()
