
import os, random, time, pygame, ai, numpy as np
from generate_cards import CardGenerator

#Load modules and initialize display
class memory_game:

    def __init__(self):
        pygame.init()

        # difficulty
        self.difficulty = 1  # 0-10

        # card size/shape
        self.card_len = 100 # both width and length
        self.card_margin = 10 # space inbetween cards
        
        # card top offset
        self.vert_offset = 140

        # number offset
        self.card_hor_pad = 37
        self.card_ver_pad = 22
        
        # game settings
        self.ai_difficulty = "easy"
        self.game_difficulty = "easy"
        self.player_mode = 0

        # board setup
        self.rows = 4
        self.columns = 6

        self.text_list = None

        self.screen = ((self.columns * (self.card_margin + self.card_len ) + self.card_margin), (self.rows * (self.card_margin + self.card_len) + self.vert_offset) + self.card_margin)
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

        # create cards, value grid, and card grid.
        self.cards, self.card_val_grid, self.card_grid = self.card_gen()
        print(self.cards)

        # load the images for the sprites
        # TODO different picture for each card value
        # generates and loads all cards using the CardGenerator:
        self.card_generator = CardGenerator()
        self.card_generator.set_difficulty(self.difficulty)
        self.card_generator.set_size(self.card_len)
        cards = self.card_generator.generate_cards(int(self.rows*self.columns))

        self.images = [pygame.image.frombuffer(card.flatten(), (self.card_len, self.card_len), "RGB") for card in cards]

        self.face_down_card_img = pygame.image.load("../memory.png").convert()

        self.face_down_card = self.face_down_card_img.get_rect()

        self.matched_img = pygame.image.load("../matched.png").convert()
        self.matched_card = self.matched_img.get_rect()

        self.selected_card_img = pygame.image.load("../selected.png").convert()
        self.selected_card = self.selected_card_img.get_rect()

        self.wrong_img = pygame.image.load("../wrong.png").convert()
        self.wrong_card = self.wrong_img.get_rect()

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

        # progam loop
        self.game_state = 0
        self.program()


    def program(self):
        if self.game_state == 0:
            self.option_select()
        if self.game_state == 1:
            # gameloop
            self.game_loop()


    def card_gen(self):
        assert int((self.rows*self.columns)%2) == 0, "Combination of rows and columns does not create a even number"
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
                        self.card_grid[i].append(pygame.Rect(
                            self.card_margin,
                            self.card_margin + self.vert_offset,
                            self.card_len,
                            self.card_len
                        ))
                    else:
                        self.card_grid[i].append(pygame.Rect(
                            self.card_grid[i][j-1].x + self.card_len + self.card_margin,
                            self.card_margin + self.vert_offset,
                            self.card_len,
                            self.card_len
                        ))
            else:
                for j in range(self.columns):
                    # first column alsop needs to be offset from the side
                    if j == 0:
                        self.card_grid[i].append(pygame.Rect(
                            self.card_margin,
                            self.card_grid[i-1][0].y + self.card_len + self.card_margin,
                            self.card_len, self.card_len
                        ))
                    else:
                        self.card_grid[i].append(pygame.Rect(
                            self.card_grid[i][j-1].x + self.card_len + self.card_margin,
                            self.card_grid[i-1][0].y + self.card_len + self.card_margin,
                            self.card_len,
                            self.card_len
                        ))
    

    def check_mouseclick(self):
        # get list of presses
        pressed = list(pygame.mouse.get_pressed())
        # loop through the buttons
        for button in pressed:
            if button:
                for i in range(self.rows):
                    for j in range(self.columns):
                        mouse_pos = list(pygame.mouse.get_pos())
                        if self.card_grid[i][j].x <= mouse_pos[0] <= self.card_grid[i][j].x + self.card_len and \
                                self.card_grid[i][j].y <= mouse_pos[1] <= self.card_grid[i][j].y + self.card_len:
                            has_instance = False
                            for k in range(len(self.exposed)):
                                if self.exposed[k] == [i, j]:
                                    has_instance = True

                            for k in range(len(self.matched)):
                                if self.matched[k] == [i, j]:
                                    has_instance = True

                            if not has_instance:
                                self.exposed.append([i, j])


    def draw_cards(self):
            for i in range(self.rows):
                for j in range(self.columns):
                    pygame.draw.rect(self.display, (255, 255, 255), self.card_grid[i][j])
                    self.face_down_card.topleft = self.card_grid[i][j].topleft
                    self.display.blit(self.face_down_card_img, self.face_down_card)


    def draw_flipside(self):
        if self.exposed:
            for i in self.exposed:
                # get value of the card
                text = str(self.card_val_grid[i[0]][i[1]])
                # create card value in certain font
                render = self.arial_50.render(text, True, self.black)
                # draw exposed card
                image_index = self.cards[i[0]*self.columns+i[1]]
                self.selected_card.topleft = self.card_grid[i[0]][i[1]].topleft
                #self.display.blit(self.selected_card_img, self.selected_card)   # display placeholder
                # display correct image:
                self.display.blit(self.images[image_index], self.selected_card)
                # display number to screen
                self.display.blit(render, (self.card_grid[i[0]][i[1]].x + self.card_hor_pad, self.card_grid[i[0]][i[1]].y + self.card_ver_pad))

        if self.matched:
            for i in self.matched:
                # get value of the card
                text = str(self.card_val_grid[i[0]][i[1]])
                # create card value in certain font
                render = self.arial_50.render(text, True, self.green)
                # draw matched card
                image_index = self.cards[i[0] * self.columns + i[1]]
                self.matched_card.topleft = self.card_grid[i[0]][i[1]].topleft
                #self.display.blit(self.matched_img, self.matched_card)
                self.display.blit(self.images[image_index], self.matched_card)
                # display matched number to screen
                self.display.blit(render, (self.card_grid[i[0]][i[1]].x + self.card_hor_pad, self.card_grid[i[0]][i[1]].y + self.card_ver_pad))

        if self.wrong:
            for i in self.wrong:
                # get value of the card
                text = str(self.card_val_grid[i[0]][i[1]])
                # create card value in certain font
                render = self.arial_50.render(text, True, self.red)
                # draw wrong card rectangle
                image_index = self.cards[i[0] * self.columns + i[1]]
                self.wrong_card.topleft = self.card_grid[i[0]][i[1]].topleft
                # self.display.blit(self.wrong_img, self.wrong_card)
                self.display.blit(self.images[image_index], self.wrong_card)
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

            
    def clunge_function(self, functionality):
        smallfont = pygame.font.SysFont('Arial',35)
        white_color = (255,255,255)

        if functionality == "start" : 
            self.screen = ((self.columns * (self.card_margin + self.card_len ) + self.card_margin), (self.rows * (self.card_margin + self.card_len) + self.vert_offset) + self.card_margin)
            self.cards, self.card_val_grid, self.card_grid = self.card_gen()
            self.fill_grid()
            self.display = pygame.display.set_mode(self.screen)
            self.game_state = 1
            if self.player_mode == 1:
                ai_player = ai.AI(self.rows, self.columns, mode = self.ai_difficulty)
            
        elif functionality == "quit":
            pygame.quit()

        elif functionality == "ai_dif_easy":
            self.ai_difficulty = "easy"
            self.text_list["ai_difficulty_status"] = smallfont.render(self.ai_difficulty, True , white_color)

        elif functionality == "ai_dif_med":
            self.ai_difficulty = "medium"
            self.text_list["ai_difficulty_status"] = smallfont.render(self.ai_difficulty, True , white_color)

        elif functionality == "ai_dif_hard":
            self.ai_difficulty = "hard"
            self.text_list["ai_difficulty_status"] = smallfont.render(self.ai_difficulty, True , white_color)

        elif functionality == "game_dif_easy":
            self.game_difficulty = "easy"
            self.text_list["game_difficulty_status"] = smallfont.render(self.game_difficulty, True , white_color)

        elif functionality == "game_dif_medium":
            self.game_difficulty = "medium"
            self.text_list["game_difficulty_status"] = smallfont.render(self.game_difficulty, True , white_color)

        elif functionality == "game_dif_hard":
            self.game_difficulty = "hard"
            self.text_list["game_difficulty_status"] = smallfont.render(self.game_difficulty, True , white_color)

        elif functionality == "human_human":
            self.player_mode = 0
            self.text_list["players_status"] = smallfont.render(self.game_mode[self.player_mode], True , white_color)
            
        elif functionality == "human_ai":
            self.player_mode = 1
            self.text_list["players_status"] = smallfont.render(self.game_mode[self.player_mode], True , white_color)

        elif functionality == "size_4x4":  
            self.rows = 4
            self.columns = 4
            self.text_list["game_grid_status"] = smallfont.render(str(self.rows)+" x "+str(self.columns), True , white_color)
            
        elif functionality == "size_4x7":
            self.rows = 4
            self.columns = 7
            self.text_list["game_grid_status"] = smallfont.render(str(self.rows)+" x "+str(self.columns), True , white_color)

        elif functionality == "size_5x8":
            self.rows = 5
            self.columns = 8
            self.text_list["game_grid_status"] = smallfont.render(str(self.rows)+" x "+str(self.columns), True , white_color)
            
        elif functionality == "size_6x10":
            self.rows = 6
            self.columns = 10
            self.text_list["game_grid_status"] = smallfont.render(str(self.rows)+" x "+str(self.columns), True , white_color)

    """
    YET TO BE IMPLEMENTED:
    Will contain buttons to change number of cards, and if one wants to play with 2 players or against an AI
    """
    def option_select(self):

        # dark shade of the button
        color_dark = (100,100,100)

        # light shade of the button
        color_light = (170,170,170)

        # white color
        white_color = (255,255,255)

        # Button location [width, height]
        button_loc = {"start": [505, 10],
        "quit" : [25, 10],
        "ai_dif_easy" : [80, 130],
        "ai_dif_med" : [265, 130],
        "ai_dif_hard" : [450, 130],
        "game_dif_easy" : [80, 260],
        "game_dif_medium" : [265, 260],
        "game_dif_hard" : [450, 260],
        "human_human" : [140, 390],
        "human_ai" : [390, 390],
        "size_4x4" : [22, 530],
        "size_4x7" : [184, 530],
        "size_5x8" : [346, 530],
        "size_6x10" : [508, 530]}

        button_width = 140
        button_height = 40

        # defining a font
        smallfont = pygame.font.SysFont('Arial',35)

        text_locations = {key: button_loc[key] for key in button_loc}
        
        text_locations2 = {"ai_difficulty" : [205, 70],
        "game_difficulty" : [180, 205],
        "players" : [155, 335],
        "game_grid" : [155, 470],
        "ai_difficulty_status" : [355, 70],
        "game_difficulty_status" : [385, 205],
        "players_status" : [375, 335],
        "game_grid_status" : [385, 470]
        }

        text_locations.update(text_locations2)

        # create text
        self.text_list = {"start": smallfont.render('Start' , True , white_color),
        "quit" : smallfont.render('Quit' , True , white_color),
        "ai_difficulty" : smallfont.render('AI difficulty:' , True , white_color),
        "ai_dif_easy" : smallfont.render('Easy' , True , white_color),
        "ai_dif_med" : smallfont.render('Medium' , True , white_color),
        "ai_dif_hard" : smallfont.render('Hard' , True , white_color),
        "game_difficulty" : smallfont.render('Game Difficulty:' , True , white_color),
        "game_dif_easy" : smallfont.render('Easy' , True , white_color),
        "game_dif_medium" : smallfont.render('Medium' , True , white_color),
        "game_dif_hard" : smallfont.render('Hard' , True , white_color),
        "players" : smallfont.render('Who are playing:' , True , white_color),
        "human_human" : smallfont.render('vs Human' , True , white_color),
        "human_ai" : smallfont.render('vs AI' , True , white_color),
        "game_grid" : smallfont.render('How many cards:' , True , white_color),
        "size_4x4" : smallfont.render('4 x 4' , True , white_color),
        "size_4x7" : smallfont.render('4 x 7' , True , white_color),
        "size_5x8" : smallfont.render('5 x 8' , True , white_color),
        "size_6x10" : smallfont.render('6 x 10' , True , white_color),
        "ai_difficulty_status" : smallfont.render(self.ai_difficulty, True , white_color),
        "game_difficulty_status" : smallfont.render(self.game_difficulty, True , white_color),
        "players_status" : smallfont.render(self.game_mode[self.player_mode], True , white_color),
        "game_grid_status" : smallfont.render(str(self.rows)+" x "+str(self.columns), True , white_color)}
        
        self.rows = 4
        self.columns = 4
        self.text_list["game_grid_status"] = smallfont.render(str(self.rows)+" x "+str(self.columns), True , white_color)

        while self.game_state == 0:

            # Clear screen
            self.display.fill(self.black)

            for ev in pygame.event.get():

                if ev.type == pygame.QUIT:
                    pygame.quit()

                #checks if a mouse is clicked
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    for key in button_loc:
                        b_width, b_height = button_loc[key]
                        if b_width <= mouse[0] <= b_width + button_width and b_height <= mouse[1] <= b_height + button_height:
                            self.clunge_function(key)

            # mouse coordinates
            mouse = pygame.mouse.get_pos()

            # if mouse is hovered on a button it changes to lighter shade
            for width, height in button_loc.values():
                if width <= mouse[0] <= width+button_width and height <= mouse[1] <= height+button_height:
                    pygame.draw.rect(self.display,color_light,[width,height,button_width,button_height])
                else:
                    pygame.draw.rect(self.display,color_dark,[width,height,button_width,button_height])

            # superimposing text onto a button
            for ids in text_locations.keys():
                self.display.blit(self.text_list[ids] , (text_locations[ids][0]+20,text_locations[ids][1]))

            # updates the frames of the game
            pygame.display.flip()
            
    def game_loop(self):
        while self.game_state == 1:
            for event in pygame.event.get():
                # Detect quit
                if event.type == pygame.QUIT:
                    pygame.quit()

            # Check for mouse click
            self.check_mouseclick()
            
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
            self.display.blit(title, (self.screen[0]/2 - 45, 10))

            # Display who's turn it is
            turn_text = self.arial_20.render("Player's {} turn".format(str(self.player_turn + 1)), True, self.white)
            self.display.blit(turn_text, (self.screen[0]/2 - 45, 55))

            # Display match score
            currentmatch_text = self.arial_20.render("Player 1: {}    Player 2: {}".format(self.game_score[0],self.game_score[1]), True, self.white)
            self.display.blit(currentmatch_text, (self.screen[0]/2 - 82, 90))

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