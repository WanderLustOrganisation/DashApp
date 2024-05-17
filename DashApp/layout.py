import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

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
    m = dbc.Modal(
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
    return m

# Función para crear el modal de comparación de países
def create_dash_layout_comparison_modal():
    m = dbc.Modal(
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
                    html.Br(),
                    dbc.Table(id='comparison-table', bordered=True, hover=True, responsive=True, striped=True)
                ]),
            ),
            dbc.ModalFooter(
                dbc.Button("Close", id="modal-comparison-close", className="mr-1")
            ),
        ],
        id="dbc-modal-comparison",
        centered=True,
        size="lg"
    )
    return m

# Layout de la aplicación Dash
layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='user-type-store'),
    dbc.Row([
        dbc.Col([
            html.H1("Mapa interactivo de población por país")
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Upload(
                id='upload-data',
                children=html.Div(['Drag and Drop or ', html.A('Select a File')]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=False
            )
        ], width=12)
    ], id='upload-row', style={'display': 'none'}),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='visualization-selector',
                options=[
                    {'label': 'Map', 'value': 'map'},
                    {'label': 'Chart', 'value': 'chart'}
                ],
                value='map',
                placeholder='Select visualization type',
                style={'width': '100%'}
            )
        ], width=12)
    ], id='visualization-row', style={'display': 'none'}),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='series-selector',
                placeholder='Select data series',
                style={'width': '100%'}
            )
        ], width=12)
    ], id='series-row', style={'display': 'none'}),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='column-selector',
                placeholder='Select column to plot',
                style={'width': '100%'}
            )
        ], width=12)
    ], id='dropdown-row', style={'display': 'none'}),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='colorscale-selector',
                options=[
                    {'label': 'Viridis', 'value': 'Viridis'},
                    {'label': 'Cividis', 'value': 'Cividis'},
                    {'label': 'Blues', 'value': 'Blues'},
                    {'label': 'Greens', 'value': 'Greens'},
                    {'label': 'Inferno', 'value': 'Inferno'},
                    {'label': 'Magma', 'value': 'Magma'},
                    {'label': 'Plasma', 'value': 'Plasma'},
                    {'label': 'Turbo', 'value': 'Turbo'},
                    {'label': 'YlGnBu', 'value': 'YlGnBu'},
                ],
                value='Plasma',
                placeholder='Select colorscale',
                style={'width': '100%'}
            )
        ], width=12)
    ], id='colorscale-row', style={'display': 'none'}),
    dbc.Row([
        dbc.Col([
            dcc.Loading(
                id='loading',
                type='default',
                children=dcc.Graph(id='map-graph', style={'height': '80vh'})
            )
        ], width=9),
        dbc.Col([
            dcc.Checklist(
                id='country-selector',
                options=[],
                value=['Spain', 'United States', 'Argentina'],
                style={'height': '80vh', 'overflowY': 'auto'}
            )
        ], width=3, id='country-row', style={'display': 'none'})
    ]),
    html.Div(id='reload-div'),
    dbc.Button("Show Line Graph", id="open-linegraph-modal", color="primary", className="mr-1"),  # Botón para abrir el modal
    dbc.Button("Show Country Comparison", id="open-comparison-modal", color="primary", className="mr-1"),  # New button
    create_dash_layout_linegraph_modal(),  # Añadir el modal al layout
    create_dash_layout_comparison_modal()  # New comparison modal
], fluid=True)
