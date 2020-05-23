
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from plotly.graph_objs import Layout

from ..generator import Generator
from . import functions
from .utils import get_functions

_EXTERNAL_STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
_PROGRESS = 100
_DEFAULT_SEED = 42


def _create_layout(app, dest_folder: 'Path', function_UIs: dict):
    """Prepares the UI layout.

    :param app: the current Dash application
    :type app: dash.Dash
    :param dest_folder: the destination folder for the datasets
    :type dest_folder: PurePath
    :param function_UIs: dataset generator UIs
    :type function_UIs: dict
    :return: the updated Dash application
    :rtype: dash.Dash
    """

    app.layout = html.Div(children=[
        dcc.Interval(id='progress-interval', n_intervals=0, interval=750),
        # For empty output callbacks
        html.Div(id='hidden-div', style={'display': "none"}),
        html.Div(children=[
            dbc.Toast(
                "",
                id="dataset-prepare-info-alert",
                header="Dataset prepare",
                icon="info",
                is_open=False,
                duration=2000,
                style={"position": "fixed", "top": 8,
                       "right": 8, "width": 480},
            ),
            dbc.Toast(
                "",
                id="dataset-inspect-info-alert",
                header="Dataset inpsect",
                icon="success",
                is_open=False,
                duration=2000,
                style={"position": "fixed", "top": 8,
                       "right": 8, "width": 480},
            ),
            dbc.Toast(
                "",
                id="dataset-generator-info-alert",
                header="Dataset save",
                icon="success",
                is_open=False,
                duration=2000,
                style={"position": "fixed", "top": 8,
                       "right": 8, "width": 480},
            ),
        ]),
        html.H2(children='Dataset Generator'),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                html.H3(children="Output folder"),
                width={'size': "auto", 'offset': 1}
            ),
            dbc.Col(dcc.Input(
                id='dest-folder',
                type="text",
                placeholder="destination folder name",
                value=dest_folder.name,
            ), width="auto"),
        ]),
        html.Hr(),
        html.H3(children="Generator Parameters"),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                html.H5(id='seed-val', children="Seed: "),
                width={'size': 3, 'offset': 1}
            ),
            dbc.Col(dcc.Input(
                id='seed',
                type="number",
                placeholder="random seed value",
                value=_DEFAULT_SEED,
            ), width="auto")
        ], style={'padding-bottom': "1em"}),
        dbc.Row([
            dbc.Col(
                html.H5(id='num-day-val', children="Num. Days: "),
                width={'size': 3, 'offset': 1}
            ),
            dbc.Col(dcc.Slider(
                id='num-days',
                min=1,
                max=365,
                step=1,
                value=7,
                marks={
                    0: {'label': '0'},
                    7: {'label': '7'},
                    30: {'label': '30'},
                    60: {'label': '60'},
                    90: {'label': '90'},
                    120: {'label': '120'},
                    365: {'label': '365'}
                },
            ), width=7)
        ]),
        dbc.Row([
            dbc.Col(html.H5(id='num-req-x-day-val', children="Num. Req. x Day: "),
                    width={'size': 3, 'offset': 1}
                    ),
            dbc.Col(dcc.Slider(
                id='num-req-x-day',
                min=1,
                max=100000,
                step=1,
                value=1000,
                marks={
                    1000: {'label': '1000'},
                    10000: {'label': '10000'},
                    20000: {'label': '20000'},
                    30000: {'label': '30000'},
                    50000: {'label': '50000'},
                    100000: {'label': '100000'},
                },
            ), width=7)
        ]),
        html.Hr(),
        html.H4(children="Function Selection"),
        dbc.Row([
            dbc.Col(
                dbc.Spinner(
                    dcc.Dropdown(
                        id='functions',
                        options=get_functions(),
                        value='None'
                    )),
                width={'size': 7, 'offset': 1}
            ),
            dbc.Col(
                dbc.Button("Reload functions",
                           id='reload-functions', color="primary",
                           ),
            ),
        ]),
        html.Hr(),
        html.H4(children="Function Parameters"),
        html.Div(id='function-parameters'),
        html.Hr(),
        dbc.Button("Prepare", id='prepare-dataset',
                   color="warning", block=True),
        dbc.Button("Inpsect", id='inspect-dataset',
                   color="info", block=True),
        dbc.Button("Save", id='save-dataset',
                   color="success", block=True),
        html.Hr(),
        dbc.Progress(
            id='create-dataset-progress', value=_PROGRESS,
            className="mb-3"
        ),
        html.Hr(),
        dbc.Spinner(html.Div(id='inspect-output')),
    ], style={'padding': "1em"})
    return app


