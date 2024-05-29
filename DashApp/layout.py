import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import dash  # Added this line to import the dash module

# Load the dataset once at the start
df_master = pd.read_parquet("DashApp/data/master.parquet")
first_series = df_master['Series'].unique()[0] if 'Series' in df_master.columns else None

# Definición de constantes
INIT_MODAL_HEADER_FONT_GENERAL = 'Arial'
INIT_MODAL_HEADER_FONT_SIZE = '24px'
INIT_MODAL_HEADER_FONT_WEIGHT = 'bold'
INIT_BUTTON_OPACITY = 0.8
INIT_BUTTON_SIZE = 'md'
INIT_LOADER_TYPE = 'circle'
INIT_LOADER_CHART_COMPONENT_COLOR = '#515A5A'
INIT_LINE_H = '80vh'
INIT_MODAL_FOOTER_FONT_SIZE = '14px'
INIT_LINE_MODAL_W = '1000px'

# Función para crear el modal del gráfico de líneas
def create_dash_layout_linegraph_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader(
                html.H1(
                    id="line-graph-modal-title",
                    style={
                        "fontFamily": INIT_MODAL_HEADER_FONT_GENERAL,
                        "fontSize": INIT_MODAL_HEADER_FONT_SIZE,
                        "fontWeight": INIT_MODAL_HEADER_FONT_WEIGHT
                    },
                ),
            ),
            dbc.ModalBody(
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.H5("Select countries"),
                            dcc.Dropdown(
                                options=[],
                                value=['United States of America', 'China', 'India', 'United Kingdom'],
                                id="line-graph-dropdown-countries",
                                multi=True,
                                placeholder='Select countries',
                            ),
                            dbc.Button(
                                "Select all countries",
                                outline=True,
                                color="secondary",
                                id="linegraph-allcountries-button",
                                style={"marginLeft": 0, 'marginTop': 10, "marginBottom": 0, 'display': 'inline-block', 'opacity': INIT_BUTTON_OPACITY},
                                size=INIT_BUTTON_SIZE
                            ),
                            dbc.Button(
                                "Remove all countries",
                                outline=True,
                                color="secondary",
                                id="linegraph-nocountries-button",
                                style={"marginLeft": 10, 'marginTop': 10, "marginBottom": 0, 'display': 'inline-block', 'opacity': INIT_BUTTON_OPACITY},
                                size=INIT_BUTTON_SIZE
                            ),
                            dbc.Tooltip(
                                "Only for the brave!",
                                target='linegraph-allcountries-button',
                                placement='bottom',
                            ),
                        ]),
                        dbc.Col([
                            html.H5("Change datasets"),
                            dcc.Dropdown(
                                options=[],
                                id="line-graph-dropdown-dataset",
                                multi=False,
                                placeholder='Select dataset or type to search'
                            ),
                        ]),
                    ]),
                    dcc.Loading(
                        type=INIT_LOADER_TYPE,
                        color=INIT_LOADER_CHART_COMPONENT_COLOR,
                        children=html.Span(id="my-loader-line-refresh"),
                        style={"zIndex": 1, 'display': 'flex', 'vertical-align': 'center', 'align-items': 'center', 'justify-content': 'center', 'paddingTop': 100},
                    ),
                    dcc.Graph(
                        id='line-graph',
                        animate=False,
                        style={"backgroundColor": "#1a2d46", 'color': '#ffffff', 'height': INIT_LINE_H},
                        config={'displayModeBar': False},
                    ),
                ]),
            ),
            dbc.ModalFooter([
                dbc.Button("Close", id="modal-line-close", className="mr-1", size=INIT_BUTTON_SIZE),
            ]),
        ],
        id="dbc-modal-line",
        centered=True,
        size="xl",
        style={"max-width": "none", "width": INIT_LINE_MODAL_W}
    )

# Función para crear el modal de comparación de países
def create_dash_layout_comparison_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader("Country Comparison"),
            dbc.ModalBody(
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.H5("Select first country"),
                            dcc.Dropdown(
                                options=[],  # Will be populated dynamically
                                id="comparison-dropdown-country1",
                                placeholder='Select first country',
                            ),
                        ]),
                        dbc.Col([
                            html.H5("Select second country"),
                            dcc.Dropdown(
                                options=[],  # Will be populated dynamically
                                id="comparison-dropdown-country2",
                                placeholder='Select second country',
                            ),
                        ]),
                    ]),
                    dcc.Graph(
                        id='comparison-graph',
                        animate=False,
                        style={"backgroundColor": "#1a2d46", 'color': '#ffffff', 'height': INIT_LINE_H},
                        config={'displayModeBar': False},
                    ),
                ]),
            ),
            dbc.ModalFooter([
                dbc.Button("Close", id="modal-comparison-close", className="mr-1", size=INIT_BUTTON_SIZE),
            ]),
        ],
        id="dbc-modal-comparison",
        centered=True,
        size="xl",
        style={"max-width": "none", "width": INIT_LINE_MODAL_W}
    )

# Layout principal de la aplicación
layout = html.Div([
    html.Header([
        html.Nav([
            dcc.Dropdown(
                id="choose-category-dropdown",
                options=[],  # Will be populated dynamically
                placeholder="Choose Category",
                searchable=True,
                style={"width": "1000px", "display": "inline-block", "margin-right": "10px"},
                value="default_category"  # Set a default category value
            ),
            dcc.Dropdown(
                id="choose-country-dropdown",
                options=[],  # Will be populated dynamically
                placeholder="Choose Country",
                searchable=True,
                style={"width": "300px", "display": "inline-block"},
            ),
        ], className="navbar navbar-expand-lg navbar-light bg-light")
    ], style={"position": "fixed", "width": "100%", "zIndex": 1000, "top": 0}),
    dcc.Store(id="user-type-store"),
    dcc.Location(id="url", refresh=False),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id="map-graph",
                style={"height": "90vh"}, 
                config={"responsive": True},
            ),
        ], width=7),
        dbc.Col([
            html.Div(id='country-info', style={"height": "100vh", "backgroundColor": "#FFFFFF"}),  # Container for displaying country data
            dbc.Button("See More", id="see-more-btn", style={"display": "none"}),  # Button to see more details
        ], width=4),
    ], style={"height": "100vh", "width": "100vw", "position": "relative", "top": "58px",  "left": 0, "--bs-gutter-x": "0"}),  # Adjusted top to start below the header
    create_dash_layout_linegraph_modal(),
    create_dash_layout_comparison_modal(),
    html.Div([
        dbc.Button("Show Line Graph", id="show-line-graph-btn", className="mr-2"),
        dbc.Button("Show Country Comparison", id="show-country-comparison-btn", className="mr-2"),
    ], style={"position": "fixed", "bottom": "10px", "width": "100%", "text-align": "center"})
])
