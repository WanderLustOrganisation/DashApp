import dash
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import numpy as np
import pandas as pd
from dash import dcc
import dash_bootstrap_components as dbc
import layout as layout
from database import Database

# Load the dataset once at the start
df_master = pd.read_parquet("DashApp/data/master.parquet")

def create_map():
    df = pd.read_csv("DashApp/data/countries.csv")
    fig = px.choropleth(
        df,
        locations="country",
        locationmode="country names",
        hover_name="country",
    )
    fig.update_layout(
        coloraxis_showscale=True,
        coloraxis=dict(colorbar=dict(x=-0.1)),  # Move colorscale to the left
        geo=dict(
            showcoastlines=False,
            showframe=False,
            showland=True,
            landcolor="rgb(243, 243, 243)",
            countrycolor="rgb(204, 204, 204)",
            bgcolor="rgba(0,0,0,0)",
            projection_scale=0.8,  
            lonaxis_range=[-180, 180],
            lataxis_range=[-90, 90],
            scope="world",
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )
    fig.update_geos(fitbounds="locations", visible=False)
    return fig

def register_callbacks(app):
    @app.callback(Output("user-type-store", "data"), [Input("url", "href")])
    def store_user_type(href):
        if href is None:
            return 0  # Default value if no information in URL
        user_type = href.split("user_type=")[1] if "user_type=" in href else 0
        return int(user_type)

    @app.callback(Output("user", "data"), [Input("url", "href")])
    def store_user_id(href):
        if href is None:
            return 0  
        user = href.split("user=")[1] if "user=" in href else 0
        return int(user)
        
    @app.callback(
        Output("main-row", "children"),
        [Input("user-type-store", "data")]
    )
    def update_layout(user_type):
        map_graph_col = dbc.Col([
            dcc.Graph(
                id="map-graph",
                style={"height": "90vh"},
                config={"responsive": True},
            ),
        ], id="map-graph-col", style={"flex": "0 0 80%", "box-sizing": "border-box"})
        
        country_info_div = html.Div(id='country-info', style={"backgroundColor": "#FFFFFF"})
        
        if user_type == 0:
            controls_col = dbc.Col([
                country_info_div
            ], id="controls-col", style={"padding": "2%", "flex": "0 0 20%", "box-sizing": "border-box", "display": "flex", "flex-direction": "column"})
        else:
            controls_col = dbc.Col([
                country_info_div,
                dbc.Button("See More", id="see-more-btn", style={"display": "none"}),
                layout.create_dash_layout_linegraph_modal(),
                layout.create_dash_layout_comparison_modal(),
                html.Div([
                    dbc.Button("Show Line Graph", id="show-line-graph-btn", className="mr-2"),
                    dbc.Button("Show Country Comparison", id="show-country-comparison-btn", className="mr-2"),
                ], style={"display": "flex", "flex-direction": "column", "gap": "8px", "margin-top": "auto", "text-align": "center"})
            ], id="controls-col", style={"padding": "2%", "flex": "0 0 20%", "box-sizing": "border-box", "display": "flex", "flex-direction": "column"})
        
        return [map_graph_col, controls_col]

    @app.callback(
        Output("header", "children"),
        [Input("user-type-store", "data")]
    )
    def update_header(user_type):
        if user_type == 0:
            return html.Nav([
                dcc.Dropdown(
                    id="choose-country-dropdown",
                    options=[],  
                    placeholder="Choose Country",
                    searchable=True,
                    style={"flex": "0 0 100%", "width": "100%"},
                ),
            ], className="navbar navbar-expand-lg navbar-light bg-light", style={"padding": "10px 20px", "gap": "10px"})
        else:
            return html.Nav([
                dcc.Dropdown(
                    id="choose-category-dropdown",
                    options=[], 
                    placeholder="Choose Category",
                    searchable=True,
                    style={"flex": "0 0 calc(50% - (20px/3))", "width": "100%"},
                ),
                dcc.Dropdown(
                    id="choose-country-dropdown",
                    options=[],  
                    placeholder="Choose Country",
                    searchable=True,
                    style={"flex": "0 0 calc(35% - (20px/3))", "width": "100%"},
                ),
                dcc.Dropdown(
                    id="choose-language-dropdown",
                    options=[], 
                    placeholder="Choose Language",
                    searchable=True,
                    style={"flex": "0 0 calc(15% - (20px/3))", "width": "100%"},
                ),
            ], className="navbar navbar-expand-lg navbar-light bg-light", style={"padding": "10px 20px", "gap": "10px"})


    @app.callback(
        [Output("choose-category-dropdown", "options"),
        Output("choose-category-dropdown", "value")],
        [Input("user-type-store", "data")]
    )
    def update_choose_category_dropdown(user_type):
        if df_master is None or 'Series' not in df_master.columns:
            return [], None

        series = df_master['Series'].unique()
        options = [{"label": serie, "value": serie} for serie in series]
        default_value = "Population density" if "Population density" in series else series[0]  # Set the default value
        return options, default_value

    # Conexión a la base de datos
    db = Database(host="localhost", user="user", password="user", database="probak")
    db.connect()

    @app.callback(
        [Output("choose-language-dropdown", "options"),
        Output("choose-language-dropdown", "value")],
        [Input("user", "data")]
    )
    def update_choose_language_dropdown(user):
        if user == 0:
            return [], None

        query = f"select hizkuntzak.hizkuntza from hizkuntzak, erabiltzaileen_hizkuntzak where hizkuntzak.hizkuntzaID = erabiltzaileen_hizkuntzak.hizkuntzaID and erabiltzaileen_hizkuntzak.erabiltzaileaID = {user}"
        results = db.execute_query(query)

        if results is None:
            return [], None  

        options = [{"label": language, "value": language} for (language,) in results]
        default_value = results[0][0] if results else None 

        return options, default_value
    '''
    @app.server.before_first_request
    def close_db_connection():
        db.disconnect()
    '''
    @app.callback(
        Output("choose-country-dropdown", "options"),
        [Input("user-type-store", "data")]
    )
    def update_choose_country_dropdown(user_type):
        if df_master is None or 'Country' not in df_master.columns:
            return []

        countries = df_master['Country'].unique()
        options = [{"label": country, "value": country} for country in countries]
        return options

    @app.callback(
        Output("map-graph", "figure"),
        [
            Input("choose-category-dropdown", "value"),
            Input("choose-country-dropdown", "value"),
            Input("user-type-store", "data"),
        ]
    )
    def update_map(selected_category, selected_country, user_type):
        if user_type == 0:
            return create_map()

        if selected_category is None:
            return {}

        df = df_master[df_master['Series'] == selected_category]

        if 'Country' not in df.columns:
            return {}

        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
        df = df[df['Value'] > 0]

        if selected_country:
            df = df[df['Country'] == selected_country]

        if df.empty:
            return {}

        df['Log_Value'] = np.log10(df['Value'])
        min_val = df['Log_Value'].min()
        df['Normalized_Log'] = df['Log_Value'] - min_val

        max_val = df['Normalized_Log'].max()
        ticks = np.linspace(0, max_val, num=8)
        ticktext = [f"{10**(x + min_val):.2f}" for x in ticks]

        fig = px.choropleth(
            df,
            locations="Country",
            locationmode="country names",
            color='Normalized_Log',
            hover_name="Country",
            animation_frame="Year",
            color_continuous_scale="Blues",
            # color_continuous_scale="Viridis",
            hover_data={"Value": True, "Log_Value": True, "Normalized_Log": False},
            range_color=(0, max_val)
        )

        fig.update_layout(
            coloraxis_showscale=True,
            coloraxis=dict(
                colorbar=dict(
                    x=-0.1,
                    tickvals=ticks,
                    ticktext=ticktext,
                )
            ),
            geo=dict(
                showcoastlines=False,
                showframe=False,
                showland=True,
                landcolor="rgb(243, 243, 243)",
                countrycolor="rgb(204, 204, 204)",
                bgcolor="rgba(0,0,0,0)",
                projection_scale=1,
                lonaxis_range=[-180, 180],
                lataxis_range=[-90, 90],
                scope="world",
            ),
            margin=dict(l=0, r=0, t=0, b=0),
        )
        last_year = df['Year'].max()
        fig.layout.sliders[0].active = len(fig.frames) - 1

        return fig

    # Callback to display country information and show the "See More" button
    @app.callback(
        [Output("country-info", "children"), Output("see-more-btn", "style")],
        [Input("map-graph", "clickData")]
    )
    def display_country_info(clickData):
        if clickData is None:
            return "", {"display": "none"}

        country = clickData['points'][0]['location']
        country_info = df_master[df_master['Country'] == country].iloc[0]

        info = html.Div([
            html.H4(country_info['Country']),
            html.P(f"Population: {country_info.get('Population', 'N/A')}"),
            html.P(f"GDP: {country_info.get('GDP', 'N/A')}"),
            # Add more fields as necessary
        ])

        return info, {"display": "block"}

    # Callback to redirect to the detailed page
    @app.callback(
        Output("url", "pathname"),
        [Input("see-more-btn", "n_clicks")],
        [State("map-graph", "clickData")]
    )
    def redirect_to_detailed_page(n_clicks, clickData):
        if n_clicks is None or clickData is None:
            return dash.no_update

        country = clickData['points'][0]['location']
        return f"/details/{country}"

    # Callback to toggle the line graph modal
    @app.callback(
        Output("dbc-modal-line", "is_open"),
        [Input("show-line-graph-btn", "n_clicks"), Input("modal-line-close", "n_clicks")],
        [State("dbc-modal-line", "is_open")],
    )
    def toggle_line_graph_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    # Callback to toggle the comparison modal
    @app.callback(
        Output("dbc-modal-comparison", "is_open"),
        [Input("show-country-comparison-btn", "n_clicks"), Input("modal-comparison-close", "n_clicks")],
        [State("dbc-modal-comparison", "is_open")],
    )
    def toggle_comparison_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    # Callbacks for the line graph modal
    @app.callback(
        [Output("line-graph-dropdown-countries", "options"),
        Output("line-graph-dropdown-dataset", "options")],
        [Input("user-type-store", "data")]
    )
    def update_line_graph_dropdowns(user_type):
        if df_master is None:
            return [], []

        countries = df_master['Country'].unique()
        country_options = [{"label": country, "value": country} for country in countries]

        datasets = df_master['Series'].unique()
        dataset_options = [{"label": dataset, "value": dataset} for dataset in datasets]

        return country_options, dataset_options
    
    @app.callback(
        Output("line-graph", "figure"),
        [Input("line-graph-dropdown-countries", "value"),
        Input("line-graph-dropdown-dataset", "value")]
    )
    def update_line_graph(countries, dataset):
        if not countries or not dataset:
            return {}

        df = df_master[(df_master['Country'].isin(countries)) & (df_master['Series'] == dataset)]

        if df.empty:
            return {}

        fig = px.line(df, x="Year", y="Value", color="Country", title=f"{dataset} over time")

        fig.update_layout(
            template="plotly_dark",
            title={
                'text': f"{dataset} over time",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Year",
            yaxis_title=dataset,
        )

        return fig

    @app.callback(
        [Output('comparison-dropdown-country1', 'options'),
        Output('comparison-dropdown-country2', 'options')],
        [Input('url', 'pathname')]
    )
    def set_country_options(pathname):
        country_options = [{'label': country, 'value': country} for country in df_master['Country'].unique()]
        return country_options, country_options


    # Callback to display country information for the first dropdown
    @app.callback(
        Output("country-info-1", "children"),
        [Input("comparison-dropdown-country1", "value")]
    )
    def display_country_info_1(selected_country):
        if not selected_country:
            return ""

        country_info = df_master[df_master['Country'] == selected_country].iloc[0]

        info = html.Div([
            html.H4(country_info['Country']),
            html.P(f"Population: {country_info.get('Population', 'N/A')}"),
            html.P(f"GDP: {country_info.get('GDP', 'N/A')}"),
            # Add more fields as necessary
        ])

        return info

    # Callback to display country information for the second dropdown
    @app.callback(
        Output("country-info-2", "children"),
        [Input("comparison-dropdown-country2", "value")]
    )
    def display_country_info_2(selected_country):
        if not selected_country:
            return ""

        country_info = df_master[df_master['Country'] == selected_country].iloc[0]

        info = html.Div([
            html.H4(country_info['Country']),
            html.P(f"Population: {country_info.get('Population', 'N/A')}"),
            html.P(f"GDP: {country_info.get('GDP', 'N/A')}"),
            # Add more fields as necessary
        ])

        return info

    # Callback to open the modal
    @app.callback(
        Output("country-details-modal", "is_open"),
        [Input("see-more-btn", "n_clicks"), Input("close-country-details", "n_clicks")],
        [State("country-details-modal", "is_open")]
    )
    def toggle_country_details_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @app.callback(
        Output('country-name', 'children'),
        [Input('url', 'pathname')]
    )
    def update_country_name(pathname):
        if pathname and pathname.startswith("/details/"):
            country = pathname.split("/details/")[1]
            return f"Details for {country}"
        return ""

    @app.callback(
        Output('modal-category-dropdown', 'options'),
        [Input('url', 'pathname')]
    )
    def update_modal_category_dropdown(pathname):
        if pathname and pathname.startswith("/details/"):
            categories = df_master['Series'].unique()
            return [{"label": category, "value": category} for category in categories]
        return []

    @app.callback(
        Output('gdp-graph', 'figure'),
        [Input('url', 'pathname')]
    )
    def update_gdp_graph(pathname):
        if pathname and pathname.startswith("/details/"):
            country = pathname.split("/details/")[1]
            df = df_master[df_master['Country'] == country]
            fig = px.line(df, x='Year', y='GDP', title=f'GDP of {country} over time')
            return fig
        return {}

    @app.callback(
        Output('population-graph', 'figure'),
        [Input('url', 'pathname')]
    )
    def update_population_graph(pathname):
        if pathname and pathname.startswith("/details/"):
            country = pathname.split("/details/")[1]
            df = df_master[df_master['Country'] == country]
            fig = px.line(df, x='Year', y='Population', title=f'Population of {country} over time')
            return fig
        return {}

    # Callback to update additional graphs based on selected category
    @app.callback(
        [Output('additional-graph-1', 'figure'), Output('additional-graph-2', 'figure')],
        [Input('modal-category-dropdown', 'value'), Input('url', 'pathname')]
    )
    def update_additional_graphs(selected_category, pathname):
        if pathname and pathname.startswith("/details/") and selected_category:
            country = pathname.split("/details/")[1]
            df = df_master[(df_master['Country'] == country) & (df_master['Series'] == selected_category)]
            
            if df.empty:
                return {}, {}

            fig1 = px.line(df, x='Year', y='Value', title=f'{selected_category} of {country} over time')
            fig2 = px.bar(df, x='Year', y='Value', title=f'{selected_category} of {country} over time')

            return fig1, fig2
        return {}, {}