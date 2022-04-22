import pandas as pd

from dash import Dash, dcc, html
from histogram_generator import generate_match_rate_histogram
from json_parser import parse_json_to_solutions
import plotly.graph_objects as go


solutions = parse_json_to_solutions("annotator.json")

histogram = generate_match_rate_histogram(solutions)


app = Dash(__name__)

app.layout = html.Div([
    html.H1("Benchmark between solutions:", style={"font-weight": "bold"}),
    dcc.Graph(
        id="histogram",
        figure=histogram
    ),
    html.Div([solution.render() for solution in solutions])

])

if __name__ == '__main__':
    app.run_server(debug=True)