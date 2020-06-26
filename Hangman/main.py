import pygame
import os
import math
import random

#setting display
pygame.init()
WIDTH,HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Hangman Game!!")

#loading images
images = []
for i in range(6):
    image = pygame.image.load("./images/hangman" + str(i)+ ".png")
    images.append(image)

# game variables
hangman_status = 0 #for the image
words = ["SNAPE", "HARRY", "ALBUS", "RON", "LILLY"]
word = random.choice(words)
guessed = []

# button variables 
RADIUS = 20
GAP  = 15
letters = []
startX = round((WIDTH - (RADIUS * 2 + GAP)* 13)/2)
startY = 400
A = 65

for i in range(26):
    x = startX + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = startY + ((i // 13) * (GAP + 2 * RADIUS)) 
    letters.append([x,y,chr(A+i),True])

# Fonts
LETTER_FONT = pygame.font.SysFont('consolas', 30)
WORD_FONT = pygame.font.SysFont('consolas', 40)
TITLE_FONT = pygame.font.SysFont('consolas', 50)

def draw():
    win.fill(WHITE)

    #draw title
    text = TITLE_FONT.render("HARRY POTTER HANGMAN", 1, BLACK)
    win.blit(text, (int(WIDTH/2 - text.get_width()/2), 20))

    #draw word
    displayWord = ""
    for letter in word:
        if letter in guessed:
            displayWord += letter + " "
        else:
            displayWord += "_ "
    text = WORD_FONT.render(displayWord, 1, BLACK)
    win.blit(text, (400, 200))

    # Drawing letters
    for letter in letters:
        x, y, ltr, visible = letter
        if visible == True:
            pygame.draw.circle(win, BLACK, (x,y), RADIUS, 2)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (int(x - text.get_width()/2), int(y - text.get_height()/ 2)))

    if(hangman_status < 6):
        win.blit(images[hangman_status], (150,100))
    pygame.display.update()


#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
#setting up a loop
FPS = 60
clock = pygame.time.Clock()


def displayMessage(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (int(WIDTH/2 - text.get_width()/2), int(HEIGHT/2 - text.get_height()/2)))
    pygame.display.update()
    pygame.time.delay(3000)

run = True

while(run == True):
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            for letter in letters:
                x, y, ltr, visible = letter
                if visible :
                    dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                    if(dis < RADIUS): 
                        letter[3] = False
                        guessed.append(ltr)
                        if ltr not in word:
                            hangman_status += 1

    draw()

    won = True
    for ltr in word:
        if ltr not in guessed:
            won = False
            break

    if won:
        displayMessage("YOU WON !!")
        break 
    
    if hangman_status == 6:
        displayMessage("YOU LOST !!")
        break 

pygame.quit()

