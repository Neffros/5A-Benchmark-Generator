import json

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
            false_positive_cards = []

            for benchmark in solution["benchmarks"]:
                for existingCards in benchmark["comparison"]["existingCards"]:
                    value = cardValue.get(existingCards["value"])
                    card_type = cardType.get(existingCards["type"])
                    match_rate = existingCards["matchRate"]
                    characteristics = []
                    [characteristics.append(characteristic) for characteristic in existingCards["characteristics"]]
                    cards.append(Card(value, card_type, match_rate, characteristics))

                for falsePositiveCards in benchmark["comparison"]["falsePositiveCards"]:
                    value = cardValue.get(falsePositiveCards["value"])
                    card_type = cardType.get(falsePositiveCards["type"])
                    match_rate = falsePositiveCards["matchRate"]
                    false_positive_cards.append(Card(value, card_type, match_rate))
                execution_time = benchmark["performance"]["executionTime"]

            solutions.append(Solution(solution_name, execution_time, cards, false_positive_cards))
    return solutions

