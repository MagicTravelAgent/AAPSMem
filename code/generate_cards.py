import cv2
import numpy as np
import logging
import sys


class CardGenerator:
    def __init__(self):
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        self.difficulty = 0
        self.card_size = 100
        pass

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        logging.debug(f'The difficulty has been set to {difficulty}')

    def set_size(self, card_size):
        self.card_size = card_size
        logging.debug(f'the size of the cards has been set to {card_size}x{card_size} pixels')

    def generate_cards(self, n_cards):
        if n_cards % 2:
            print(f'ERROR: You need to specify an even number of cards! {n_cards} is not an even number, silly!', file=sys.stderr)
            return []
        cards = []
        for i in range(int(n_cards/2)):
            pass
        logging.info(f'{n_cards} cards have been generated')
        return cards



cg = CardGenerator()
cg.set_difficulty(2)
cg.set_size(200)
cg.generate_cards(4)

