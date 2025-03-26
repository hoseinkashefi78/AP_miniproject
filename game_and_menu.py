import pygame
import sys
from random import randint
import time
import copy
from math import sqrt

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
    icon = pygame.image.load('icon.png')
    pygame.display.set_icon(icon)
    selected = 0 
    pygame.mixer.music.load("kharabkardi.mp3")
    pygame.mixer.music.play()
    while True:
        screen.fill(WHITE)
        golzar = Image("golzar.jpg",800,600).load()
        screen.blit(golzar,(0,0))
        start_color = RED if selected == 0 else BLACK
        exit_color = RED if selected == 1 else BLACK
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
        self.points = []
        self.freezed = False
        self.freeze_end_time = 0
        self.hypnotized = False
        self.hypnosis_count  = 0 
        self.bullets = 10

    def move(self):
        self.positions[0] += self.x_change
        self.positions[1] += self.y_change

    def draw(self, screen):
        screen.blit(self.image, (self.positions[0], self.positions[1]))
    
    def activatefreeze(self):
        self.freezed = True
        self.start_freeze_time = time.time()
    def activatehypnosis(self):
        self.hypnotized = True
    def update(self):
        if self.freezed :
            if (time.time()-self.start_freeze_time) > 10 :
                self.freezed = False
        if self.hypnotized:
            if self.hypnosis_count == 3 :
                self.hypnotized = False
                self.hypnosis_count = 0

class Player1(Player):
    def __init__(self, filename):
        super().__init__(filename, randint(0, 750), randint(0, 550))
        self.pointer = Image("circle.png", 10, 10).load()
    def point (self , screen):  
        if len(self.points) >= 1 :
            screen.blit(self.pointer, (self.points[-1][0], self.points[-1][1]))
            if len(self.points) >= 2 :
                screen.blit(self.pointer, (self.points[-2][0], self.points[-2][1]))
                if len(self.points) >= 3 :
                    screen.blit(self.pointer, (self.points[-3][0], self.points[-3][1]))

class Player2(Player):
    def __init__(self, filename):
        super().__init__(filename, randint(0, 750), randint(0, 550))
        self.pointer = Image("record.png", 10, 10).load()
    def point (self , screen):  
        if len(self.points) >= 1 :
            screen.blit(self.pointer, (self.points[-1][0], self.points[-1][1]))
            if len(self.points) >= 2 :
                screen.blit(self.pointer, (self.points[-2][0], self.points[-2][1]))
                if len(self.points) >= 3 :
                    screen.blit(self.pointer, (self.points[-3][0], self.points[-3][1]))

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

def shooting(player, poppet , enemy):
    if poppet.positions and abs(player.positions[0] - poppet.positions[0]) <= 20 and abs(player.positions[1] - poppet.positions[1]) <= 20:
        player.shoots.append(poppet.positions)
        if len(player.points) < 2:
            player.score += 1
        else:
            score = (sqrt((player.points[-1][0] - player.points[-2][0])**2 + (player.points[-1][1] - player.points[-2][1])**2)) // 100
            if score == 0:
                score += 1
            if player.hypnotized == True :
                enemy.score += score
                player.hypnosis_count += 1
            else:
                player.score += score
        print(player.score)
        poppet.generate_positions() 

def ice(player, special, enemy):
    if special and special.number == 1 and abs(player.positions[0] - special.positions[0]) <= 20 and abs(player.positions[1] - special.positions[1]) <= 20:
        print("Ice hit!")
        enemy.activatefreeze()
        return None
    return special

def hypnosis(player, special, enemy):
    if special and special.number == 2 and abs(player.positions[0] - special.positions[0]) <= 20 and abs(player.positions[1] - special.positions[1]) <= 20:
        print("hypnosis hit!")
        enemy.activatehypnosis()
        return None
    return special

def ammu(player, special):
    if special and special.number == 3 and abs(player.positions[0] - special.positions[0]) <= 20 and abs(player.positions[1] - special.positions[1]) <= 20:
        print("ammu hit!")
        player.bullets += 5
        return None
    return special

def game_loop():
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

    game_start_time = time.time()

    while running:
        screen.fill((255, 255, 255))  

        current_time = time.time()
        if current_time - last_power_time >= 10:  
            special = SpecialTarget(randint(1,3))
            special.activate()
            last_power_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if not player1.freezed:
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
                        if player1.bullets > 0 :
                            p = copy.deepcopy(player1.positions)
                            pp = [p[0] + 20 , p[1] + 20]
                            player1.points.append(pp)
                            shooting(player1, poppet1 , player2)
                            shooting(player1, poppet2 , player2)
                            shooting(player1, poppet3 , player2)
                            player1.bullets -= 1
                            if special:
                                if ice(player1,special,player2) == None :
                                    special = None
                                if hypnosis(player1,special,player2) == None :
                                    special = None
                                if ammu(player1,special) == None :
                                    special = None
                if not player2.freezed:
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
                        if player2.bullets > 0 :
                            q = copy.deepcopy(player2.positions)
                            qq = [q[0] + 20 , q[1] + 20]
                            player2.points.append(qq)
                            shooting(player2, poppet1 , player1)
                            shooting(player2, poppet2 , player1)
                            shooting(player2, poppet3 , player1)
                            player2.bullets -= 1
                            if special:
                                if ice(player2,special,player1) == None :
                                    special = None
                                if hypnosis(player2,special,player1) == None :
                                    special = None
                                if ammu(player2,special) == None :
                                    special = None
                     

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    player1.y_change = 0
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    player1.x_change = 0
                if event.key in [pygame.K_w, pygame.K_s]:
                    player2.y_change = 0
                if event.key in [pygame.K_a, pygame.K_d]:
                    player2.x_change = 0
        player1.update()
        player2.update()
        player1.move()
        player2.move()
        player1.draw(screen)
        player2.draw(screen)
        poppet1.draw(screen)
        poppet2.draw(screen)
        poppet3.draw(screen)
        player1.point(screen)
        player2.point(screen)
        if special:
            special.draw_special(screen)

        game_time = time.time()  

        if 300 < (game_time - game_start_time) < 300.01 :
            running = False

        time_text = small_font.render(f"{int(300 - (game_time - game_start_time))}", True, (0, 0, 0))
        screen.blit(time_text, (400, 20))
        score1_text = small_font.render(f"Player1 Score: {int(player1.score)}", True, (0, 0, 0))
        screen.blit(score1_text, (600, 20))
        score2_text = small_font.render(f"Player2 Score: {int(player2.score)}", True, (0, 0, 0))
        screen.blit(score2_text, (600, 45))
        score1_text = small_font.render(f"Player1 Bullets: {int(player1.bullets)}", True, (0, 0, 0))
        screen.blit(score1_text, (20, 20))
        score2_text = small_font.render(f"Player2 Bullets: {int(player2.bullets)}", True, (0, 0, 0))
        screen.blit(score2_text, (20, 45))
        pygame.display.update()

if __name__ == "__main__":
    main_menu()
