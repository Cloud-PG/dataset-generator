import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output
import dash


class FunctionUI(object):

    def __init__(self, app: 'dash.dash.Dash'):
        assert isinstance(
            app, dash.dash.Dash
        ), "Function UI needs main app reference..."
        self._app = app

    def elements(self):
        raise NotImplementedError

    def callbacks(self):
        raise NotImplementedError

    def to_dict(self):
        raise NotImplementedError

    @property
    def name(self):
        return repr(self)


class RandomGenerator(FunctionUI):

    def __init__(self, app: 'dash.dash.Dash'):
        super().__init__(app)
        self._num_files = 1000
        self._min_file_size = 1000
        self._max_file_size = 4000

    def __repr__(self):
        return "Random Generator"

    def to_dict(self):
        return {
            'num_files': self._num_files,
            'min_file_size': self._min_file_size,
            'max_file_size': self._max_file_size,
        }

    def callbacks(self):
        @self._app.callback(
            Output('num-file-val', 'children'),
            [Input('num-files', 'value')])
        def update_output(value):
            self._num_files = value
            return f"Num. Files: {value}"

        @self._app.callback(
            Output("file-size-val", "children"),
            [Input("file-size", "value")],
        )
        def change_dest_folder(value):
            self._min_file_size, self._max_file_size = value
            return f"File Size (MB): {self._min_file_size}-{self._max_file_size}"

    def elements(self):
        return html.Div([
            dbc.Row([
                dbc.Col(
                    html.H5(id='num-file-val', children="Num. Files: "),
                    width={'size': 3, 'offset': 1}),
                dbc.Col(dcc.Slider(
                    id='num-files',
                    min=1,
                    max=100000,
                    step=1,
                    value=self._num_files,
                    marks={
                        1000: {'label': '1000', 'style': {'font-size': "8px"}},
                        10000: {'label': '10000', 'style': {'font-size': "8px"}},
                        20000: {'label': '20000', 'style': {'font-size': "8px"}},
                        30000: {'label': '30000', 'style': {'font-size': "8px"}},
                        50000: {'label': '50000', 'style': {'font-size': "8px"}},
                        100000: {'label': '100000', 'style': {'font-size': "8px"}},
                    },
                ), width=6)
            ]),
            dbc.Row([
                dbc.Col(
                    html.H5(id='file-size-val', children="File Size (MB): "),
                    width={'size': 3, 'offset': 1}),
                dbc.Col(dcc.RangeSlider(
                    id='file-size',
                    min=1,
                    max=24000,
                    step=1,
                    value=[self._min_file_size, self._max_file_size],
                    marks={
                        1000: {'label': '1000', 'style': {'font-size': "8px"}},
                        2000: {'label': '2000', 'style': {'font-size': "8px"}},
                        4000: {'label': '4000', 'style': {'font-size': "8px"}},
                        8000: {'label': '8000', 'style': {'font-size': "8px"}},
                        16000: {'label': '16000', 'style': {'font-size': "8px"}},
                        24000: {'label': '24000', 'style': {'font-size': "8px"}},
                    },
                    allowCross=False,
                ), width=6)
            ]),
        ])
