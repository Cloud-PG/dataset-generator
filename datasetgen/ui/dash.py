
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ..generator import Generator
from . import functions
from .utils import get_functions

_EXTERNAL_STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
_PROGRESS = 100


def _create_layout(app, dest_folder: 'Path', function_UIs: list):

    app.layout = html.Div(children=[
        dcc.Interval(id='progress-interval', n_intervals=0, interval=1000),
        # For empty output callbacks
        html.Div(id='hidden-div', style={'display': "none"}),

        html.H2(children='Dataset Generator'),
        dbc.Alert(
            "",
            id="dataset-prepare-info-alert",
            color="info",
            is_open=False,
            duration=2000,
        ),
        dbc.Alert(
            "",
            id="dataset-generator-info-alert",
            color="info",
            is_open=False,
            duration=2000,
        ),
        html.Hr(),
        html.H3(children="Output folder"),
        dcc.Input(
            id='dest-folder',
            type="text",
            placeholder="destination folder name",
            value=dest_folder.name,
        ),
        html.Hr(),
        html.H3(children="Parameters"),
        html.Hr(),
        html.H5(id='num-day-val', children="Num. Days: "),
        dcc.Slider(
            id='num-days',
            min=1,
            max=365,
            step=1,
            value=1,
        ),
        html.Hr(),
        dbc.Button("Reload functions", id='reload-functions', color="primary"),
        dcc.Dropdown(
            id='functions',
            options=[
                {'label': 'None', 'value': 'None'},
            ] + get_functions(),
            value='None'
        ),
        html.H4(children="Function Parameters"),
        html.Div(id='function-parameters'),
        html.Hr(),
        dbc.Button("Prepare", id='prepare-dataset',
                   color="warning", block=True),
        dbc.Button("Create", id='create-dataset', color="success", block=True),
        html.Hr(),
        dbc.Progress(
            id='create-dataset-progress', value=_PROGRESS,
            style={
                'height': "6px",
                # 'display': "none",
            },
            className="mb-3"
        ),
    ])
    return app


def _prepare_callbacks(app, generator, dest_folder, function_UIs: list):

    for elm in function_UIs:
        elm.callbacks()

    @app.callback(
        [Output("functions", "options"), Output("functions", "value")],
        [Input("reload-functions", "n_clicks")],
    )
    def reload_functions(n_clicks):
        if n_clicks:
            return [
                {'label': 'None', 'value': 'None'},
            ] + get_functions(), "None"
        return [
            {'label': 'None', 'value': 'None'},
        ], "None"

    @app.callback(
        Output('function-parameters', 'children'),
        [Input('functions', 'value')],
    )
    def update_function_ui(value):
        for elm in function_UIs:
            if elm.__class__.__name__ == value:
                return elm.elements()
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
        Output('num-day-val', 'children'),
        [Input('num-days', 'value')])
    def update_output(value):
        generator.clean()
        generator.num_days = value
        return f"Num. Days: {value}"

    @app.callback(
        [Output('dataset-prepare-info-alert', 'is_open'),
         Output('dataset-prepare-info-alert', 'children')],
        [Input('prepare-dataset', 'n_clicks')]
    )
    def prepare_dataset(n_clicks):
        if n_clicks:
            global _PROGRESS
            _PROGRESS = 0
            for day in generator.prepare():
                _PROGRESS = day
            return True, "Done"
        else:
            return False, "No message from prepare dataset..."

    @app.callback(
        [Output('dataset-generator-info-alert', 'is_open'),
         Output('dataset-generator-info-alert', 'children')],
        [Input('create-dataset', 'n_clicks')]
    )
    def create_dataset(n_clicks):
        if n_clicks:
            global _PROGRESS
            _PROGRESS = 0
            for day in generator.save():
                _PROGRESS = day
            return True, "Done"
        else:
            return False, "No message from create dataset..."

    @app.callback(
        Output("create-dataset-progress", "value"),
        [Input("progress-interval", "n_intervals")],
    )
    def update_progress(n):
        global _PROGRESS
        return _PROGRESS

    return app


def start_app(debug: bool = True, dest_folder: 'Path' = Path(__file__).parent):
    generator = Generator(
        dest_folder=dest_folder,
    )

    app = dash.Dash(__name__, external_stylesheets=[
        _EXTERNAL_STYLESHEETS, dbc.themes.BOOTSTRAP
    ], suppress_callback_exceptions=True)

    function_UIs = []
    for elm in dir(functions):
        cur_elm = getattr(functions, elm)
        if type(cur_elm) == type and cur_elm is not functions.FunctionUI and issubclass(cur_elm, functions.FunctionUI):
            function_UIs.append(cur_elm(app))

    app = _create_layout(app, dest_folder, function_UIs)
    app = _prepare_callbacks(app, generator, dest_folder, function_UIs)

    app.run_server(debug=debug)
