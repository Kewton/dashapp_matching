import pandas as pd
import networkx as nx
import dash_cytoscape as cyto
import copy

from MyUtil import com_replace

def addno(_df):
  df_nodedef_0 = _df[_df["属性"]==0].sort_values('名前')
  serial_num_0= pd.RangeIndex(start=1, stop=len(df_nodedef_0.index) + 1, step=1)
  df_nodedef_0["no"]=serial_num_0
  
  df_nodedef_1 = _df[_df["属性"]==1].sort_values('名前')
  serial_num_1 = pd.RangeIndex(start=1, stop=len(df_nodedef_1.index) + 1, step=1)
  df_nodedef_1["no"]=serial_num_1

  return df_nodedef_0, df_nodedef_1

def getval(_edge_weight):
  if "weight" in _edge_weight.keys():
    return _edge_weight["weight"]
  else:
    return 0

def getGraph(df_nodedef, df_edge0to1, df_edge1to0):
  G = nx.Graph()

  df0, df1 = addno(df_nodedef)
  df = pd.concat([df0, df1])

  for index, row in df.iterrows():
    node = (int(row["属性"]), int(row["no"]))
    G.add_node(node)

  for index, row in pd.concat([df_edge0to1, df_edge1to0]).iterrows():
    x_0=df0[df0["名前"]==row["0属性"]]["属性"].iloc[0]
    y_0=df0[df0["名前"]==row["0属性"]]["no"].iloc[0]
    x_1=df1[df1["名前"]==row["1属性"]]["属性"].iloc[0]
    y_1=df1[df1["名前"]==row["1属性"]]["no"].iloc[0]
    node_0=(x_0, y_0)
    node_1=(x_1, y_1)
    G.add_edge(node_0, node_1)
    G[node_0][node_1]["weight"] = getval(G[node_0][node_1]) + row["重み"]
  
  return G, df

def CreateGraphAndMax_weight_matching(_df_nodedef, _df_edge0to1, _df_edge1to0):
    G, df = getGraph(_df_nodedef, _df_edge0to1, _df_edge1to0)
    
    # 重み最大マッチング
    mw = nx.max_weight_matching(G)

    # 扱いやすいように重み最大マッチングの結果のノード名を置換してリストに格納する
    mw_list = []
    for a in mw:
      fromtolist = []
      for b in a:
        fromtolist.append((com_replace(b)))
      mw_list.append(fromtolist)
    
    return G, mw_list, df

def drawCytoscape(_df_nodedef, _df_edge0to1, _df_edge1to0):
  # Step 1. NetworkXのGraphオブジェクトと重み最大マッチング結果リストを取得
  G, mw_list, df = CreateGraphAndMax_weight_matching(_df_nodedef, _df_edge0to1, _df_edge1to0)

  # Step 2. NetworkXのGraphオブジェクト ⇨ Cytoscape用のデータ形式
  cy_data = nx.readwrite.json_graph.cytoscape_data(G)

  # Step 3. Cytoscapeのデータ形式 ⇨ Dash Cytoscapeのデータ形式
  dash_cy_elements = cy_data["elements"]["nodes"] + cy_data["elements"]["edges"]

  aftele = copy.deepcopy(dash_cy_elements)
  for i in range(0, len(dash_cy_elements)):
    ele_list = dash_cy_elements[i]
    for ele_dict in ele_list:
      for dt in ele_list[ele_dict]:
        if "id" in ele_list[ele_dict].keys():
          # nodeの場合
          tp = eval(ele_list[ele_dict]["id"])
          _name = df[(df["属性"]==tp[0]) & (df["no"]==tp[1])]["名前"].iloc[0]
          aftele[i][ele_dict]["id"] = com_replace(ele_list[ele_dict]["id"])
          aftele[i][ele_dict]["value"] = _name
          aftele[i][ele_dict]["name"] = _name+"さん"
          if "(1" in aftele[i][ele_dict]["id"]:
            # 突っ込みの場合
            aftele[i][ele_dict]["color"] = "red"
          else:
            # ボケの場合
            aftele[i][ele_dict]["color"] = "navy"
        else:
          # edgeの場合
          # idを付与する
          aftele[i][ele_dict]["id"] = com_replace(ele_list[ele_dict]["source"]) + "2" + com_replace(ele_list[ele_dict]["target"])
          aftele[i][ele_dict]["source"] = com_replace(ele_list[ele_dict]["source"])
          aftele[i][ele_dict]["target"] = com_replace(ele_list[ele_dict]["target"])
          # 線の太さの差異を強調する
          aftele[i][ele_dict]["weight_width"] = float(aftele[i][ele_dict]["weight"])*1.5
          # デフォルトカラー
          aftele[i][ele_dict]["color"] = "silver"
          for a in mw_list:
            # 重み最大マッチング結果に含まれる場合強調カラー
            if aftele[i][ele_dict]["source"] in set(a) and aftele[i][ele_dict]["target"] in set(a):
              aftele[i][ele_dict]["color"] = "black"
  
  elements = aftele
  # 設定値を確認したいとき
  #for ele in elements:
  #  print(ele)

  cyto_compo = cyto.Cytoscape(
      id='cytoscape',
      elements=elements,
      layout={
          'name': 'circle','padding': 10
          # 'name': 'grid',"rows":2,"colmuns":5 # グリッドは枝の重みのラベルが重なりやすい
      },
      stylesheet=[{
          'selector': 'node',
          'style': {
              'width': '60px',
              'height': '60px',
              'content': 'data(name)',
              'pie-size': '80%',
              'background-color': 'data(color)',
          }
      }, {
          'selector': 'edge',
          'style': {
              'label': 'data(weight)',
              'width': 'data(weight_width)',
              'curve-style': 'bezier',
              #'target-arrow-shape': 'triangle', # 今回は無向グラフ
              'line-color': 'data(color)',
              'opacity': 0.5
          }
      }, {
          'selector': ':selected',
          'style': {
              'background-color': 'black',
              'line-color': 'black',
              'target-arrow-color': 'black',
              'source-arrow-color': 'black',
              'opacity': 1
          }
      }, {
          'selector': '.faded',
          'style': {
              'opacity': 0.25,
              'text-opacity': 0
          }
      }],
      style={
          'width': '80%',
          'height': '80%',
          'position': 'absolute',
          #'position': 'relative',
          'left': 200,
          'top': 200
      }
  )
  return cyto_compo
