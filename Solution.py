from dash import html


class Solution:
	name = ""
	execution_time = 0.0
	cards = []

	def __init__(self, name, execution_time, cards):
		self.name = name
		self.execution_time = execution_time
		self.cards = cards

	# TODO return html div for each solution
	def render(self):
		return html.Div(
			html.P("Solution " + self.name + "div", style={"font-weight": "bold"})
		)
