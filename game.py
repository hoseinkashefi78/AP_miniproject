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
        super().__init__(filename, randint(0, 750), randint(0, 550))

class Player2(Player):
    def __init__(self, filename):
        super().__init__(filename, randint(0, 750), randint(0, 550))

class Target:
    def __init__(self, filename, x, y):
        self.image = Image(filename, 50, 50).load()
        self.positions = [x, y]

    def generate_positions(self):
        self.positions = [randint(0, 750), randint(0, 550)]

    def draw(self, screen):
        screen.blit(self.image, (self.positions[0], self.positions[1]))

class SpecialTarget(Target):
    def __init__(self, number):
        if number == 1:
            filename = "ice-cubes.png"
        elif number == 2:
            filename = "hypnosis.png"
        elif number == 3:
            filename = "ammunition.png"
        super().__init__(filename, randint(0, 750), randint(0, 550))
        self.number = number
        self.active = False
        self.start_time = 0

    def activate(self):
        self.active = True
        self.start_time = time.time()

    def draw_special(self, screen):
        if self.active:
            self.draw(screen)
            if time.time() - self.start_time >= 5:  
                self.active = False

def shooting(player, poppet):
    if poppet.positions and abs(player.positions[0] - poppet.positions[0]) <= 20 and abs(player.positions[1] - poppet.positions[1]) <= 20:
        player.shoots.append(poppet.positions)
        if len(player.shoots) < 2:
            player.score += 1
        else:
            score = (sqrt((player.shoots[-1][0] - player.shoots[-2][0])**2 + (player.shoots[-1][1] - player.shoots[-2][1])**2)) // 100
            if score == 0:
                score += 1
            player.score += score
        print(player.score)
        poppet.generate_positions()

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game")
font = pygame.font.Font(None, 36)

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
player1 = Player1("focus.png")
player2 = Player2("focus2.png")
poppet1 = Target("dog.png", randint(0, 750), randint(0, 550))
poppet2 = Target("dog.png", randint(0, 750), randint(0, 550))
poppet3 = Target("dog.png", randint(0, 750), randint(0, 550))

last_power_time = time.time()
special = None
running = True
while running:
    screen.fill((255, 255, 255))  

    current_time = time.time()
    if current_time - last_power_time >= 10:  
        special = SpecialTarget(randint(1, 3))
        special.activate()
        last_power_time = current_time

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
                pygame.mixer.music.load("kesafat.mp3")
                pygame.mixer.music.play()
                shooting(player1, poppet1)
                shooting(player1, poppet2)
                shooting(player1, poppet3)
            if event.key == pygame.K_w:
                player2.y_change = -0.2
            if event.key == pygame.K_s:
                player2.y_change = 0.2
            if event.key == pygame.K_a:
                player2.x_change = -0.2
            if event.key == pygame.K_d:
                player2.x_change = 0.2
            if event.key == pygame.K_TAB:
                pygame.mixer.music.load("bishor.mp3")
                pygame.mixer.music.play()
                shooting(player2, poppet1)
                shooting(player2, poppet2)
                shooting(player2, poppet3)

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                player1.y_change = 0
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player1.x_change = 0
            if event.key in [pygame.K_w, pygame.K_s]:
                player2.y_change = 0
            if event.key in [pygame.K_a, pygame.K_d]:
                player2.x_change = 0

    player1.move()
    player2.move()
    player1.draw(screen)
    player2.draw(screen)
    poppet1.draw(screen)
    poppet2.draw(screen)
    poppet3.draw(screen)

    if special:
        special.draw_special(screen)  

    score1_text = font.render(f"Player1 Score: {int(player1.score)}", True, (0, 0, 0))
    screen.blit(score1_text, (600, 20))
    score2_text = font.render(f"Player2 Score: {int(player2.score)}", True, (0, 0, 0))
    screen.blit(score2_text, (600, 45))
    pygame.display.update()

pygame.quit()
