from dash import html, dcc
import plotly.graph_objects as go
from constants import cardCharacteristics
from helper import remove_key


class Solution:
	name = ""
	execution_time = 0.0
	cards = []
	false_positive_cards = []

	def __init__(self, name, execution_time, cards, false_positive_cards):
		self.name = name
		self.execution_time = execution_time
		self.cards = cards
		self.false_positive_cards = false_positive_cards

	def generate_characteristic_match_rate_histogram(self):
		characteristics = {}
		characteristics_avg_rate = {}
		for characteristic in cardCharacteristics:
			characteristics[characteristic] = []
			characteristics_avg_rate[characteristic] = 0
		for card in self.cards:
			for characteristic in card.characteristics:
				characteristics[characteristic].append(card.match_rate)

		for key in list(characteristics.keys()):
			if len(characteristics[key]) == 0:
				del characteristics[key]
				del characteristics_avg_rate[key]
				continue
			characteristics_avg_rate[key] = sum(characteristics[key]) / len(characteristics[key])

		array_rates = []
		characteristic_names = []
		for key in characteristics_avg_rate:
			array_rates.append(characteristics_avg_rate[key])
			characteristic_names.append(cardCharacteristics.get(key))

		histogram = go.Figure(
			data=[go.Bar(x=characteristic_names, y=array_rates)], layout_yaxis_range=[0, 1],
			layout_title_text="Average matchRate per characteristics"
		)
		histogram.update_layout(
			title="Score matches",
			xaxis_title="Characteristics",
			yaxis_title="Average Score",
			font=dict(
				family="Courier New, monospace",
				size=18,
				color="RebeccaPurple"
			)
		)

		return histogram

	def render(self):
		return html.Div([
			html.H1(self.name + ":", style={"font-weight": "bold"}),
			html.H3(self.name + " detected " + str(len(self.false_positive_cards)) + " false positive cards."),
			html.H3("it took " + str(self.execution_time) + " seconds to run"),
			dcc.Graph(
				id=self.name + " characteristics",
				figure=self.generate_characteristic_match_rate_histogram()
			)
		])
