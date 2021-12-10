import numpy as np
import random

class AI:
    def __init__(self, board_size, forget_prob=0.4):
        self.known_cards = -1*np.ones((int(board_size*board_size/2),2,3), dtype = np.int8)
        
        # Easy = 0.7
        # Medium = 0.4
        # Hard = 0.1
        self.forget_prob = forget_prob
        self.threshold = 0.5
        self.board = np.zeros((board_size, board_size))
        
        # VOOR ONS: for testing
        self.full_board = np.array([[1,7,6,0],[3,5,7,2],[4,0,2,1],[3,6,4,5]])

        # VOOR ONS: "ik wil deze kaart pakken", kans implementeren dat je ernaast zit. Noise op de move


    # Return the two cards the AI will turn around
    def make_move(self, opp_move, opp_card, opp_pair):
        self.known_cards[self.known_cards[:,:,2]>-1,2] += 1
        # If opponent has pair remove from board and seen cards (to avoid choosing those cards to turn around)        
        if opp_pair:
            self.board[opp_move[0,0]][opp_move[0,1]] = -1
            self.board[opp_move[1,0]][opp_move[1,1]] = -1
            self.known_cards[opp_card[0]] = np.array([[-1,-1,-1],[-1,-1,-1]])
        else:
            # Update the knowledge with the opponent's move
            self.update(opp_card[0], opp_move[0])
            self.update(opp_card[1], opp_move[1])

        self.known_cards[self.known_cards[:,:,2]>-1,2] += 1


        # If two positions are known for a set, turn around those two cards
        known_set = self.check_known_set()
        if known_set != -1:
            first_move = np.copy(self.known_cards[known_set,0,0:2])
            second_move = np.copy(self.known_cards[known_set,1,0:2])
            self.board[first_move[0]][first_move[1]] = -1
            self.board[second_move[0]][second_move[1]] = -1
            self.known_cards[known_set] = np.array([[-1,-1,-1],[-1,-1,-1]])
            return first_move, second_move
        
        # Pick a random unknown card. If you know the other card of this set, turn around that card
        first_card = self.random_move()
        if self.known_cards[first_card,1,0] != -1:
            probability = self.calculate_probability(self.known_cards[first_card,0,2])
            print("set", self.known_cards[first_card,0,2], probability)
            if probability > self.threshold:
                first_move = np.copy(self.known_cards[first_card,1,0:2])
                second_move = np.copy(self.known_cards[first_card,0,0:2])
                self.board[first_move[0]][first_move[1]] = -1
                self.board[second_move[0]][second_move[1]] = -1
                self.known_cards[first_card] = np.array([[-1,-1,-1],[-1,-1,-1]])
                print("yeey pair")
                return first_move, second_move
        
        # Pick a second random unknown card
        second_card = self.random_move()
        first_move = np.copy(self.known_cards[first_card,0,0:2])
        second_move = np.copy(self.known_cards[second_card, 0 if self.known_cards[second_card,1,0] == -1 else 1, 0:2])
        if first_card == second_card:
            self.board[first_move[0]][first_move[1]] = -1
            self.board[second_move[0]][second_move[1]] = -1
            self.known_cards[first_card] = np.array([[-1,-1,-1],[-1,-1,-1]])
        return first_move, second_move
   

    # Store a position together with the observed card
    def update(self, card, position):
        if self.known_cards[card,0,0] == -1:
            self.known_cards[card,0,0:2] = position
            self.known_cards[card,0,2] = 0
        elif (self.known_cards[card,0,0:2] != position).all():
            self.known_cards[card,1,0:2] = position
            self.known_cards[card,1,2] = 0
        else:
            self.known_cards[card,0,2] = 0

        # Indicate that the card at that position has been seen
        self.board[position[0],position[1]] = 1


    # Return if both position of a pair of cards is known
    def check_known_set(self):
        highest_prob = 0
        highest_card = -1
        for card_index in range(len(self.known_cards)):
            if self.known_cards[card_index,1,0] != -1:
                probability = (self.calculate_probability(self.known_cards[card_index,0,2]) + self.calculate_probability(self.known_cards[card_index,1,2]))/2
                # print(self.known_cards[first_card,1,2], probability)
                if probability > highest_prob:
                    highest_prob = probability
                    highest_card = card_index

        if highest_prob > self.threshold:
            return highest_card
        
        return -1


    # Pick random move from all unknown locations in the board
    def random_move(self):
                # VOOR ONS: random getal (prob voor of we geziene kaarten nog eens om gaan draaien)
        # Random choice of all unknown locations
        possible_positions = list(zip(*np.where(self.board == 0)))
        move = random.choice(possible_positions)
        position = np.array([move[0], move[1]])
        # Observe card at the chosen position
        card_value = self.get_card(position) #GET_CARD from GAME
        # Update knowlegde
        self.update(card_value, position)
        return card_value
    

    def get_card(self, position):
        return self.full_board[position[0], position[1]]


    def calculate_probability(self, time):
        # VOOR ONS: Aan de rand of naast lege vakjes beter onthouden
        if time == -1:
            return 0
        noise = np.random.normal(0,0.05)
        return max(min(np.exp(-time / (15*(1-self.forget_prob))) + noise ,1) ,0)


def main():
    board_size = 4
    ai = AI(board_size)
    #self.full_board = np.array([[1,7,6,0],[3,5,7,2],[4,0,2,1],[3,6,4,5]])

    opp_card = np.array([[2,1],[7,7],[1,5]])
    opp_move = np.array([[[2,2],[2,3]], [[1,2],[0,1]], [[0,0],[3,3]]])
    opp_pair = [False, True, False]
    
    for i in range(3):
        print("iteration: ", i)
        move = ai.make_move(opp_move[i], opp_card[i], opp_pair[i])
        #KAARTWAARDES PRINTEN
        print("moves: ", move[0],"and", move[1])

main()