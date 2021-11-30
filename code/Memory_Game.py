import os, random, time, pygame
#Load modules and initialize display


<<<<<<< HEAD
#class memory_game:

#    def __init__(self):
        
pygame.init()
screen = (1000,600)
pygame.display.set_caption("Memory")
display = pygame.display.set_mode(screen)

#Define objects and generate number grid
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
arial_200 = pygame.font.SysFont("Arial", 200)
arial_50 = pygame.font.SysFont("Arial", 50)
arial_35 = pygame.font.SysFont("Arial", 35)
arial_20 = pygame.font.SysFont("Arial", 20)

# card size/shape
card_len = 100
card_margin = 10
card_hor_pad = 37
card_ver_pad = 22

# board setup
rows = 4
columns = 5

# create list of numbers to represent card values
cards = [i for i in range(10) for j in range(2)]
# shuffle these values
random.shuffle(cards)
# apply shuffled values to the grid so each item in the grid is the true value
card_val_grid = [cards[i*len(cards) // rows:(i+1)*len(cards) // rows] for i in range(rows)]


# create rectangles of the card grid
card_grid = [[] for i in range(rows)]

for i in range(rows):
    # the first row needs to be a bite more offset from the top?
    if i == 0:
        for j in range(columns):

            # first column alsop needs to be offset from the side
            if j == 0:
                card_grid[i].append(pygame.Rect(card_margin, card_margin, card_len, card_len))
=======
class memory_game:

    def __init__(self):
        pygame.init()
        self.screen = (1000,600)
        pygame.display.set_caption("Memory")
        self.display = pygame.display.set_mode(self.screen)

        #Define objects and generate number grid
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.arial_200 = pygame.font.SysFont("Arial", 200)
        self.arial_50 = pygame.font.SysFont("Arial", 50)
        self.arial_35 = pygame.font.SysFont("Arial", 35)
        self.arial_20 = pygame.font.SysFont("Arial", 20)

        # card size/shape
        self.card_len = 100
        self.card_margin = 10
        self.card_hor_pad = 37
        self.card_ver_pad = 22

        # board setup
        self.rows = 4
        self.columns = 5

        # create cards, value grid, and card grid.
        self.cards, self.card_val_grid, self.card_grid = self.card_gen()

        # load the images for the sprites
        self.img_test = pygame.image.load("memory.png")
        self.img_test.convert()
        self.rect = self.img_test.get_rect()

        # fill card_grid with images
        self.fill_grid()

        # TODO create game mode select screen
        # game mode
        self.game_mode = {0: 'humans', 1: 'ai'}

        # player scores (p1 = 0, p2 = 1)
        self.game_score = {0: 0, 1: 0}           # current game matches
        self.overall_score = {0: 0, 1: 0}        # game wins

        # keeps track of who's turn it is
        self.player_turn = 0 # start with p1 (p1 = 0, p2 = 1)
        self.player_correct = False # stores if the player found match in their turn

        # list of currently exposed cards (max 2)
        self.exposed = []

        # list of already matched cards
        self.matched = []

        # list of cards which did not match in a turn (always 2)
        self.wrong = []

        # gameloop
        self.game_loop()


    def card_gen(self):
        assert int((self.rows*self.columns/2)%2) == 0, "Combination of rows and columns does not create a even number"
        # create list of numbers to represent card values
        cards = [i for i in range(int(self.rows*self.columns/2)) for j in range(2)]
        # shuffle these values
        random.shuffle(cards)
        # apply shuffled values to the grid so each item in the grid is the true value
        card_val_grid = [cards[i*len(cards) // self.rows:(i+1)*len(cards) // self.rows] for i in range(self.rows)]
        # create card sprites grid
        card_grid = [[] for i in range(self.rows)]
        return cards, card_val_grid, card_grid


    def fill_grid(self):
        # fill grid with cards
        for i in range(self.rows):
            # the first row needs to be a bite more offset from the top?
            if i == 0:
                for j in range(self.columns):

                    # first column alsop needs to be offset from the side
                    if j == 0:
                        self.card_grid[i].append(pygame.Rect(self.card_margin, self.card_margin, self.card_len, self.card_len))
                    else:
                        self.card_grid[i].append(pygame.Rect(self.card_grid[i][j-1].x + self.card_len + self.card_margin, self.card_margin, self.card_len, self.card_len))
>>>>>>> b4ffc1e6b87d2e39b02122bde4ac0ee134ed8b11
            else:
                for j in range(self.columns):
                    
                    # first column alsop needs to be offset from the side
                    if j == 0:
                        self.card_grid[i].append(pygame.Rect(self.card_margin, self.card_grid[i-1][0].y + self.card_len + self.card_margin, self.card_len, self.card_len))
                    else:
                        self.card_grid[i].append(pygame.Rect(self.card_grid[i][j-1].x + self.card_len + self.card_margin, self.card_grid[i-1][0].y + self.card_len + self.card_margin, self.card_len, self.card_len))
    

    def check_mouseclick(self):
        # get list of presses
        pressed = list(pygame.mouse.get_pressed())
        # loop through the buttons
        for button in pressed:
            if button:
                for i in range(self.rows):
                    for j in range(self.columns):
                        mouse_pos = list(pygame.mouse.get_pos())
                        if mouse_pos[0] >= self.card_grid[i][j].x and mouse_pos[1] >= self.card_grid[i][j].y and mouse_pos[0] <= self.card_grid[i][j].x + self.card_len and mouse_pos[1] <= self.card_grid[i][j].y + self.card_len:
                            has_instance = False
                            for k in range(len(self.exposed)):
                                if self.exposed[k] == [i, j]:
                                    has_instance = True

                            for k in range(len(self.matched)):
                                if self.matched[k] == [i, j]:
                                    has_instance = True

                            if has_instance == False:
                                self.exposed.append([i, j])


    def draw_cards(self):
            for i in range(self.rows):
                for j in range(self.columns):
                    pygame.draw.rect(self.display, (255, 255, 255), self.card_grid[i][j])


    def draw_flipside(self):
        if self.exposed:
                for i in self.exposed:
                    # get value of the card
                    text = str(self.card_val_grid[i[0]][i[1]])
                    # create card value in certain font
                    render = self.arial_50.render(text, True, self.black)
                    # display to screen
                    self.display.blit(render, (self.card_grid[i[0]][i[1]].x + self.card_hor_pad, self.card_grid[i[0]][i[1]].y + self.card_ver_pad))

        if self.matched:
            for i in self.matched:
                # get value of the card
                text = str(self.card_val_grid[i[0]][i[1]])
                # create card value in certain font
                render = self.arial_50.render(text, True, self.green)
                # display to screen
                self.display.blit(render, (self.card_grid[i[0]][i[1]].x + self.card_hor_pad, self.card_grid[i[0]][i[1]].y + self.card_ver_pad))

        if self.wrong:
            for i in self.wrong:
                # get value of the card
                text = str(self.card_val_grid[i[0]][i[1]])
                # create card value in certain font
                render = self.arial_50.render(text, True, self.red)
                # display to screen
                self.display.blit(render, (self.card_grid[i[0]][i[1]].x + self.card_hor_pad, self.card_grid[i[0]][i[1]].y + self.card_ver_pad))

    def check_match(self):
            # check if they match
            if self.card_val_grid[self.exposed[0][0]][self.exposed[0][1]] == self.card_val_grid[self.exposed[1][0]][self.exposed[1][1]]:
                self.matched.extend(self.exposed)
                self.exposed.clear()
                    
                # increment player score
                self.game_score[self.player_turn] += 1

                # player found a match
                self.player_correct = True
                    
            else: # no match
                self.wrong.extend(self.exposed)
                self.exposed.clear()

            # change turn if the player did not get a match
            if not self.player_correct:
                if self.player_turn == 0:
                    self.player_turn = 1
                else:
                    self.player_turn = 0

            # set back to false after change check.
            self.player_correct = False

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                # Detect quit
                if event.type == pygame.QUIT:
                    pygame.quit()

            # Check for mouse click
            self.check_mouseclick()
            
<<<<<<< HEAD
        else: # no match
            wrong.extend(exposed)
            exposed.clear()

        # change turn if the player did not get a match
        if not player_correct:
            if player_turn == 0:
                player_turn = 1
            else:
                player_turn = 0

        # set back to false after change check.
        player_correct = False

    #Clear screen
    display.fill(black)

    # load the images for the sprites
    # TODO different picture for each card value
    face_down_card_img = pygame.image.load("memory.png").convert()
    face_down_card = face_down_card_img.get_rect()

    matched_img = pygame.image.load("matched.png").convert()
    matched_card = matched_img.get_rect()

    selected_card_img = pygame.image.load("selected.png").convert()
    selected_card = selected_card_img.get_rect()

    wrong_img = pygame.image.load("wrong.png").convert()
    wrong_card = wrong_img.get_rect()

    #Draw cards
    for i in range(rows):
        for j in range(columns):
            pygame.draw.rect(display, (255, 255, 255), card_grid[i][j])
            face_down_card.topleft = card_grid[i][j].topleft
            display.blit(face_down_card_img, face_down_card)
            
    #Draw numbers
    if exposed:
        for i in exposed:
            # get value of the card
            text = str(card_val_grid[i[0]][i[1]])
            # create card value in certain font
            render = arial_50.render(text, True, black)
            
            # display the selected card rect
            selected_card.topleft = card_grid[i[0]][i[1]].topleft
            display.blit(selected_card_img, selected_card)

            # display number to screen
            display.blit(render, (card_grid[i[0]][i[1]].x + card_hor_pad, card_grid[i[0]][i[1]].y + card_ver_pad))

    if matched:
        for i in matched:
            # get value of the card
            text = str(card_val_grid[i[0]][i[1]])
            # create card value in certain font
            render = arial_50.render(text, True, green)

            # display matched rect
            matched_card.topleft = card_grid[i[0]][i[1]].topleft
            display.blit(matched_img, matched_card)

            # display number to screen
            display.blit(render, (card_grid[i[0]][i[1]].x + card_hor_pad, card_grid[i[0]][i[1]].y + card_ver_pad))

    if wrong:
        for i in wrong:
            # get value of the card
            text = str(card_val_grid[i[0]][i[1]])
            # create card value in certain font
            render = arial_50.render(text, True, red)
            
            # display wrong rect
            wrong_card.topleft = card_grid[i[0]][i[1]].topleft
            display.blit(wrong_img, wrong_card)
            
            # display number to screen
            display.blit(render, (card_grid[i[0]][i[1]].x + card_hor_pad, card_grid[i[0]][i[1]].y + card_ver_pad))


    #Draw other stuff
    title = arial_35.render("Memory", True, white)
    display.blit(title, (570, 10))

    # Display who's turn it is
    turn_text = arial_20.render("Player's {} turn".format(str(player_turn + 1)), True, white)
    display.blit(turn_text, (580, 75))

    currentmatch_text = arial_20.render("Player 1: {}    Player 2: {}".format(game_score[0],game_score[1]), True, white)
    display.blit(currentmatch_text, (580, 105))

    #Check win
    if len(matched) == 20:
        display.fill(black)
        win = arial_200.render("You win!", True, green)
        display.blit(win, (40, 105))
        pygame.display.flip()
        break
    
    pygame.display.flip()
    if wrong:
        time.sleep(1)
        wrong.clear()
=======
            # if two cards have been turned 
            if len(self.exposed) == 2:
                self.check_match()

            # Clear screen
            self.display.fill(self.black)

            # Draw cards
            self.draw_cards()

            # Draw numbers of the card (when flipped)
            self.draw_flipside()

            # Draw Title
            title = self.arial_35.render("Memory", True, self.white)
            self.display.blit(title, (570, 10))

            # Display who's turn it is
            turn_text = self.arial_20.render("Player's {} turn".format(str(self.player_turn + 1)), True, self.white)
            self.display.blit(turn_text, (580, 75))

            # Display match score
            currentmatch_text = self.arial_20.render("Player 1: {}    Player 2: {}".format(self.game_score[0],self.game_score[1]), True, self.white)
            self.display.blit(currentmatch_text, (580, 105))

            # Check win
            if len(self.matched) == self.rows*self.columns:
                self.display.fill(self.black)
                win = self.arial_200.render("You win!", True, self.green)
                self.display.blit(win, (40, 105))
                pygame.display.flip()
                break
            
            pygame.display.flip()
            if self.wrong:
                time.sleep(1)
                self.wrong.clear()

mg = memory_game()
>>>>>>> b4ffc1e6b87d2e39b02122bde4ac0ee134ed8b11
