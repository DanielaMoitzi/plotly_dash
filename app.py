import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_ag_grid as dag

import dash_mantine_components as dmc

app = Dash(__name__)


@app.callback(
    Output("price-chart", "figure"),
    Output("volume-chart", "figure"),
    Input("region-select", "value"),
    Input("type-select", "value"),
    Input("date-range-picker", "value"),
)
def update_charts(region, avocado_type, dates):
    print("Updating charts")
    print(dates)
    filtered_data = data.query(
        f"region == '{region}' and type == '{avocado_type}' and Date >= '{dates[0]}' and Date <= '{dates[1]}'"
    )
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["AveragePrice"],
                "type": "lines",
                "hovertemplate": ("$%{y:.2f}<extra></extra>"),
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocado",
                "x": "center",
            },
            "colorway": ["#FFA15A"],
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "font": {
                "color": "#fff",
            },
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Total Volume"],
                "type": "bar",
                "hovertemplate": ("%{y}<extra></extra>"),
            },
        ],
        "layout": {
            "title": "Avocados Sold",
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "font": {
                "color": "#fff",
            },
        },
    }

    return price_chart_figure, volume_chart_figure


data = (
    pd.read_csv("avocado.csv")
    # .query("type == 'conventional' and region == 'Albany'")
    .assign(
        Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d")
    ).sort_values(by="Date")
)

regions = data["region"].sort_values().unique()
avocado_types = data["type"].sort_values().unique()


app.layout = html.Div(
    style={
        "height": "100vh",
        "margin": "0",
        "display": "flex",
        "background": "#383b42",
    },
    children=[
        dmc.Group(
            align="start",
            # grow=True,
            style={
                "display": "flex",
                "position": "relative",
                "height": "100vh",
            },
            children=[
                dmc.Stack(
                    style={
                        "flex": "0 0 20%",
                        "margin-left": "0.5rem",
                        "align-items": "center",
                    },
                    children=[
                        html.H1(
                            children="Avocado Prices Dashboard",
                            style={"textAlign": "center"},
                        ),
                        html.P(
                            children="Analyze the behavior of avocado prices",
                            style={"textAlign": "center"},
                        ),
                        dmc.Select(
                            label="Select a region",
                            placeholder="Select a region",
                            id="region-select",
                            value="Albany",
                            clearable=False,
                            data=[
                                {"label": region, "value": region} for region in regions
                            ],
                            style={"width": "100%"},
                        ),
                        dmc.Select(
                            label="Select a type",
                            placeholder="Select a type",
                            id="type-select",
                            value="organic",
                            clearable=False,
                            searchable=False,
                            data=[
                                {
                                    "label": avocado_type.title(),
                                    "value": avocado_type,
                                }
                                for avocado_type in avocado_types
                            ],
                            style={"width": "100%"},
                        ),
                        dmc.DateRangePicker(
                            id="date-range-picker",
                            label="Select a date range",
                            minDate=data["Date"].min().date(),
                            maxDate=data["Date"].max().date(),
                            style={"color": "#fff", "width": "-webkit-fill-available"},
                            value=[
                                data["Date"].min().date(),
                                data["Date"].max().date(),
                            ],
                        ),
                        dmc.Text(id="selected-value"),
                    ],
                ),
                dmc.Stack(
                    style={
                        "flex": "1 1 auto",
                        "margin": "0.5rem",
                    },
                    children=[
                        dcc.Graph(
                            id="price-chart",
                            style={"width": "100%"},
                            # figure={
                            #     "data": [
                            #         {
                            #             "x": data["Date"],
                            #             "y": data["AveragePrice"],
                            #             "type": "lines",
                            #             "hovertemplate": ("$%{y:.2f}<extra></extra>"),
                            #         },
                            #     ],
                            #     "layout": {
                            #         "title": {
                            #             "text": "Average Price of Avocado",
                            #             "x": "center",
                            #         },
                            #         "colorway": ["#FFA15A"],
                            #         "paper_bgcolor": "rgba(0,0,0,0)",
                            #         "plot_bgcolor": "rgba(0,0,0,0)",
                            #         "font": {
                            #             "color": "#fff",
                            #         },
                            #     },
                            # },
                            config={"displayModeBar": False},
                        ),
                        dcc.Graph(
                            id="volume-chart",
                            # figure={
                            #     "data": [
                            #         {
                            #             "x": data["Date"],
                            #             "y": data["Total Volume"],
                            #             "type": "bar",
                            #             "hovertemplate": ("%{y}<extra></extra>"),
                            #         },
                            #     ],
                            #     "layout": {
                            #         "title": "Avocados Sold",
                            #         "paper_bgcolor": "rgba(0,0,0,0)",
                            #         "plot_bgcolor": "rgba(0,0,0,0)",
                            #         "font": {
                            #             "color": "#fff",
                            #         },
                            #     },
                            # },
                        ),
                    ],
                ),
            ],
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
