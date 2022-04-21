import plotly.graph_objects as go
import pandas as pd
import json

from dash import Dash, dcc, html
from card import Card
from solution import Solution
from constants import cardType, cardValue


def parse_json_to_solutions(path):
    solutions = []
    with open(path) as json_file:
        parser = json.load(json_file)
        for solution in parser["solutions"]:
            solution_name = solution["name"]
            execution_time = 0.0
            cards = []
            for benchmark in solution["benchmarks"]:
                for existingCards in benchmark["comparison"]["existingCards"]:
                    value = cardValue.get(existingCards["value"])
                    card_type = cardType.get(existingCards["type"])
                    match_rate = existingCards["matchRate"]
                    cards.append(Card(value, card_type, match_rate))
                execution_time = benchmark["performance"]["executionTime"]
            solutions.append(Solution(solution_name, execution_time, cards))
    return solutions


def generate_match_rate_histogram(solutions):
    solution_names = []
    card_names = []
    solution_values = []
    for solution in solutions:
        solution_names.append(solution.name)

    for card in solutions[0].cards:
        card_names.append(card.value + " of " + card.card_type)

    for index in range(len(card_names)):
        values_of_card = []
        for solution in solutions:
            values_of_card.append(solution.cards[index].match_rate)
        solution_values.append(values_of_card)

    listofBars = []

    for index in range(len(solutions)):
        listofBars.append(go.Bar(name=solution_names[index], x=card_names, y=solution_values[index]))

    histogram = go.Figure(data=listofBars)

    histogram.update_layout(
        title="Score matches",
        xaxis_title="Cards To Find",
        yaxis_title="Score",
        legend_title="Solutions",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )

    return histogram


solutions = parse_json_to_solutions("annotator.json")

df = pd.DataFrame(dict(
    x=[1, 2, 3, 4, 5],
    y=[1, 2, 10, 6, 2]
))

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df.x,
    y=df.y,
    name='<b>No</b> Gaps',  # Style name/legend entry with html tags
    connectgaps=True  # override default to connect the gaps
))\

fig.update_layout(
    title="Memory usage over time",
    xaxis_title="Time (seconds)",
    yaxis_title="Memory usage (mb)",
    legend_title="Legend Title",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)

histogram = generate_match_rate_histogram(solutions)


app = Dash(__name__)

app.layout = html.Div([
    html.P("Memory usage overtime", style={"font-weight": "bold"}),
    html.Div([solution.render() for solution in solutions]),
    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    html.P("after the graph"),
    dcc.Graph(
        id="histogram",
        figure=histogram
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)