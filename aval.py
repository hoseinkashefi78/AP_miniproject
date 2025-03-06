import pygame
from random import randint
class image:
    pass  
class player:
    pass
class player1(player):
    pass
class player2(player):
    pass
class poppet:
    pass

class shooting():
    pass


# initialize the pygame
pygame.init()
pygame.mixer.init()
player_image_load = pygame.image.load("focus.png")
player_image = pygame.transform.scale(player_image_load, (50, 50))

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Game")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
pygame.mixer.music.load("kesafat.mp3")

playerx = randint(0,750)
playery = randint(0,550)
x_change = 0
y_change = 0
def play (x, y):
    screen.blit(player_image, (x, y))


running = True

while running:
    for event in pygame.event.get():
        screen.fill((255, 255, 255))
        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                y_change -= 0.1
            if event.key == pygame.K_DOWN:
                y_change += 0.1
            if event.key == pygame.K_LEFT:
                x_change -= 0.1
            if event.key == pygame.K_RIGHT:
                x_change += 0.1
            if event.key == pygame.K_SPACE:
                pygame.mixer.music.play()           
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_change = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                x_change = 0

    screen.fill((255, 255, 255))

    playerx += x_change
    playery += y_change
    play(playerx, playery)
    
    pygame.display.update()

pygame.quit()