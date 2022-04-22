import base64
from dash import Dash, dcc, html
from histogram_generator import generate_match_rate_histogram
from json_parser import parse_json_to_solutions


solutions = parse_json_to_solutions("easy.json")

histogram = generate_match_rate_histogram(solutions)


app = Dash(__name__)

app.layout = html.Div([
    html.H1("Benchmark between solutions:", style={"font-weight": "bold"}),
    html.H3("If the match rate is 0, the card was not detected at all by the solution.\n"
            "If the match rate is beetween 0 and 1, a card was detected but it wasn't the correct one. the score will "
            "be closer to 1 the more similar that card is to the expected one\n "
            "If the match rate is 1, the card was correctly detected."),
    dcc.Graph(
        id="histogram",
        figure=histogram
    ),
    html.Div([solution.render() for solution in solutions])

])

if __name__ == '__main__':
    app.run_server(debug=True)