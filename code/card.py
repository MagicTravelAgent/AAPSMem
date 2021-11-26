import logging


class Card:
    def __init__(self, size, back_image, front_image):
        self.size = size
        self.back_image = back_image
        self.front_image = front_image
        self.hidden = True

    def get_size(self):
        """
        Returns the size of the card in pixels. The height and width are the same.
        :return:
        """
        return self.size

    def hide(self):
        """
        Hides the card and returns the back image
        :return:
        """
        self.hidden = True
        return self.back_image

    def show(self):
        """
        Reveals the card and returns the front image
        :return:
        """
        self.hidden = False
        return self.front_image

    def flip(self):
        """
        flips the card and returns the corresponding image
        :return:
        """
        self.hidden = not self.hidden
        return self.get_image()

    def get_image(self):
        """
        returns the currently facing image
        :return:
        """
        if self.hidden:
            logging.debug(f'The card is face down')
            return self.back_image
        else:
            logging.debug(f'the card is face up')
            return self.front_image
