from dataclasses import dataclass

import plotly.express as px
import numpy as np
import pandas as pd


@dataclass
class Sector:
    x: int
    y: int
    content: str


def main():

    df = pd.read_csv("assets/map_info.csv")

    XMAX = 16
    YMAX = 16

    galaxy = np.zeros((XMAX, YMAX))

    for _, sector in df.iterrows():
        galaxy[sector.x, sector.y] = sector.color

    fig = px.imshow(galaxy, origin="lower")
    fig.update_traces(hovertemplate="x: %{x} <br> y: %{y} <br> color: %{color}")
    fig.show()


if __name__ == "__main__":
    main()
