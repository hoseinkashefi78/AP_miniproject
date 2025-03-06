import pygame
from random import randint
class image:
    def __init__(self, filename , width, height):
        self.filename = filename
        self.width = width
        self.height = height
    def load(self,):
        image_load = pygame.image.load(self.filename)
        return(pygame.transform.scale(image_load, (self.width, self.height)))    
class player:
    pass
class player1(player):
    def play (x, y):
        screen.blit(player_image, (x, y))
class player2(player):
    pass
class poppet:
    def play (popet_positions):
        if len(poppet_positions) <= 3:
            for i in range(3):
                poppet_positions.append(randint(0,750))
                poppet_positions.append(randint(0,650))
        screen.blit(poppet_image, (poppet_positions[-2],poppet_positions[-1] ))
        screen.blit(poppet_image, (poppet_positions[-4],poppet_positions[-3] ))
        screen.blit(poppet_image, (poppet_positions[-6],poppet_positions[-5] ))

class shooting():
    pass
# initialize the pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Game")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
player_photo = image('focus.png',50,50)
player_image = image.load(player_photo)
poppet_photo = image("dog.png",50,50)
poppet_image = image.load(poppet_photo)
pygame.mixer.music.load("kesafat.mp3")
playerx = 300
playery = 300
playery_change = 0
playerx_change = 0
poppet_positions = []


running = True

while running:
    for event in pygame.event.get():
        screen.fill((255, 255, 255))
        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playery_change -= 0.1
            if event.key == pygame.K_DOWN:
                playery_change += 0.1
            if event.key == pygame.K_LEFT:
                playerx_change -= 0.1
            if event.key == pygame.K_RIGHT:
                playerx_change += 0.1
            if event.key == pygame.K_SPACE:
                pygame.mixer.music.play()           
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playery_change = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                playerx_change = 0
    
    playerx += playerx_change
    playery += playery_change
    screen.fill((255, 255, 255))
    player1.play(playerx, playery)
    poppet.play(poppet_positions)
    pygame.display.update()

pygame.quit()