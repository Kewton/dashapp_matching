import pandas as pd

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from MyDashBootStrapBase import MyDashBootStrapBase
from GetGraph import drawCytoscape
from MyUtil import parse_content

class MyDashCytoscape(MyDashBootStrapBase):
  _df_nodedef = pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
  _df_edge0to1 = pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
  _df_edge1to0 = pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
  
  def buildbaselayout(self):
    upload_style = {
        "width": "50%",
        "height": "120px",
        "lineHeight": "60px",
        "borderWidth": "1px",
        "borderStyle": "dashed",
        "borderRadius": "5px",
        "textAlign": "center",
        "margin": "10px",
        "margin": "3% auto",
    }
    _up1 = dcc.Upload(
                id="nodedef",
                children=html.Div(["ノード属性", html.A("のcsvファイル")]),
                style=upload_style,
            )
    _up2 = dcc.Upload(
                id="edge0to1",
                children=html.Div(["エッジリスト_0to1", html.A("のcsvファイル")]),
                style=upload_style,
            )
    _up3 = dcc.Upload(
                id="edge1to0",
                children=html.Div(["エッジリスト_1to0", html.A("のcsvファイル")]),
                style=upload_style,
            )

    row = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(_up1),
                    dbc.Col(_up2),
                    dbc.Col(_up3),
                ],
                align="start",
            ),
            dbc.Button("Matching!", id="my_button", className="me-2", n_clicks=0),
            html.Div(id="my_div1", children=[]),
            html.Div(id="my_div2", children=[]),
            html.Div(id="my_div3", children=[]),
            html.Div(id="my_div4", children=[]),
            html.Div(id="my_div", children=[]),
        ]
    )
    return row
    
  def registcalback(self, app):
    @app.callback(
        [
            Output("my_div1", "children"),
        ],
        [Input("nodedef", "contents")],
        [State("nodedef", "filename")],
        prevent_initial_call=True,
    )
    def upload_nodedef(contents, filename):
        print("upload_nodedef")
        self._df_nodedef = parse_content(contents, filename)
        print(self._df_nodedef.info())
        return [f"ノード属性ファイル：{filename}"]

    @app.callback(
        [
            Output("my_div2", "children"),
        ],
        [Input("edge0to1", "contents")],
        [State("edge0to1", "filename")],
        prevent_initial_call=True,
    )
    def upload_edge0to1(contents, filename):
        self._df_edge0to1 = parse_content(contents, filename)
        return [f"エッジリスト_0to1ファイル：{filename}"]

    @app.callback(
        [
            Output("my_div3", "children"),
        ],
        [Input("edge1to0", "contents")],
        [State("edge1to0", "filename"),],
        prevent_initial_call=True,
    )
    def upload_edge1to0(contents, filename):
        self._df_edge1to0 = parse_content(contents, filename)
        return [f"エッジリスト_1to0ファイル：{filename}"]

    @app.callback(
        [
            Output("my_div4", "children"),
            Output("my_div", "children"),
        ],
        [Input("my_button", "n_clicks")],
        prevent_initial_call=True,
    )
    def drawmatching(n_clicks):
        print("drawmatching")
        try:
            new_layout=drawCytoscape(self._df_nodedef, self._df_edge0to1, self._df_edge1to0)
            return "success!", [new_layout]
        except Exception as e:
            print(e)
            return "File format is incorrect", []
        
