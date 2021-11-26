import cv2
import numpy as np
import logging
import sys


class CardGenerator:
    def __init__(self):
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        self.difficulty = 0
        self.card_size = 100
        self.n_cards = 0
        self.cards = []
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
        self.n_cards = n_cards

        for i in range(int(n_cards/2)):
            new_card = cv2.full()
        logging.info(f'{n_cards} cards have been generated')
        return self.cards

    def flip_card(self, index):
        if index >= self.n_cards or index < 0:
            print(f'ERROR: invalid index. {index} is outside the range 0-{self.n_cards-1}')
            return None
        logging.debug(f'Card {index} has been flipped')
        return self.cards[index].flip


cg = CardGenerator()
cg.set_difficulty(2)
cg.set_size(200)
cg.generate_cards(4)

