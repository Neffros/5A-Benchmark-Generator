import plotly.graph_objects as go
from dash import Dash, dcc, html
import pandas as pd
import json

from Card import Card
from Solution import Solution

cardType = {
    0: "clubs",
    1: "spades",
    2: "diamonds",
    3: "hearts"
}

cardValue = {
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "jack",
    12: "queen",
    13: "king",
    14: "ace"
}


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

hist = go.Figure(
    data=[go.Bar(y=[2, 1, 3])],
    layout_title_text="A Figure Displayed with fig.show()"
)

listofBars = []
solutionNames = ["solution1", "solution crazy", "another one"]
cardNames = ["Seven of hearts", "Queen of hearts", "Ace of Spades"]
tmpValues = [[4,5,6], [2,3,6], [1,0,9]]
index=0
for solutionName in solutionNames:
    listofBars.append(go.Bar(name=solutionName, x=cardNames, y=tmpValues[index]))
    index+=1
histogram = go.Figure(data=listofBars)

histogram.update_layout(
    title="Score matches",
    xaxis_title="cards",
    yaxis_title="score",
    legend_title="Legend Title",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)

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