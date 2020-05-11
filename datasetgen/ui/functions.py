import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


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

    @property
    def name_id(self):
        return "-".join(str(self).lower().split())


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
            Output(f'{self.name_id}-num-file-val', 'children'),
            [Input(f'{self.name_id}-num-files', 'value')])
        def change_num_files(value):
            self._num_files = value
            return f"Num. Files: {value}"

        @self._app.callback(
            Output(f'{self.name_id}-file-size-val', 'children'),
            [Input(f'{self.name_id}-file-size', 'value')],
        )
        def change_size(value):
            self._min_file_size, self._max_file_size = value
            return f"File Size (MB): {self._min_file_size}-{self._max_file_size}"

    def elements(self):
        return html.Div([
            dbc.Row([
                dbc.Col(
                    html.H5(id=f'{self.name_id}-num-file-val',
                            children="Num. Files: "),
                    width={'size': 3, 'offset': 1}),
                dbc.Col(dcc.Slider(
                    id=f'{self.name_id}-num-files',
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
                    html.H5(id=f'{self.name_id}-file-size-val',
                            children="File Size (MB): "),
                    width={'size': 3, 'offset': 1}),
                dbc.Col(dcc.RangeSlider(
                    id=f'{self.name_id}-file-size',
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


class PoissonGenerator(FunctionUI):

    def __init__(self, app: 'dash.dash.Dash'):
        super().__init__(app)
        self._num_files: int = 1000
        self._min_file_size: int = 1000
        self._max_file_size: int = 4000
        self._lambda_less_req_files: float = 1.
        self._lambda_more_req_files: float = 2.
        self._perc_more_req_files: float = 10.

    def __repr__(self):
        return "Poisson Generator"

    def to_dict(self):
        return {
            'num_files': self._num_files,
            'min_file_size': self._min_file_size,
            'max_file_size': self._max_file_size,
            'lambda_less_req_files': self._lambda_less_req_files,
            'lambda_more_req_files': self._lambda_more_req_files,
            'perc_more_req_files': self._perc_more_req_files,
        }

    def callbacks(self):
        pass

        @self._app.callback(
            Output(f'{self.name_id}-num-file-val', 'children'),
            [Input(f'{self.name_id}-num-files', 'value')])
        def change_num_files(value):
            self._num_files = value
            return f"Num. Files: {value}"

        @self._app.callback(
            Output(f'{self.name_id}-file-size-val', 'children'),
            [Input(f'{self.name_id}-file-size', 'value')],
        )
        def change_size(value):
            self._min_file_size, self._max_file_size = value
            return f"File Size (MB): {self._min_file_size}-{self._max_file_size}"

        @self._app.callback(
            Output(f'{self.name_id}-hidden-div-lambda-less', 'children'),
            [Input(f'{self.name_id}-lambda-less-req-files', 'value')],
        )
        def change_lambda_less_req_files(value):
            self._lambda_less_req_files = value

        @self._app.callback(
            Output(f'{self.name_id}-hidden-div-lambda-more', 'children'),
            [Input(f'{self.name_id}-lambda-more-req-files', 'value')],
        )
        def change_lambda_more_req_files(value):
            self._lambda_more_req_files = value

        @self._app.callback(
            Output(f'{self.name_id}-perc-more-req-files-val', 'children'),
            [Input(f'{self.name_id}-perc-more-req-files', 'value')],
        )
        def change_percentage_more_req_files(value):
            self._perc_more_req_files = value
            return f"More requested files: {value}%"

    def elements(self):
        return html.Div([
            html.Div(
                # For empty output callbacks
                id=f'{self.name_id}-hidden-div-lambda-less',
                style={'display': "none"}),
            html.Div(
                # For empty output callbacks
                id=f'{self.name_id}-hidden-div-lambda-more',
                style={'display': "none"}),
            dbc.Row([
                dbc.Col(
                    html.H5(id=f'{self.name_id}-num-file-val',
                            children="Num. Files: "),
                    width={'size': 3, 'offset': 1}),
                dbc.Col(dcc.Slider(
                    id=f'{self.name_id}-num-files',
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
                    html.H5(id=f'{self.name_id}-file-size-val',
                            children="File Size (MB): "),
                    width={'size': 3, 'offset': 1}),
                dbc.Col(dcc.RangeSlider(
                    id=f'{self.name_id}-file-size',
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
            dbc.Row([
                dbc.Col(
                    html.H5(children="Lambda less requested files"),
                    width={'size': "auto", 'offset': 1}
                ),
                dbc.Col(dcc.Input(
                    id=f'{self.name_id}-lambda-less-req-files',
                    type="number",
                    placeholder="Lambda less requested files",
                    value=self._lambda_less_req_files,
                ), width="auto"),
            ]),
            dbc.Row([
                dbc.Col(
                    html.H5(children="Lambda more requested files"),
                    width={'size': "auto", 'offset': 1}
                ),
                dbc.Col(dcc.Input(
                    id=f'{self.name_id}-lambda-more-req-files',
                    type="number",
                    placeholder="Lambda more requested files",
                    value=self._lambda_more_req_files,
                ), width="auto"),
            ]),
            dbc.Row([
                dbc.Col(
                    html.H5(id=f'{self.name_id}-perc-more-req-files-val',
                            children="More requested files: %"),
                    width={'size': 3, 'offset': 1}),
                dbc.Col(dcc.Slider(
                    id=f'{self.name_id}-perc-more-req-files',
                    min=1,
                    max=100,
                    step=1,
                    value=self._perc_more_req_files,
                    marks={
                        10: {'label': '10%', 'style': {'font-size': "8px"}},
                        20: {'label': '20%', 'style': {'font-size': "8px"}},
                        30: {'label': '30%', 'style': {'font-size': "8px"}},
                        40: {'label': '40%', 'style': {'font-size': "8px"}},
                        50: {'label': '50%', 'style': {'font-size': "8px"}},
                        60: {'label': '60%', 'style': {'font-size': "8px"}},
                        70: {'label': '70%', 'style': {'font-size': "8px"}},
                        80: {'label': '80%', 'style': {'font-size': "8px"}},
                        90: {'label': '90%', 'style': {'font-size': "8px"}},
                        100: {'label': '100%', 'style': {'font-size': "8px"}},
                    },
                ), width=6)
            ]),
        ])
