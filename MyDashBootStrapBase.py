from dash import Dash
import dash_bootstrap_components as dbc

class MyDashBootStrapBase(Dash):
  def __init__(self, _title):
    super().__init__(__name__, external_stylesheets=self.__external_stylesheets())
    if _title is not None:
      self.title = _title
    self.__setlayout()
    #self.run_server(debug=True, port=_port)
    self.run_server(debug=True)
  
  def __setlayout(self):
      self.layout = self.buildbaselayout()
      self.registcalback(self)

  def buildbaselayout(self):
      return
  
  def registcalback(self, app):
      return
  
  def __external_stylesheets(self):
    return [dbc.themes.BOOTSTRAP]