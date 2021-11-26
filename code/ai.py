import numpy as np
import random
#ALS KAARTEN ERUIT GAAN
class AI:
    def __init__(self, board_size, forget_prob=1):
        self.known_cards = -1*np.ones((int(board_size*board_size/2),2,2), dtype = np.int8)
        self.forget_prob = forget_prob
        self.board = np.zeros((board_size, board_size))
        
        # VOOR ONS: for testing
        self.full_board = np.array([[1,7,6,0],[3,5,7,2],[4,0,2,1],[3,6,4,5]])

    # Return the two cards the AI will turn around
    def make_move(self):
        # If two positions are known for a set, turn around those two cards
        known_set = self.check_known_set()
        if known_set != -1:
            return self.known_cards[known_set,0], self.known_cards[known_set,1]
        
        # Pick a random unknown card. If you know the other card of this set, turn around that card
        first_card = self.random_move()
        if self.known_cards[first_card,1,0] != -1:
            return self.known_cards[first_card,0], self.known_cards[first_card,1]
        
        # Pick a second random unknown card
        second_card = self.random_move()
        return self.known_cards[first_card,0], self.known_cards[second_card, 0 if self.known_cards[second_card,1,0] == -1 else 1]
   
    # Store a position together with the observed card
    def update(self, card, position):
        if self.known_cards[card,0,0] == -1:
            self.known_cards[card,0] = position[0]
        elif (self.known_cards[card,0] != position[0]).all():
            self.known_cards[card,1] = position[0]
        # Indicate that the card at that position has been seen
        self.board[position[0,0],position[0,1]] = 1

    # Return if both position of a pair of cards is known
    def check_known_set(self):
                # VOOR ONS: later ook voor de eerste de hoogste prob pakken
        for card_index in range(len(self.known_cards)):
            if self.known_cards[card_index,1,0] != -1:
                return card_index
        return -1

    # Pick random move from all unknown locations in the board
    def random_move(self):
                # VOOR ONS: random getal (prob voor of we geziene kaarten nog eens om gaan draaien)
        # Random choice of all unknown locations
        possible_positions = list(zip(*np.where(self.board == 0)))
        move = random.choice(possible_positions)
        position = np.array([move[0], move[1]]).reshape((1,2))
        # Observe card at the chosen position
        card_value = self.get_card(position) #GET_CARD from GAME
        # Update knowlegde
        self.update(card_value, position)
        return card_value
    
    def get_card(self, position):
        return self.full_board[position[0,0], position[0,1]]

def main():
    board_size = 4
    ai = AI(board_size)
    for i in range(10):
        print("iteration: ", i)
        move = ai.make_move()
        #KAARTWAARDES PRINTEN
        print("moves: ", move[0],"and", move[1])

main()