import pygame
from random import randint
import time
from math import sqrt
class Image:
    def __init__(self, filename, width, height):
        self.filename = filename
        self.width = width
        self.height = height

    def load(self):
        image_load = pygame.image.load(self.filename)
        return pygame.transform.scale(image_load, (self.width, self.height))

class Player:
    def __init__(self, filename, x, y):
        self.image = Image(filename, 50, 50).load()
        self.positions = [x, y]
        self.x_change = 0
        self.y_change = 0
        self.score = 0
        self.shoots = []
    def move(self):
        self.positions[0] += self.x_change
        self.positions[1] += self.y_change

    def draw(self, screen):
        screen.blit(self.image, (self.positions[0], self.positions[1]))

class Player1(Player):
    def __init__(self, filename):
        super().__init__(filename, randint(0,750), randint(0,550))

class Player2(Player):
    pass

class Poppet:
    def __init__(self, filename , x, y):
        self.image = Image(filename, 50, 50).load()
        self.positions = [x, y]
    def generate_positions(self):
        if len(self.positions) < 1:
            self.positions.append(randint(0, 750))
            self.positions.append(randint(0, 550))
    def draw(self, screen):
        screen.blit(self.image , (self.positions[0], self.positions[1]))

def shooting(player,poppet):
    if abs(player.positions[0] - poppet.positions[0]) <= 20 and abs(player.positions[1] - poppet.positions[1]) <= 20:
        player.shoots.append(poppet.positions)
        if len(player.shoots) < 2:
            player.score += 1
        else:
            score = (sqrt((player.shoots[-1][0] - player.shoots[-2][0])**2 + (player.shoots[-1][1] - player.shoots[-2][1])**2))//100
            if score == 0:
                score +=1
            player.score += score 
        print(player.score)
        poppet.positions = []
        poppet.generate_positions()

# initialize the pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game")
font = pygame.font.Font(None, 36)

#images and musics
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
player1 = Player1("focus.png")
poppet1 = Poppet("dog.png" , randint(0,750), randint(0,550))
poppet2 = Poppet("dog.png" , randint(0,750), randint(0,550))
poppet3 = Poppet("dog.png" , randint(0,750), randint(0,550))

pygame.mixer.music.load("kesafat.mp3")

# game loop
running = True
while running:
    screen.fill((255, 255, 255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player1.y_change = -0.2
            if event.key == pygame.K_DOWN:
                player1.y_change = 0.2
            if event.key == pygame.K_LEFT:
                player1.x_change = -0.2
            if event.key == pygame.K_RIGHT:
                player1.x_change = 0.2
            if event.key == pygame.K_RETURN:
                pygame.mixer.music.play()
                shooting(player1, poppet1)
                shooting(player1, poppet2)
                shooting(player1, poppet3)
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                player1.y_change = 0
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player1.x_change = 0

    player1.move()

    player1.draw(screen)
    poppet1.draw(screen)
    poppet2.draw(screen)
    poppet3.draw(screen)

    score_text = font.render(f"Payer1 Score: {int(player1.score)}", True, (0, 0, 0))
    screen.blit(score_text, (600, 20))

    pygame.display.update()

pygame.quit()

