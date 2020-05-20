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
        self._num_files = 100
        self._min_file_size = 100
        self._max_file_size = 24000
        self._size_function_generator = "gen_random_sizes"

    def __repr__(self):
        return "Random Generator"

    def to_dict(self):
        return {
            'num_files': self._num_files,
            'min_file_size': self._min_file_size,
            'max_file_size': self._max_file_size,
            'size_generator_function': self._size_function_generator,
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

        @self._app.callback(
            Output(f'{self.name_id}-size-function-val', 'children'),
            [Input(f'{self.name_id}-size-function', 'value')],
        )
        def update_function_ui(value):
            self._size_function_generator = value
            if value == "gen_random_sizes":
                return "File size function generator: [0]"
            elif value == "gen_in_range_random_sizes":
                return "File size function generator: [1]"

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
            dbc.Row([
                dbc.Col(
                    html.H5(id=f'{self.name_id}-size-function-val',
                            children="File size function generator: [1]"),
                    width={'size': 3, 'offset': 1}),
                dbc.Col(dcc.Dropdown(
                        id=f'{self.name_id}-size-function',
                        options=[
                            {'label': "(0) gen random sizes",
                                'value': "gen_random_sizes"},
                            {'label': "(1) gen in range random sizes",
                                'value': "gen_in_range_random_sizes"},
                        ],
                        value='gen_in_range_random_sizes'
                        ), width=6),
            ]),
        ])


class HighFrequencyDataset(FunctionUI):

    def __init__(self, app: 'dash.dash.Dash'):
        super().__init__(app)
        self._num_files: int = 100
        self._min_file_size: int = 100
        self._max_file_size: int = 24000
        self._lambda_less_req_files: float = 1.
        self._lambda_more_req_files: float = 10.
        self._perc_more_req_files: float = 10.
        self._perc_files_x_day: float = 25.
        self._size_function_generator = "gen_random_sizes"

    def __repr__(self):
        return "High Frequency Dataset"

    def to_dict(self):
        return {
            'num_files': self._num_files,
            'min_file_size': self._min_file_size,
            'max_file_size': self._max_file_size,
            'lambda_less_req_files': self._lambda_less_req_files,
            'lambda_more_req_files': self._lambda_more_req_files,
            'perc_more_req_files': self._perc_more_req_files,
            'perc_files_x_day': self._perc_files_x_day,
            'size_generator_function': self._size_function_generator,
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
            Output(f'{self.name_id}-size-function-val', 'children'),
            [Input(f'{self.name_id}-size-function', 'value')],
        )
        def update_function_ui(value):
            self._size_function_generator = value
            if value == "gen_random_sizes":
                return "File size function generator: [0]"
            elif value == "gen_in_range_random_sizes":
                return "File size function generator: [1]"

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

        @self._app.callback(
            Output(f'{self.name_id}-perc-files-x-day-val', 'children'),
            [Input(f'{self.name_id}-perc-files-x-day', 'value')],
        )
        def change_percentage_files_x_day(value):
            self._perc_files_x_day = value
            return f"Files x day: {value}%"

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
                    html.Div(
                        "NOTE: This function do NOT take into account the above num. of req. x day parameter",
                        style={'color': "rgb(251, 0, 0)",
                               'padding-bottom': "2em"},
                    ),
                    width={'size': 9, 'offset': 3}),
            ]),
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
            ], style={'padding-bottom': "1em"}),
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
            ], style={'padding-bottom': "1em"}),
            dbc.Row([
                dbc.Col(
                    html.H5(id=f'{self.name_id}-size-function-val',
                            children="File size function generator: [1]"),
                    width={'size': 3, 'offset': 1}),
                dbc.Col(dcc.Dropdown(
                        id=f'{self.name_id}-size-function',
                        options=[
                            {'label': "(0) gen random sizes",
                                'value': "gen_random_sizes"},
                            {'label': "(1) gen in range random sizes",
                                'value': "gen_in_range_random_sizes"},
                        ],
                        value='gen_in_range_random_sizes'
                        ), width=6),
            ], style={'padding-bottom': "2em"},),
            dbc.Row([
                dbc.Col(
                    html.H5(children="Poisson distribution parameters"),
                    width={'size': "auto", 'offset': 1}
                )
            ]),
            dbc.Row([
                dbc.Col(
                    html.Hr(),
                    width={'size': "8", 'offset': 1}
                )
            ]),
            dbc.Row([
                dbc.Col(
                    html.H5(children="Lambda less requested files"),
                    width={'size': "auto", 'offset': 2}
                ),
                dbc.Col(dcc.Input(
                    id=f'{self.name_id}-lambda-less-req-files',
                    type="number",
                    placeholder="Lambda less requested files",
                    value=self._lambda_less_req_files,
                ), width={'size': "auto", 'offset': 1}),
            ], style={'padding-bottom': "1em"}),
            dbc.Row([
                dbc.Col(
                    html.H5(children="Lambda more requested files"),
                    width={'size': "auto", 'offset': 2}
                ),
                dbc.Col(dcc.Input(
                    id=f'{self.name_id}-lambda-more-req-files',
                    type="number",
                    placeholder="Lambda more requested files",
                    value=self._lambda_more_req_files,
                ), width={'size': "auto", 'offset': 1}),
            ], style={'padding-bottom': "2em"}),
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
            ], style={'padding-bottom': "1em"}),
            dbc.Row([
                dbc.Col(
                    html.H5(id=f'{self.name_id}-perc-files-x-day-val',
                            children="Files x day: %"),
                    width={'size': 3, 'offset': 1}),
                dbc.Col(dcc.Slider(
                    id=f'{self.name_id}-perc-files-x-day',
                    min=1,
                    max=100,
                    step=1,
                    value=self._perc_files_x_day,
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
            ], style={'padding-bottom': "1em"}),
        ])


