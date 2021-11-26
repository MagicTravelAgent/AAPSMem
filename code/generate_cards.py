import cv2
import numpy as np
import logging
import sys
import random
from card import Card


class CardGenerator:
    def __init__(self):
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        self.difficulty = 0
        self.card_size = 100
        self.n_cards = 0
        self.cards = []
        self.back_image = self.generate_back_image()
        pass

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        logging.debug(f'The difficulty has been set to {difficulty}')

    def set_size(self, card_size):
        self.card_size = card_size
        logging.debug(f'the size of the cards has been set to {card_size}x{card_size} pixels')

    def generate_back_image(self):
        img = None
        return img

    def generate_front_image(self, background):
        shapes = 5
        shapes += self.difficulty*2
        img = np.array([np.full((self.card_size, self.card_size), col) for col in background])
        return img

    def generate_cards(self, n_cards):
        background = [random.random()*255 for i in range(3)]
        if n_cards % 2:
            print(f'ERROR: You need to specify an even number of cards! {n_cards} is not an even number, silly!', file=sys.stderr)
            return []
        self.n_cards = n_cards

        for i in range(int(n_cards/2)):
            new_card = Card(
                size=self.card_size,
                back_image=self.back_image,
                front_image=self.generate_front_image(background)
            )
            self.cards.append(new_card)
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
cg.flip_card(2)

