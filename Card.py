class Card:
	value = ""
	card_type = ""
	match_rate = 0.0

	def __init__(self, value, card_type, match_rate):
		self.value = value
		self.card_type = card_type
		self.match_rate = match_rate
