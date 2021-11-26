class CardGenerator:
    def __init__(self):
        self.difficulty = 0
        self.card_size = 100
        pass

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def set_size(self, card_size):
        self.card_size = card_size

    def generate_cards(self, n_cards):
        cards = []
        for i in range(n_cards):
            pass
