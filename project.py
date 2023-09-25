import pygame
import time
import random

window = pygame.display.set_mode((1000, 700))
wind_len = 1000
wind_heig = 700

jewish = pygame.image.load('lucky_fb2.jpg')
jewish = pygame.transform.scale(jewish, (1000, 700))

background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (1000, 700))

win_pic = pygame.image.load('thumb_1.jpg')
win_pic = pygame.transform.scale(win_pic, (1000, 700))

lose_pic = pygame.image.load('game-over_2.png')
lose_pic = pygame.transform.scale(lose_pic, (1000, 700))

pygame.display.set_caption('LEAT')

game = True
finish = False

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Wall(GameSprite):
    def stk(self):
        a = True

class Player(GameSprite):
    def __init__(self, picture, w, h, x, y, vel_x, vel_y, move = 0):
        super().__init__(picture, w, h, x, y)
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.move = move
    def shivup(self):
        if self.rect.y - self.vel_y + 13 >= 0:
            self.rect.y -= self.vel_y
    def shivdown(self):
        if self.rect.y + self.vel_y + 65 <= wind_heig:
            self.rect.y += self.vel_y
    def shivleft(self):
        if self.rect.x - self.vel_x >= 0:
            self.rect.x -= self.vel_x
    def shivright(self):
        if self.rect.x + self.vel_x + 80 <= wind_len:
            self.rect.x += self.vel_x
    def shoot(self):
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            x = pos[0] - self.rect.x
            y = pos[1] - self.rect.y
            sina = y / ((x ** 2 + y ** 2) ** 0.5)
            cosa = x / ((x ** 2 + y ** 2) ** 0.5)
            vel = 30
            ball = Ball('football.png', 15, 15, self.rect.x + 25, self.rect.y + 25, vel * cosa, vel * sina)
            balls.add(ball)
        

class Ball(GameSprite):
    def __init__(self, picture, w, h, x, y, vel_x, vel_y):
        super().__init__(picture, w, h, x, y)
        self.vel_x = vel_x
        self.vel_y = vel_y
    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if not (0 <= self.rect.x <= 1000 and 0 <= self.rect.y <= 700):
            self.kill()
        window.blit(self.image, (self.rect.x, self.rect.y))

balls = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemy_move = [0] * 6

hero = Player('ufo_3.png', 40, 40, 100, 150, 20, 10)
hero.reset()

enemy1 = Player('ufo_4.png', 40, 40, 200, 250, 10, 10)
enemy1.reset()
enemies.add(enemy1)

enemy2 = Player('ufo_4.png', 40, 40, 400, 450, 10, 10)
enemy2.reset()
enemies.add(enemy2)

enemy3 = Player('ufo_4.png', 40, 40, 40, 250, 10, 10)
enemy3.reset()
enemies.add(enemy3)

enemy4 = Player('ufo_4.png', 40, 40, 320, 60, 10, 10)
enemy4.reset()
enemies.add(enemy4)

enemy5 = Player('ufo_4.png', 40, 40, 500, 250, 10, 10)
enemy5.reset()
enemies.add(enemy5)

enemy6 = Player('ufo_4.png', 40, 40, 700, 450, 10, 10)
enemy6.reset()
enemies.add(enemy6)

window.blit(background, (0, 0))

timeshoot = time.time()
timechange = time.time()

while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
    if pygame.key.get_pressed()[pygame.K_w]:
        hero.shivup()
    if pygame.key.get_pressed()[pygame.K_s]:
        hero.shivdown()
    if pygame.key.get_pressed()[pygame.K_a]:
        hero.shivleft()
    if pygame.key.get_pressed()[pygame.K_d]:
        hero.shivright()
    if ((time.time() - timeshoot) >= 0.2):
        hero.shoot()
        timeshoot = time.time()

    if not finish:
        window.blit(background, (0, 0))

        balls.update()

        if len(enemies) == 0:
            finish = True
            window.blit(win_pic, (0, 0))
        
        for enemy in enemies:
            if int(time.time() - timechange) >= 0.25:
                enemy.move = random.randint(0, 3)
            move = enemy.move
            if move == 0:
                if enemy.rect.y + enemy.vel_y + 65 > wind_heig:
                    enemy.move = 3
                enemy.shivdown()
            if move == 1:
                if enemy.rect.x - enemy.vel_x < 0:
                    enemy.move = 2
                enemy.shivleft()
            if move == 2:
                if enemy.rect.x + enemy.vel_x + 80 > wind_len:
                    enemy.move = 1
                enemy.shivright()
            if move == 3:
                if enemy.rect.y - enemy.vel_y + 13 < 0:
                    enemy.move = 0
                enemy.shivup()
            enemy.reset()
        if int(time.time() - timechange) >= 0.25:
                timechange = time.time()
                
                
        hero.reset()

        if len(pygame.sprite.spritecollide(hero, enemies, False)) != 0:
            finish = True
            window.blit(lose_pic, (0, 0))
        for enemy in enemies:
            if len(pygame.sprite.spritecollide(enemy, balls, False)) != 0:
                enemy.kill()

    pygame.time.delay(30)
    pygame.display.update()