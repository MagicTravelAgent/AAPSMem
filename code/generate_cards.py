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
        self.back_image = None
        self.generate_back_image()

        self.shapes = [
            self.rectangle,
            self.line,
            self.circle
        ]
        pass

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        logging.debug(f'The difficulty has been set to {difficulty}')

    def set_size(self, card_size):
        self.card_size = card_size
        self.generate_back_image()
        logging.debug(f'the size of the cards has been set to {card_size}x{card_size} pixels')

    def generate_back_image(self):
        background = [random.random() * 50 for i in range(3)]
        img = np.full((self.card_size, self.card_size, 3), 0, dtype=np.uint8)
        for i in range(3):
            img[:, :, i] = background[i]
        self.back_image = img

    def triangle(self, img):
        pass

    def rectangle(self, img):
        rect_size1 = random.randint(35, int(self.card_size/2))
        rect_size2 = random.randint(35, int(self.card_size/2))
        fill_col = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pt1 = (random.randint(-30, self.card_size), random.randint(-30,self.card_size))
        pt2 = (pt1[0]+rect_size1, pt1[1]+rect_size2)
        cv2.rectangle(img, pt1, pt2, fill_col, random.randint(5, 20))

    def circle(self, img):
        center = (random.randint(-30, self.card_size+30), random.randint(-30, self.card_size+30))
        thickness = random.randint(5,15)
        radius = random.randint(30, int(self.card_size/2))
        fill_col = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        cv2.circle(img, center, radius, fill_col, thickness)

    def line(self, img):
        if random.randint(0,1):
            pt1 = (random.randint(-30, self.card_size + 30), -30)
            pt2 = (random.randint(-30, self.card_size + 30), self.card_size + 30)
        else:
            pt1 = (-30, random.randint(-30, self.card_size + 30))
            pt2 = (self.card_size + 30, random.randint(-30, self.card_size + 30))
        fill_col = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        thickness = random.randint(5,15)
        cv2.line(img, pt1, pt2, fill_col, thickness)

    def add_shape(self, img):
        self.shapes[random.randint(0, len(self.shapes)-1)](img)

    def generate_front_image(self, background):
        shapes = 3
        shapes += self.difficulty
        img = np.full((self.card_size, self.card_size, 3), 0, dtype=np.uint8)
        for i in range(3):
            d_col = 200*(random.random()-0.5)/max(self.difficulty, 1)
            img[:, :, i] = min(255, max(0, background[i] + d_col))
        for i in range(shapes):
            self.add_shape(img)

        self.show_img(img)
        return img

    def generate_cards(self, n_cards):
        background = np.array([random.random()*60 for i in range(3)])
        self.n_cards = n_cards

        for i in range(int(n_cards)):
            new_card = Card(
                size=self.card_size,
                back_image=self.back_image,
                front_image=self.generate_front_image(background)
            )
            self.cards.append(new_card)
        logging.info(f'{len(self.cards)} cards have been generated')

    def flip_card(self, index):
        if index >= self.n_cards or index < 0:
            logging.exception(f'ERROR: invalid index. {index} is outside the range 0-{self.n_cards-1}')
            return None
        logging.debug(f'Card {index} has been flipped')
        return self.cards[index].flip()

    def show_img(self, img):
        cv2.imshow('test', img)
        cv2.waitKey()
        cv2.destroyAllWindows()


def debug():
    cg = CardGenerator()
    cg.set_difficulty(3)
    cg.set_size(400)
    cg.generate_cards(4)
    flipped = cg.flip_card(2)
    cg.show_img(flipped)
    flipped = cg.flip_card(2)
    cg.show_img(flipped)

debug()
