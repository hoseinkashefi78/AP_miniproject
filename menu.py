import pygame
import sys
from random import randint
import time
import copy
from math import sqrt



# مقداردهی اولیه Pygame
pygame.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
RED = (255, 0, 0)

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    selected = 0 
    while True:
        screen.fill(BLACK)
        start_color = RED if selected == 0 else WHITE
        exit_color = RED if selected == 1 else WHITE
        draw_text("START", font, start_color, screen, WIDTH//2, HEIGHT//2)
        draw_text("EXIT", font, exit_color, screen, WIDTH//2, HEIGHT//2 + 100)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = 0
                elif event.key == pygame.K_DOWN:
                    selected = 1
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        game_loop() 
                    elif selected == 1:
                        pygame.quit()
                        sys.exit()
        pygame.display.update()




if __name__ == "__main__":
    main_menu()