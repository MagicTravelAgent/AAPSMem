import os, random, time, pygame
#Load modules and initialize display


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


# create card sprites grid
card_grid = [[] for i in range(rows)]

# load the images for the sprites
img_test = pygame.image.load("memory.png")
img_test.convert()
rect = img_test.get_rect()

for i in range(rows):
    # the first row needs to be a bite more offset from the top?
    if i == 0:
        for j in range(columns):

            # first column alsop needs to be offset from the side
            if j == 0:
                card_grid[i].append(pygame.Rect(card_margin, card_margin, card_len, card_len))
            else:
                card_grid[i].append(pygame.Rect(card_grid[i][j-1].x + card_len + card_margin, card_margin, card_len, card_len))
    else:
        for j in range(columns):
            
            # first column alsop needs to be offset from the side
            if j == 0:
                card_grid[i].append(pygame.Rect(card_margin, card_grid[i-1][0].y + card_len + card_margin, card_len, card_len))
            else:
                card_grid[i].append(pygame.Rect(card_grid[i][j-1].x + card_len + card_margin, card_grid[i-1][0].y + card_len + card_margin, card_len, card_len))

# TODO create game mode select screen
# game mode
game_mode = {0: 'humans', 1: 'ai'}

# player scores (p1 = 0, p2 = 1)
game_score = {0: 0, 1: 0}
overall_score = {0: 0, 1: 0}

# keeps track of who's turn it is
player_turn = 0 # start with p1 (p1 = 0, p2 = 1)


# list of currently exposed cards (max 2)
global exposed
exposed = []

# list of already matched cards
global matched
matched = []

# list of cards which did not match in a turn (always 2)
global wrong
wrong = []


#Game loop
while True:
    for event in pygame.event.get():
        #Detect quit
        if event.type == pygame.QUIT:
            pygame.quit()

    #Check for mouse click
    pressed = list(pygame.mouse.get_pressed())
    for button in pressed:
        if button:
            for i in range(rows):
                for j in range(columns):
                    mouse_pos = list(pygame.mouse.get_pos())
                    if mouse_pos[0] >= card_grid[i][j].x and mouse_pos[1] >= card_grid[i][j].y and mouse_pos[0] <= card_grid[i][j].x + card_len and mouse_pos[1] <= card_grid[i][j].y + card_len:
                        global has_instance
                        has_instance = False
                        for k in range(len(exposed)):
                            if exposed[k] == [i, j]:
                                has_instance = True

                        for k in range(len(matched)):
                            if matched[k] == [i, j]:
                                has_instance = True

                        if has_instance == False:
                            exposed.append([i, j])

    # if two cards have been turned 
    if len(exposed) == 2:

        # check if they match
        if card_val_grid[exposed[0][0]][exposed[0][1]] == card_val_grid[exposed[1][0]][exposed[1][1]]: # match
            matched.extend(exposed)
            exposed.clear()
            
            # increment player score
            game_score[player_turn] =+ 1
            
        else: # no match
            wrong.extend(exposed)
            exposed.clear()

        # change turn
        if player_turn == 0:
            player_turn = 1
        else:
            player_turn = 0

    #Clear screen
    display.fill(black)

    #Draw cards
    for i in range(rows):
        for j in range(columns):
            pygame.draw.rect(display, (255, 255, 255), card_grid[i][j])
            
    #Draw numbers
    if exposed:
        for i in exposed:
            # get value of the card
            text = str(card_val_grid[i[0]][i[1]])
            # create card value in certain font
            render = arial_50.render(text, True, black)
            # display to screen
            display.blit(render, (card_grid[i[0]][i[1]].x + card_hor_pad, card_grid[i[0]][i[1]].y + card_ver_pad))

    if matched:
        for i in matched:
            # get value of the card
            text = str(card_val_grid[i[0]][i[1]])
            # create card value in certain font
            render = arial_50.render(text, True, green)
            # display to screen
            display.blit(render, (card_grid[i[0]][i[1]].x + card_hor_pad, card_grid[i[0]][i[1]].y + card_ver_pad))

    if wrong:
        for i in wrong:
            # get value of the card
            text = str(card_val_grid[i[0]][i[1]])
            # create card value in certain font
            render = arial_50.render(text, True, red)
            # display to screen
            display.blit(render, (card_grid[i[0]][i[1]].x + card_hor_pad, card_grid[i[0]][i[1]].y + card_ver_pad))

    #Draw other stuff
    title = arial_35.render("Memory", True, white)
    display.blit(title, (570, 10))

    # Display who's turn it is
    turn_text = arial_20.render("Player's {} turn".format(str(player_turn + 1)), True, white)

    display.blit(turn_text, (580, 75))

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