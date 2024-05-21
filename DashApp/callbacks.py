from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import numpy as np
from utils import parse_contents
import pandas as pd


def register_callbacks(app):
    @app.callback(Output("user-type-store", "data"), [Input("url", "href")])
    def store_user_type(href):
        if href is None:
            return 0  # Valor predeterminado si no hay información en la URL
        user_type = href.split("user_type=")[1] if "user_type=" in href else 0
        return int(user_type)


    @app.callback(
        Output("map-graph", "figure"),
        [
            Input("upload-data", "contents"),
            Input("series-selector", "value"),
            Input("colorscale-selector", "value"),
            Input("visualization-selector", "value"),
            Input("country-selector", "value"),
            Input("user-type-store", "data"),
        ],
        [State("upload-data", "filename")],
    )
    def update_map(
        contents, selected_series, colorscale, visualization_type, selected_countries, user_type, filename
    ):
        if user_type == 0 or contents is None or selected_series is None:
            # Mostrar mapa básico para usuarios no logueados
            df = pd.read_csv(
                "/data/countries.csv"
            )
            if(df.isnull):
                print("Hola")
            
            print(df.head())
            # Archivo CSV con información básica de países
            fig = px.choropleth(
                df,
                locations="country",
                locationmode="country names",
                hover_name="country",
                projection="natural earth",
                title="Mapa interactivo de países",
            )
            fig.update_layout(coloraxis_showscale=False)  # Ocultar escala de colores
            return fig

        if contents is None or selected_series is None:
            return {}

        df = parse_contents(contents, filename)
        if df is None:
            return {}

        df = df[df['Series'] == selected_series]

        if 'Country' not in df.columns:
            return {}

        # Convertir la columna 'Value' a numérico, forzando errores a NaN
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

        # Filtrar valores no positivos ya que el logaritmo no está definido para ellos
        df = df[df['Value'] > 0]

        if df.empty:
            return {}  # Devuelve un gráfico vacío si no hay datos válidos

        # Aplicar transformación logarítmica a los datos
        df['Log_Value'] = np.log10(df['Value'])

        # Normalizar los valores logarítmicos para la escala de color
        min_val = df['Log_Value'].min()
        df['Normalized_Log'] = df['Log_Value'] - min_val

        if visualization_type == "chart":
            # Filtrar los datos por los países seleccionados
            df = df[df['Country'].isin(selected_countries)]

            fig = px.line(
                df,
                x="Year",
                y='Normalized_Log',
                color="Country",
                title=f"{selected_series} a través de los años",
                markers=True,
                hover_data={'Normalized_Log': False, 'Value': True}  # Mostrar solo valores originales
            )

            return fig

        elif visualization_type == "map":
            # Generar valores de ticks para la escala
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
                color_continuous_scale=colorscale,
                projection="natural earth",
                title=f"Mapa interactivo de {selected_series} por país a través de los años",
                range_color=(0, max_val),
                hover_data={'Normalized_Log': False, 'Value': True}  # Mostrar solo valores originales
            )

            # Set the animation frame to the last year
            last_year = df['Year'].max()
            fig.layout.sliders[0].active = len(fig.frames) - 1
            fig.layout.sliders[0].currentvalue = {"prefix": "Year: ", "font": {"size": 20}, "offset": 10}
            fig.layout.sliders[0].steps[-1]['label'] = str(last_year)

            return fig

        return {}

    # Callback para mostrar y ocultar el modal
    @app.callback(
        Output("dbc-modal-line", "is_open"),
        [Input("open-linegraph-modal", "n_clicks"), Input("modal-line-close", "n_clicks")],
        [State("dbc-modal-line", "is_open")]
    )
    def toggle_linegraph_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @app.callback(
        Output("dbc-modal-comparison", "is_open"),
        [Input("open-comparison-modal", "n_clicks"), Input("modal-comparison-close", "n_clicks")],
        [State("dbc-modal-comparison", "is_open")],
    )
    def toggle_comparison_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @app.callback(
        [Output("comparison-dropdown-country1", "options"), Output("comparison-dropdown-country2", "options")],
        [Input("upload-data", "contents")],
        [State("upload-data", "filename")]
    )
    def update_country_dropdowns(contents, filename):
        if contents is None:
            print("No contents uploaded")
            return [], []

        df = parse_contents(contents, filename)
        if df is None:
            print("DataFrame is None after parsing contents")
            return [], []

        if 'Country' not in df.columns:
            print("Country column not found in DataFrame")
            return [], []

        countries = df['Country'].unique()
        options = [{"label": country, "value": country} for country in countries]
        print(f"Generated options: {options}")
        return options, options


    @app.callback(
        Output("comparison-table", "children"),
        [Input("comparison-dropdown-country1", "value"), Input("comparison-dropdown-country2", "value")],
        [State("upload-data", "contents"), State("upload-data", "filename")]
    )
    def update_comparison_table(country1, country2, contents, filename):
        if not country1 or not country2 or contents is None:
            return []

        df = parse_contents(contents, filename)
        if df is None:
            return []

        # Filter data for the selected countries
        df1 = df[df['Country'] == country1]
        df2 = df[df['Country'] == country2]

        # Create a comparison table
        comparison_data = {
            "Metric": df1.columns,
            country1: df1.iloc[0].values,
            country2: df2.iloc[0].values
        }
        comparison_df = pd.DataFrame(comparison_data)

        # Generate table rows
        table_header = [html.Thead(html.Tr([html.Th(col) for col in comparison_df.columns]))]
        table_body = [html.Tbody([
            html.Tr([html.Td(comparison_df.iloc[i][col]) for col in comparison_df.columns])
            for i in range(len(comparison_df))
        ])]

        return table_header + table_body

