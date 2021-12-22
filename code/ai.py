import numpy as np
import random


class AI:
    def __init__(self, nr_rows, nr_columns, mode="medium"):
        self.rows = nr_rows
        self.cols = nr_columns
        self.centre = [self.rows / 2, self.cols / 2]
        self.known_cards = -1 * np.ones((int(self.rows * self.cols / 2), 2, 3), dtype=np.int8)

        self.threshold = 0.5
        if mode == "easy":
            self.forget_prob = 0.7
        elif mode == "medium":
            self.forget_prob = 0.4
        else:
            self.forget_prob = 0.1
        self.board = np.zeros((nr_rows, nr_columns))

        # VOOR ONS: for testing
        # self.full_board = np.array([[1,7,6,0],[3,5,7,2],[4,0,2,1],[3,6,4,5]])

    def observe_opp_move(self, opp_move, opp_card, opp_pair):
        self.known_cards[self.known_cards[:, :, 2] > -1, 2] += 1
        # If opponent has pair remove from board and seen cards (to avoid choosing those cards to turn around)        
        if opp_pair:
            print("we have a pair")
            self.board[opp_move[0][0]][opp_move[0][1]] = -1
            self.board[opp_move[1][0]][opp_move[1][1]] = -1
            self.known_cards[opp_card[0]] = np.array([[-1, -1, -1], [-1, -1, -1]])
        else:
            # Update the knowledge with the opponent's move
            self.update(opp_card[0], opp_move[0])
            self.update(opp_card[1], opp_move[1])

    def make_first_move(self):
        self.known_cards[self.known_cards[:, :, 2] > -1, 2] += 1
        # If two positions are known for a set, turn around those two cards
        known_set = self.check_known_set()
        if known_set != -1:
            # Add some noise over selection
            first_move = self.selection_noise(self.known_cards[known_set, 0])
        else:
            first_move = self.random_move()
        # Update knowledge
        self.first_move = first_move

        return first_move

    # Return the two cards the AI will turn around
    def make_second_move(self, first_card):
        self.first_card = first_card
        self.update(first_card, self.first_move)
        # Pick a random unknown card. If you know the other card of this set, turn around that card
        if self.known_cards[first_card, 1, 0] != -1:
            other_pos = 0 if (self.known_cards[first_card, 1, 0:2] == self.first_move).all() else 1
            probability = self.calculate_probability(self.known_cards[first_card, other_pos])
            if probability > self.threshold:
                # desired_second_move = np.copy(self.known_cards[first_card, other_pos, 0:2])
                original_move = self.known_cards[first_card, other_pos]
                self.second_move = self.selection_noise(original_move)
                if self.first_move == self.second_move:
                    self.second_move = original_move
                return self.second_move

        self.second_move = self.random_move()
        while self.first_move == self.second_move:
            self.second_move = self.random_move()
        return self.second_move

    def update_second_move(self, second_card):
        if self.first_card == second_card:
            self.board[self.first_move[0]][self.first_move[1]] = -1
            self.board[self.second_move[0]][self.second_move[1]] = -1
            self.known_cards[self.first_card] = np.array([[-1, -1, -1], [-1, -1, -1]])
            print("yeey pair")
        else:
            self.update(second_card, self.second_move)

    # Store a position together with the observed card
    def update(self, card, position):
        if self.known_cards[card, 0, 0] == -1:
            self.known_cards[card, 0, 0:2] = position
            self.known_cards[card, 0, 2] = 0
        elif (self.known_cards[card, 0, 0:2] != position).all():            
            self.known_cards[card, 1, 0:2] = position
            self.known_cards[card, 1, 2] = 0
        else:
            self.known_cards[card, 0, 2] = 0

        # Indicate that the card at that position has been seen
        self.board[position[0], position[1]] = 1


    # Return if both position of a pair of cards is known
    def check_known_set(self):
        highest_prob = 0
        highest_card = -1
        for card_index in range(len(self.known_cards)):
            if self.known_cards[card_index, 1, 0] != -1:
                probability = (self.calculate_probability(self.known_cards[card_index, 0]) + self.calculate_probability(
                    self.known_cards[card_index, 1])) / 2
                if probability > highest_prob:
                    highest_prob = probability
                    highest_card = card_index

        if highest_prob > self.threshold:
            return highest_card

        return -1

    # Pick random move from all unknown locations in the board
    def random_move(self):
        # Random choice of all unknown locations
        possible_positions = []
        for i, row in enumerate(self.board):
            for j, element in enumerate(row):
                random_prob = random.random()
                if element == 0 and random_prob > self.forget_prob / 3:
                    possible_positions.append([i, j])
                elif element == 1 and random_prob > (1 - self.forget_prob / 2):
                    possible_positions.append([i, j])
        if possible_positions == []:
            possible_positions = list(zip(*np.where(self.board == 0)))
            if possible_positions == []:
                possible_positions = list(zip(*np.where(self.board == 1)))
                
        move = random.choice(possible_positions)
        # position = np.array([move[0], move[1]])
        # Observe card at the chosen position

        return [move[0], move[1]]

    # def get_card(self, position):
    #    return self.full_board[position[0], position[1]]

    def calculate_probability(self, position):
        time = position[2]
        if time == -1:
            return 0
        noise = np.random.normal(0, 0.05)
        close_to_border = max(1, np.sqrt((self.centre[0] - position[0]) ** 2 + (self.centre[1] - position[1]) ** 2))
        probability = max(min(np.exp(-time / (15 * close_to_border * (1 - self.forget_prob))) + noise, 1), 0)
        return probability

    def selection_noise(self, move):
        moves_ago = move[2]
        sigma_x = self.forget_prob * np.sqrt(moves_ago * self.rows) / 4
        sigma_y = self.forget_prob * np.sqrt(moves_ago * self.cols) / 4
        cov = [[sigma_x, 0], [0, sigma_y]]

        new_move = np.random.multivariate_normal(move[0:2], cov)
        new_move = [max(min(int(new_move[0]), self.rows - 1), 0), max(min(int(new_move[1]), self.cols - 1), 0)]
        if self.board[int(new_move[0]),int(new_move[1])] == -1:
            return [move[0], move[1]]
        else:
            return new_move

# def main():
#     nr_rows = 4
#     nr_cols = 4
#     ai = AI(nr_rows, nr_cols)
#     #self.full_board = np.array([[1,7,6,0],[3,5,7,2],[4,0,2,1],[3,6,4,5]])

#     opp_card = np.array([[2,1],[7,7],[1,5],[6,2]])
#     opp_move = np.array([[[2,2],[2,3]], [[1,2],[0,1]], [[0,0],[3,3]],[[0,2],[1,3]]])
#     opp_pair = [False, True, False, False]

#     for i in range(4):
#         print("iteration: ", i)
#         move = ai.make_move(opp_move[i], opp_card[i], opp_pair[i])
#         #KAARTWAARDES PRINTEN
#         print("moves: ", move[0],"and", move[1])

# main()
