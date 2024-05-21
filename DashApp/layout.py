import dash_core_components as dcc
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Define constants
INIT_MODAL_HEADER_FONT_GENERAL = "Arial"
INIT_MODAL_HEADER_FONT_SIZE = "24px"
INIT_MODAL_HEADER_FONT_WEIGHT = "bold"
INIT_BUTTON_OPACITY = 0.8
INIT_BUTTON_SIZE = "md"
INIT_LOADER_TYPE = "circle"
INIT_LOADER_CHART_COMPONENT_COLOR = "#515A5A"
INIT_LINE_H = "80vh"
INIT_MODAL_FOOTER_FONT_SIZE = "14px"
INIT_LINE_MODAL_W = "1000px"
PRIMARY_COLOR = "#097192"
MAIN_COLOR = "#ffffff"


def create_dash_layout_linegraph_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader(
                html.H1(
                    id="line-graph-modal-title",
                    style={
                        "fontFamily": INIT_MODAL_HEADER_FONT_GENERAL,
                        "fontSize": INIT_MODAL_HEADER_FONT_SIZE,
                        "fontWeight": INIT_MODAL_HEADER_FONT_WEIGHT,
                        "color": PRIMARY_COLOR,
                    },
                ),
            ),
            dbc.ModalBody(
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H5("Select countries", style={"color": PRIMARY_COLOR}),
                                        dcc.Dropdown(
                                            options=[],
                                            value=[
                                                "United States of America",
                                                "China",
                                                "India",
                                                "United Kingdom",
                                            ],
                                            id="line-graph-dropdown-countries",
                                            multi=True,
                                            placeholder="Select countries",
                                        ),
                                        dbc.Button(
                                            "Select all countries",
                                            outline=True,
                                            color="secondary",
                                            id="linegraph-allcountries-button",
                                            style={
                                                "marginLeft": 0,
                                                "marginTop": 10,
                                                "marginBottom": 0,
                                                "display": "inline-block",
                                                "opacity": INIT_BUTTON_OPACITY,
                                                "color": PRIMARY_COLOR,
                                            },
                                            size=INIT_BUTTON_SIZE,
                                        ),
                                        dbc.Button(
                                            "Remove all countries",
                                            outline=True,
                                            color="secondary",
                                            id="linegraph-nocountries-button",
                                            style={
                                                "marginLeft": 10,
                                                "marginTop": 10,
                                                "marginBottom": 0,
                                                "display": "inline-block",
                                                "opacity": INIT_BUTTON_OPACITY,
                                                "color": PRIMARY_COLOR,
                                            },
                                            size=INIT_BUTTON_SIZE,
                                        ),
                                        dbc.Tooltip(
                                            "Only for the brave!",
                                            target="linegraph-allcountries-button",
                                            placement="bottom",
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.H5("Change datasets", style={"color": PRIMARY_COLOR}),
                                        dcc.Dropdown(
                                            options=[],
                                            id="line-graph-dropdown-dataset",
                                            multi=False,
                                            placeholder="Select dataset or type to search",
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        dcc.Loading(
                            type=INIT_LOADER_TYPE,
                            color=INIT_LOADER_CHART_COMPONENT_COLOR,
                            children=html.Span(id="my-loader-line-refresh"),
                            style={
                                "zIndex": 1,
                                "display": "flex",
                                "vertical-align": "center",
                                "align-items": "center",
                                "justify-content": "center",
                                "paddingTop": 100,
                            },
                        ),
                        dcc.Graph(
                            id="line-graph",
                            animate=False,
                            style={
                                "backgroundColor": MAIN_COLOR,
                                "color": PRIMARY_COLOR,
                                "height": INIT_LINE_H,
                            },
                            config={"displayModeBar": False},
                        ),
                    ]
                ),
            ),
            dbc.ModalFooter(
                [
                    dbc.Button(
                        "Close",
                        id="modal-line-close",
                        className="mr-1",
                        size=INIT_BUTTON_SIZE,
                        style={"backgroundColor": PRIMARY_COLOR, "color": MAIN_COLOR}
                    ),
                ]
            ),
        ],
        id="dbc-modal-line",
        centered=True,
        size="xl",
        style={"max-width": "none", "width": INIT_LINE_MODAL_W},
    )

def create_dash_layout_comparison_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader("Country Comparison", style={"color": PRIMARY_COLOR}),
            dbc.ModalBody(
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H5("Select first country", style={"color": PRIMARY_COLOR}),
                                        dcc.Dropdown(
                                            options=[],  # Will be populated dynamically
                                            id="comparison-dropdown-country1",
                                            placeholder="Select first country",
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.H5("Select second country", style={"color": PRIMARY_COLOR}),
                                        dcc.Dropdown(
                                            options=[],  # Will be populated dynamically
                                            id="comparison-dropdown-country2",
                                            placeholder="Select second country",
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        html.Br(),
                        dbc.Table(
                            id="comparison-table",
                            bordered=True,
                            hover=True,
                            responsive=True,
                            striped=True,
                        ),
                    ]
                ),
            ),
            dbc.ModalFooter(
                dbc.Button("Close", id="modal-comparison-close", className="mr-1", style={"backgroundColor": PRIMARY_COLOR, "color": MAIN_COLOR})
            ),
        ],
        id="dbc-modal-comparison",
        centered=True,
        size="lg",
    )


