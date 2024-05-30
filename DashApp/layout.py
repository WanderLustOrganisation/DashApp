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
    html.Header([
        html.Nav([
            dcc.Dropdown(
                id="choose-category-dropdown",
                options=[], 
                placeholder="Choose Category",
                searchable=True,
                style={"flex": "0 0 calc(60% - 10px)", "width": "100%"},
                value="Population density"  # Set the default value here
            ),
            dcc.Dropdown(
                id="choose-country-dropdown",
                options=[],  # Will be populated dynamically
                placeholder="Choose Country",
                searchable=True,
                style={"flex": "0 0 calc(40% - 10px)", "width": "100%"},
            ),
        ], className="navbar navbar-expand-lg navbar-light bg-light", style={"padding":"10px 20px", "gap":"20px"})
    ], style={"position": "fixed", "width": "100%", "zIndex": 1000, "top": 0}),
    
    html.Div([
        dcc.Store(id="user-type-store"),
        dcc.Location(id="url", refresh=False),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id="map-graph",
                    style={"height": "90vh"}, 
                    config={"responsive": True},
                ),
            ], style={"flex": "0 0 80%", "box-sizing": "border-box"}),
            dbc.Col([
                html.Div(id='country-info', style={"backgroundColor": "#FFFFFF"}), 
                dbc.Button("See More", id="see-more-btn", style={"display": "none"}),  
                create_dash_layout_linegraph_modal(),
                create_dash_layout_comparison_modal(),
                html.Div([
                    dbc.Button("Show Line Graph", id="show-line-graph-btn", className="mr-2"),
                    dbc.Button("Show Country Comparison", id="show-country-comparison-btn", className="mr-2"),
                ], style={"display": "flex", "flex-direction": "column", "gap":"8px", "margin-top": "auto", "text-align": "center"})
            ], style={"padding": "2%", "flex": "0 0 20%", "box-sizing": "border-box", "display": "flex", "flex-direction": "column"}),
        ], style={"--bs-gutter-x": "0"}),  
    ], id="content", style={"padding-top": "56px", "height": "calc(100% - 58px)", "width": "100%", "overflow": "hidden"}),
    html.Div(id='page-content'),
    dcc.Store(id='selected-country')
])
