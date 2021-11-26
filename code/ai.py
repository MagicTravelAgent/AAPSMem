import numpy as np
import random

class AI:
    def __init__(self, board_width, forget_prob):
        self.known_cards = -1*np.ones((board_width*board_width/2,2,2))
        self.forget_prob = forget_prob
        self.board = np.zeros((board_width, board_width))

    # Return the two cards the AI will turn around
    def make_move(self):
        # If two positions are known for a set, turn around those two cards
        known_set = self.check_known_set()
        if known_set is not -1:
            return self.known_cards[known_set,0], self.known_cards[known_set,1]
        
        # Pick a random unknown card. If you know the other card of this set, turn around that card
        first_card = self.random_move()
        if self.known_cards[first_card,1,0] is not -1:
            return self.known_cards[first_card,0], self.known_cards[first_card,1]
        
        # Pick a second random unknown card
        second_card = self.random_move()
        return self.known_cards[first_card,0], self.known_cards[second_card, 0 if self.known_cards[second_card,1] is -1 else 1]
   
    # Store a position together with the observed card
    def update(self, card, position):
        if self.known_cards[card,0,0] is -1:
            self.known_cards[card,0] = position
        elif self.known_cards[card,0] is not position:
            self.known_cards[card,1] = position
        # Indicate that the card at that position has been seen
        self.board[position] = 1

    # Return if both position of a pair of cards is known
    def check_known_set(self):
                # VOOR ONS: later ook voor de eerste de hoogste prob pakken
        for card_index in len(self.known_cards):
            if self.known_cards[card_index,1,0] is not -1:
                return card_index
        return -1

    # Pick random move from all unknown locations in the board
    def random_move(self):
                # VOOR ONS: random getal (prob voor of we geziene kaarten nog eens om gaan draaien)
        # Random choice of all unknown locations
        move = random.choice(zip(*np.where(self.board is 0)))
        position = [move[0], move[1]]
        # Observe card at the chosen position
        card_value = BOARD.get_card(position)
        # Update knowlegde
        self.update(card_value, position)
        return card_value