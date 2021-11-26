import logging


class Card:
    def __init__(self, size, back_image, front_image):
        self.size = size
        self.back_image = back_image
        self.front_image = front_image
        self.hidden = True

    def flip(self):
        self.hidden = not self.hidden
        return self.get_image()

    def get_image(self):
        if self.hidden:
            logging.debug(f'The card is face down')
            return self.back_image
        else:
            logging.debug(f'the card is face up')
            return self.front_image
