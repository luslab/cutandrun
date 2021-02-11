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
figures = Figures(None, "data/meta_table.csv", "data/frags.csv")


meta, fragments = figures.return_data()

# data = Figures.load_data("data/meta_table.csv")

# figs, data = figures.generate_dash_plots()


app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash 2020"),
        html.Div(children="""Dash: A web application framework for Python."""),
        html.Div([
                html.H4("Alignment Summary Metrics"),
                html.H5("Select Metric"),
                dcc.Dropdown(
                    id='cat-dropdown',
                    options=[{'label': i, 'value': i} for i in meta.columns],
                    value=meta.columns[0]
                ),
                dcc.Graph(
                    id='box-plot',
                )
            ]),
        html.Div([
                html.H4("Fragment Length Distribution"),
                # html.H5("Select Metric"),
                # dcc.Dropdown(
                #     id='cat-dropdown',
                #     options=[{'label': i, 'value': i} for i in meta.columns],
                #     value=meta.columns[0]
                # ),
                dcc.Graph(
                    id='violin-plot',
                    figure=figures.generate_frag_plots()
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
@app.callback(
    dash.dependencies.Output('box-plot', 'figure'),
    dash.dependencies.Input('cat-dropdown', 'value')
)
def update_boxplot(cat):
    fig = figures.generate_box_plot(x_axis="group", y_axis=cat)
    return fig

# @app.callback(
#     dash.dependencies.Output('violin-plot', 'figure'),
#     # dash.dependencies.Input('cat-dropdown', 'value')
# )
# def update_boxplot(cat):
#     fig = figures.generate_box_plot(x_axis="group", y_axis=cat)
#     return fig

    


if __name__ == "__main__":
    import os

    debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True
    app.run_server(host="0.0.0.0", port=8050, debug=debug)