from dash import Dash, Input, Output, dcc, html
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import math
import pandas as pd
import numpy as np

last_x = 0
last_y = 0


def get_galaxy():
    df = pd.read_csv("assets/map_info.csv")
    df["highlight"] = 0

    XMAX = 16
    YMAX = 16

    galaxy = np.zeros((XMAX, YMAX))

    for _, sector in df.iterrows():
        galaxy[sector.x, sector.y] = sector.color

    return galaxy


def get_map():
    fig = px.imshow(get_galaxy(), origin="lower")
    fig.update_traces(hovertemplate="x: %{x} <br> y: %{y} <br> color: %{color}")
    fig.update_layout(
        {
            "template": "plotly_dark",
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            "width": 800,
            "height": 600,
        }
    )
    return fig


fig = get_map()

# initiate app, use a dbc theme
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SLATE],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4("Click to set destination"),
                        dcc.Graph(id="graph", figure=fig),
                    ],
                    width={"size": 10},
                ),
                dbc.Col(
                    [html.H4("Route"), html.Pre(id="click")],
                    width={"size": 2},
                ),
            ]
        )
    ],
    fluid=True,
)


def euclidean_distance(src: tuple[int, int], dst: tuple[int, int]) -> float:
    return math.sqrt((dst[0] - src[0]) ** 2 + (dst[1] - src[1]) ** 2)


def path_finding(src: tuple[int, int], dst: tuple[int, int]):
    direction_x = 0
    direction_y = 0

    directions = []

    pos_x = src[0]
    pos_y = src[1]

    while (pos_x != dst[0]) or (pos_y != dst[1]):
        direction_x = np.sign(dst[0] - pos_x)
        direction_y = np.sign(dst[1] - pos_y)

        pos_x += direction_x
        pos_y += direction_y

        directions.append((int(direction_x), int(direction_y)))

    return directions


# serverside callback (python)
@app.callback(Output("click", "children"), Input("graph", "clickData"))
def get_click(clickData):
    global last_x, last_y
    if not clickData:
        raise PreventUpdate
    else:
        points = clickData.get("points")[0]
        x = points.get("x")
        y = points.get("y")

        distance = euclidean_distance((last_x, last_y), (x, y))
        directions = path_finding((last_x, last_y), (x, y))

        return_string = f"({last_x, last_y}) -> {x,y}\n{distance}\n"
        for direction in directions:
            return_string = f"{return_string}\n   {direction}"

        last_x = x
        last_y = y

    return return_string


if __name__ == "__main__":
    app.run(debug=True, port=8052)
