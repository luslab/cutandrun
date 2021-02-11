#!/usr/bin/env python
# coding: utf-8

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask

from lib.figures import Figures

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

# Init data
figures = Figures(None, "data/meta_table.csv")
figs, data = figures.generate_dash_plots()

cats = ["hello", "world"]

app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash 2020"),
        html.Div(children="""Dash: A web application framework for Python."""),
        html.Div([
                html.H4("Alignment Summary Metrics"),
                html.H5("Select Metric"),
                dcc.Dropdown(
                    id='cat-dropdown',
                    options=[{'label': i, 'value': i} for i in cats],
                    value=cats[0]
                ),
                dcc.Graph(
                    id='box-plot',
                )
            ])
        # dcc.Graph(
        #     id='example-graph',
        #     figure=figs["alignment_summary_reads_target"]
        # ),
    ]
)

# =========
# Dynamic plotting
# =========
# @app.callback(
#     dash.dependencies.Output('box-plot', 'figure'),
#     dash.dependencies.Input('cat-dropdown', 'value')
# )
# def 

if __name__ == "__main__":
    import os

    debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True
    app.run_server(host="0.0.0.0", port=8050, debug=debug)