class RecencyFocusedDataset(FunctionUI):

    def __init__(self, app: 'dash.dash.Dash'):
        super().__init__(app)
        self._num_files: int = 100
        self._min_file_size: int = 100
        self._max_file_size: int = 24000
        self._perc_noise: float = 10.
        self._perc_files_x_day: float = 25.
        self._size_function_generator = "gen_random_sizes"

    def __repr__(self):
        return "Recency Focused Dataset"

    def to_dict(self):
        return {
            'num_files': self._num_files,
            'min_file_size': self._min_file_size,
            'max_file_size': self._max_file_size,
            'perc_noise': self._perc_noise,
            'perc_files_x_day': self._perc_files_x_day,
            'size_generator_function': self._size_function_generator,
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
            Output(f'{self.name_id}-size-function-val', 'children'),
            [Input(f'{self.name_id}-size-function', 'value')],
        )
        def update_function_ui(value):
            self._size_function_generator = value
            if value == "gen_random_sizes":
                return "File size function generator: [0]"
            elif value == "gen_in_range_random_sizes":
                return "File size function generator: [1]"

        @self._app.callback(
            Output(f'{self.name_id}-perc-noise-val', 'children'),
            [Input(f'{self.name_id}-perc-noise', 'value')],
        )
        def change_percentage_more_req_files(value):
            self._perc_noise = value
            return f"Noise: {value}%"

        @self._app.callback(
            Output(f'{self.name_id}-perc-files-x-day-val', 'children'),
            [Input(f'{self.name_id}-perc-files-x-day', 'value')],
        )
        def change_percentage_files_x_day(value):
            self._perc_files_x_day = value
            return f"Files x day: {value}%"

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
            ], style={'padding-bottom': "1em"}),
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
            ], style={'padding-bottom': "1em"}),
            dbc.Row([
                dbc.Col(
                    html.H5(id=f'{self.name_id}-size-function-val',
                            children="File size function generator: [1]"),
                    width={'size': 3, 'offset': 1}),
                dbc.Col(dcc.Dropdown(
                        id=f'{self.name_id}-size-function',
                        options=[
                            {'label': "(0) gen random sizes",
                                'value': "gen_random_sizes"},
                            {'label': "(1) gen in range random sizes",
                                'value': "gen_in_range_random_sizes"},
                        ],
                        value='gen_in_range_random_sizes'
                        ), width=6),
            ], style={'padding-bottom': "2em"},),
            dbc.Row([
                dbc.Col(
                    html.H5(id=f'{self.name_id}-perc-noise-val',
                            children="Noise: %"),
                    width={'size': 3, 'offset': 1}),
                dbc.Col(dcc.Slider(
                    id=f'{self.name_id}-perc-noise',
                    min=1,
                    max=100,
                    step=1,
                    value=self._perc_noise,
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
            ], style={'padding-bottom': "1em"}),
            dbc.Row([
                dbc.Col(
                    html.H5(id=f'{self.name_id}-perc-files-x-day-val',
                            children="Files x day: %"),
                    width={'size': 3, 'offset': 1}),
                dbc.Col(dcc.Slider(
                    id=f'{self.name_id}-perc-files-x-day',
                    min=1,
                    max=100,
                    step=1,
                    value=self._perc_files_x_day,
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
            ], style={'padding-bottom': "1em"}),
        ])