def create_map():
    df = pd.read_csv(
        "data/countries.csv"
    )  # Change the path according to your CSV file location
    fig = px.choropleth(
        df,
        locations="country",
        locationmode="country names",
        hover_name="country",
    )
    fig.update_layout(
        coloraxis_showscale=False,
        geo=dict(
            showcoastlines=False,
            showframe=False,
            showland=True,  # Show land
            landcolor="rgb(243, 243, 243)",  # Land color
            countrycolor="rgb(204, 204, 204)",  # Country color
            bgcolor="rgba(0,0,0,0)",  # Set map background color to transparent
            projection_scale=2,  # Projection scale (adjust as needed)
            lonaxis_range=[-180, 180],  # Longitude range
            lataxis_range=[-90, 90],  # Latitude range
            scope="world",
        ),
        margin=dict(l=0, r=0, t=0, b=0),  # Remove margins
    )
    fig.update_geos(fitbounds="locations", visible=False)
    return fig


# Dash application layout
layout = dbc.Container(
    [
        # Header with dropdown menus
        dbc.Row(
            [
                dbc.Col(dcc.Dropdown(id='dropdown-1', options=[{'label': 'Option 1', 'value': '1'}, {'label': 'Option 2', 'value': '2'}], placeholder='Select an option')),
                dbc.Col(dcc.Dropdown(id='dropdown-2', options=[{'label': 'Option 1', 'value': '1'}, {'label': 'Option 2', 'value': '2'}], placeholder='Select an option')),
                dbc.Col(dcc.Dropdown(id='dropdown-3', options=[{'label': 'Option 1', 'value': '1'}, {'label': 'Option 2', 'value': '2'}], placeholder='Select an option')),
                dbc.Col(dcc.Dropdown(id='dropdown-4', options=[{'label': 'Option 1', 'value': '1'}, {'label': 'Option 2', 'value': '2'}], placeholder='Select an option')),
                dbc.Col(dcc.Dropdown(id='dropdown-5', options=[{'label': 'Option 1', 'value': '1'}, {'label': 'Option 2', 'value': '2'}], placeholder='Select an option')),
                dbc.Col(dcc.Dropdown(id='dropdown-6', options=[{'label': 'Option 1', 'value': '1'}, {'label': 'Option 2', 'value': '2'}], placeholder='Select an option')),
                dbc.Col(dcc.Dropdown(id='dropdown-7', options=[{'label': 'Option 1', 'value': '1'}, {'label': 'Option 2', 'value': '2'}], placeholder='Select an option')),
                dbc.Col(dcc.Dropdown(id='dropdown-8', options=[{'label': 'Option 1', 'value': '1'}, {'label': 'Option 2', 'value': '2'}], placeholder='Select an option')),
            ],
            style={'padding': 20}
        ),

        # Main content with map and empty container
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        figure=create_map(),
                        id="background-map",
                        config={"displayModeBar": False},
                        style={"width": "100%", "height": "80vh", "margin": 0, "padding": 0}
                    ),
                    width=8  # 70% width of the row
                ),
                dbc.Col(
                    html.Div(id='empty-container', style={"height": "80vh", "backgroundColor": MAIN_COLOR}),  # Empty container
                    width=4  # 30% width of the row
                ),
            ],
            style={'marginBottom': 20}
        ),

        # Year evolution with play button
        dbc.Row(
            [
                dbc.Col(
                    dcc.Slider(
                        id='year-slider',
                        min=1952,  # Adjust accordingly
                        max=2007,  # Adjust accordingly
                        value=1952,
                        marks={str(year): str(year) for year in range(1952, 2008, 5)},  # Adjust accordingly
                        step=None,
                        included=False,
                        updatemode='drag'
                    ),
                    width=10
                ),
                dbc.Col(
                    dbc.Button(
                        'Play',
                        id='play-button',
                        color='primary',
                        style={'backgroundColor': PRIMARY_COLOR, 'borderColor': PRIMARY_COLOR, 'color': MAIN_COLOR}
                    ),
                    width=2
                ),
            ],
            style={'marginBottom': 20}
        ),
        # Two empty containers for future content
        dbc.Row(
            [
                dbc.Col(
                    html.Div(id='container-1', style={"height": "50vh", "backgroundColor": MAIN_COLOR}),
                    width=6
                ),
                dbc.Col(
                    html.Div(id='container-2', style={"height": "50vh", "backgroundColor": MAIN_COLOR}),
                    width=6
                ),
            ],
            style={'marginBottom': 20}
        ),
        # Buttons for displaying modals
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        "Show Line Graph",
                        id="open-linegraph-modal",
                        color="primary",
                        style={'backgroundColor': PRIMARY_COLOR, 'borderColor': PRIMARY_COLOR, 'color': MAIN_COLOR}
                    ),  # Button to open the modal
                    width=6
                ),
                dbc.Col(
                    dbc.Button(
                        "Show Country Comparison",
                        id="open-comparison-modal",
                        color="primary",
                        style={'backgroundColor': PRIMARY_COLOR, 'borderColor': PRIMARY_COLOR, 'color': MAIN_COLOR}
                    ),  # New button
                    width=6
                ),
            ],
            style={'marginBottom': 20}
        ),
        create_dash_layout_linegraph_modal(),  # Add the modal to the layout
        create_dash_layout_comparison_modal(),  # New comparison modal
    ],
    fluid=True,
    style={"backgroundColor": MAIN_COLOR, "color": PRIMARY_COLOR},
)