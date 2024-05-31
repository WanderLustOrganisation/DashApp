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
INIT_LINE_MODAL_W = '100%'

# Función para crear el modal del gráfico de líneas
def create_dash_layout_linegraph_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader("Line Graph"),
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
                            )
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
        style={"max-width": "none", "width": INIT_LINE_MODAL_W, "margin": "0 auto"}
    )

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
                                options=[],
                                id="comparison-dropdown-country1",
                                placeholder='Select first country',
                            ),
                            html.Div(id='country-info-1'),
                        ]),
                        dbc.Col([
                            html.H5("Select second country"),
                            dcc.Dropdown(
                                id="comparison-dropdown-country2",
                                options=[],
                                placeholder='Select second country',
                            ),
                            html.Div(id='country-info-2'),
                        ]),
                    ]),
                ]),
            ),
            dbc.ModalFooter([
                dbc.Button("Close", id="modal-comparison-close", className="mr-1", size=INIT_BUTTON_SIZE),
            ]),
        ],
        id="dbc-modal-comparison",
        centered=True,
        size="xl",
        style={"max-width": "none", "width": INIT_LINE_MODAL_W, "margin": "0 auto"}
    )

# Layout principal de la aplicación
layout = html.Div([
    dcc.Store(id="user-type-store"),
    dcc.Store(id='user'),
    dcc.Location(id="url", refresh=False),
    
    html.Header(id="header", style={"position": "fixed", "width": "100%", "zIndex": 1000, "top": 0}),
    
    html.Div([
        dbc.Row(id="main-row", style={"--bs-gutter-x": "0"}),  
    ], id="content", style={"padding-top": "56px", "height": "calc(100% - 58px)", "width": "100%", "overflow": "hidden"}),
    
    html.Div(id='page-content'),
    dcc.Store(id='selected-country'),
    
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Country Details")),
            dbc.ModalBody(
                [
                    html.Div(id="country-name"),
                    dcc.Dropdown(id="modal-category-dropdown", placeholder="Select a category"),
                    dcc.Graph(id="gdp-graph"),
                    dcc.Graph(id="population-graph"),
                    dcc.Graph(id="additional-graph-1"),
                    dcc.Graph(id="additional-graph-2"),
                    # Add more graphs as needed
                ]
            ),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-country-details", className="ms-auto", n_clicks=0)
            ),
        ],
        id="country-details-modal",
        size="lg",
    )
])