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


class base_function(FunctionUI):

    def __init__(self, app: 'dash.dash.Dash'):
        super().__init__(app)

    def callbacks(self):
        @self._app.callback(
            Output('num-file-val', 'children'),
            [Input('num-files', 'value')])
        def update_output(value):
            return f"Num. Files: {value}"

    def elements(self):
        return html.Div(id="base_function", children=[
            html.H5(id='num-file-val', children="Num. Files: "),
            dcc.Slider(
                id='num-files',
                min=1,
                max=100000,
                step=1,
                value=1,
            ),
        ])