def _prepare_callbacks(app, generator, dest_folder, function_UIs: dict):
    """Function to prepare the UI callbacks.

    In this function are called also all the personalized UI callbacks present
    in the function generator UIs.

    :param app: the current Dash application
    :type app: dash.Dash
    :param generator: the generator object
    :type generator: Generator
    :param dest_folder: the destination folder for the datasets
    :type dest_folder: PurePath
    :param function_UIs: the dataset generator UIs
    :type function_UIs: dict
    :return: the Dash app with the updated callbacks
    :rtype: dash.Dash
    """

    for elm in function_UIs.values():
        elm.callbacks()

    @app.callback(
        [Output("functions", "options"), Output("functions", "value")],
        [Input("reload-functions", "n_clicks")],
    )
    def reload_functions(n_clicks):
        return get_functions(), ""

    @app.callback(
        Output('function-parameters', 'children'),
        [Input('functions', 'value')],
    )
    def update_function_ui(value):
        if value in function_UIs:
            return function_UIs[value].elements()
        else:
            return "Function has no parameters"

    @app.callback(
        Output("hidden-div", "children"),
        [Input("dest-folder", "value")],
    )
    def change_dest_folder(new_dest_folder):
        generator.dest_folder = Path(
            dest_folder).parent.joinpath(new_dest_folder)
        return ""

    @app.callback(
        Output("seed-val", "children"),
        [Input("seed", "value")],
    )
    def change_seed(value):
        generator.seed = value
        return f"Seed: {value}"

    @app.callback(
        Output('num-day-val', 'children'),
        [Input('num-days', 'value')])
    def update_num_days(value):
        generator.clean()
        generator.num_days = value
        return f"Num. Days: {value}"

    @app.callback(
        Output('num-req-x-day-val', 'children'),
        [Input('num-req-x-day', 'value')])
    def update_num_req_x_day(value):
        generator.num_req_x_day = value
        return f"Num. Req. x Day: {value}"

    @app.callback(
        [Output('dataset-prepare-info-alert', 'is_open'),
         Output('dataset-prepare-info-alert', 'icon'),
         Output('dataset-prepare-info-alert', 'children')],
        [Input('prepare-dataset', 'n_clicks')],
        [State("functions", "value")]
    )
    def prepare_dataset(n_clicks, selected_function):
        if n_clicks:
            global _PROGRESS
            _PROGRESS = 0
            try:
                fun_kwargs = function_UIs[selected_function].to_dict()
            except KeyError:
                return True, "danger", "Impossible to get function parameters..."
            if selected_function and fun_kwargs:
                generator.clean()
                for day in generator.prepare(
                    selected_function, fun_kwargs
                ):
                    _PROGRESS = day
                return True, "success", "Done"
            else:
                return True, "warning", "Nothing to do..."
        else:
            return False, "primary", "No message from prepare dataset..."

    @app.callback(
        [Output('inspect-output', 'children'),
         Output('dataset-inspect-info-alert', 'is_open'),
         Output('dataset-inspect-info-alert', 'children')],
        [Input('inspect-dataset', 'n_clicks')]
    )
    def inspect_dataset(n_clicks):
        if n_clicks:
            (df, file_frequencies, file_sizes,
             num_files, num_req) = generator.df_stats

            layout = Layout(
                paper_bgcolor='rgb(255,255,255)',
                plot_bgcolor='rgb(255,255,255)',
                yaxis={'gridcolor': 'black'},
                xaxis={'gridcolor': 'black'},
            )

            daily_stats = go.Figure(data=[
                go.Bar(name='Files', x=num_files.day,
                       y=num_files.numFiles),
                go.Bar(name='Requests', x=num_req.day,
                       y=num_req.numReq),
            ], layout=layout)
            daily_stats.update_layout(title="# files and requests x day")

            file_freq_fig = px.bar(
                file_frequencies, x="Filename",
                y="# requests", title="File requests"
            )
            file_size_fig = px.bar(
                file_sizes, x="Filename",
                y="Size", title="File sizes"
            )
            size_hist_fig = px.histogram(
                df, x="Size", title="Size distribution"
            )
            size_scatter_fit = px.scatter(
                df, y='Size', size='Size',
                title="Sizes during days"
            )
            filename_scatter_fig = px.scatter(
                df, y='Filename', color="Filename",
                title="Files during days"
            )

            file_freq_fig.update_layout(layout)
            file_size_fig.update_layout(layout)
            size_hist_fig.update_layout(layout)
            size_scatter_fit.update_layout(layout)
            filename_scatter_fig.update_layout(layout)

            return [
                dcc.Graph(figure=daily_stats),
                dcc.Graph(figure=file_freq_fig),
                dcc.Graph(figure=file_size_fig),
                dcc.Graph(figure=size_hist_fig),
                dcc.Graph(figure=size_scatter_fit),
                dcc.Graph(figure=filename_scatter_fig),
            ], True, "Inspection donw. Result plots are ready!"
        return "", False, ""

    @app.callback(
        [Output('dataset-generator-info-alert', 'is_open'),
         Output('dataset-generator-info-alert', 'children')],
        [Input('save-dataset', 'n_clicks')]
    )
    def save_dataset(n_clicks):
        if n_clicks:
            global _PROGRESS
            _PROGRESS = 0
            for day in generator.save():
                _PROGRESS = day
            return True, "Done! Dataset saved in the output folder..."
        else:
            return False, "No message from save dataset..."

    @app.callback(
        Output("create-dataset-progress", "value"),
        [Input("progress-interval", "n_intervals")],
    )
    def update_progress(n):
        global _PROGRESS
        return _PROGRESS

    return app


def start_app(debug: bool = True, dest_folder: 'Path' = Path(__file__).parent):
    """Start the generator UI app.

    :param debug: if start in debug mode or not, defaults to True
    :type debug: bool, optional
    :param dest_folder: the destination folder for the dataset generator, defaults to Path(__file__).parent
    :type dest_folder: PurePath, optional
    """
    generator = Generator(
        dest_folder=dest_folder,
    )

    app = dash.Dash(__name__, external_stylesheets=[
        _EXTERNAL_STYLESHEETS, dbc.themes.BOOTSTRAP
    ], suppress_callback_exceptions=True)

    function_UIs = {}
    for elm in dir(functions):
        cur_elm = getattr(functions, elm)
        if type(cur_elm) == type and \
            cur_elm is not functions.FunctionUI and \
                issubclass(cur_elm, functions.FunctionUI):
            function_UIs[elm] = cur_elm(app)

    app = _create_layout(app, dest_folder, function_UIs)
    app = _prepare_callbacks(app, generator, dest_folder, function_UIs)

    app.run_server(debug=debug)
