import dash_html_components as html
import pandas as pd
import base64
import io
import re

def com_replace(_s):
  '''
  dashではidに","（カンマ）は使えないため置換する。
  ※カンマをそのまま置換するとjson形式が崩れるため注意が必要
  ※(1, 1)->1
  
  '''
  pattern = r'(\d{1,4}?), (\d{1,4}?)'
  result = re.sub(pattern, r'\1_\2', str(_s))
  return result 

def parse_content(contents, filename):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div(["ファイルの読み込みでエラーが発生しました"])

    return df