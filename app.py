from MyDashCytoscape import MyDashCytoscape

app = MyDashCytoscape("*** matching ***")
server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
