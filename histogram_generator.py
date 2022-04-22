import plotly.graph_objects as go


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

	histogram = go.Figure(data=listofBars, layout_yaxis_range=[0, 1])

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
