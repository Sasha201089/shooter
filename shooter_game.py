#Создай собственный Шутер!
import pygame
import sys 
from time import time as timer
from random import *
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('space.ogg')
pygame.mixer.music.play()
screen = pygame.display.set_mode((700, 700))
game = 1
lost = 0
score = 0
def stop():
    pygame.quit()
    sys.exit()
class sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (65, 65))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speed = speed
    def output(self):
        screen.blit(self.image, self.rect)
class player(sprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < 630:
            self.rect.y += self.speed
    def fire(self):    
        bullet = vrag(self.rect.centerx + 30, self.rect.centery, -10, 'bullet.png')
        bullet.image = pygame.transform.scale(bullet.image, (15, 20))   
        bullets.add(bullet)
class vrag(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (65, 65))
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speed = speed
    def output(self):
        screen.blit(self.image, self.rect)
    def update(self, image):
        global lost
        self.rect.centery += self.speed
        if self.rect.centery >= 700:
            self.rect.centery = 0
            if image == 'ufo.png':
                lost += 1
            self.rect.centerx = randint(50, 650)
            self.speed = randint(1, 4)
bullets = pygame.sprite.Group()
meteors = pygame.sprite.Group()
bass = pygame.font.SysFont('Arial', 36)
vig = 0
proig = 0
rel_time = False
num_fire = 0
life = 3
heal = bass.render(str(life), 1, (255, 255, 255))
sch = bass.render('Пропущено:'+str(lost), 1, (255, 255, 255))
sch_rect = sch.get_rect(center=(100, 100))
sot = bass.render('Сбито:'+str(lost), 1, (255, 255, 255))
sot_rect = sot.get_rect(center=(100, 200))
vrags = pygame.sprite.Group()
hero = player(350, 350, 2, 'rocket.png')
fon = pygame.image.load('galaxy.jpg')
fon = pygame.transform.scale(fon, (700, 700))
fon_rect = fon.get_rect(center=(350, 350))
pule = pygame.mixer.Sound('fire.ogg')
win = bass.render('Победа!', 1, (255, 255, 255))
lose = bass.render('Проигрыш!', 1, (255, 255, 255))
for i in range(0, 5):
    vrags.add(vrag(randint(50, 650), 0, randint(1, 4), 'ufo.png'))
for h in range(0, 3):
    meteors.add(vrag(randint(50, 650), 0, randint(1, 4), 'asteroid.png'))
while True:
    screen.fill((255, 0, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if num_fire <= 5 and rel_time == False:
                    hero.fire()
                    pule.play()
                    num_fire += 1
                if num_fire > 5 and rel_time == False:
                    rel_time = True
                    last_time = timer()

    if game:
        sot = bass.render('Сбито:' + str(score), 1, (255, 255, 255))
        sch = bass.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        screen.blit(fon, fon_rect)
        hero.update()            
        hero.output()  
        meteors.update('met.png')
        bullets.update('l.png')
        vrags.update('ufo.png')
        vrags.draw(screen)
        meteors.draw(screen)
        bullets.draw(screen)
        screen.blit(sch, sch_rect)
        screen.blit(sot, sot_rect)
        screen.blit(heal, (650, 10))
        collide = pygame.sprite.groupcollide(vrags, bullets, True, True)
        collide2 = pygame.sprite.groupcollide(meteors, bullets, False, True)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:    
                relo = bass.render('Wait, reload...', 1, (150, 0, 0))
                screen.blit(relo, (260, 460))
            else:
                num_fire = 0
                rel_time = False   
        for i in collide:
            score += 1
            vrags.add(vrag(randint(50, 650), 0, randint(1, 5), 'ufo.png'))
        if score >= 10 or lost >= 5 or pygame.sprite.spritecollide(hero, vrags, False) or pygame.sprite.spritecollide(hero, meteors, False):
            if score >= 10:
                win_rect = win.get_rect(center=(350, 350))
                screen.blit(win, win_rect)
                score = 0
                lost = 0
                game = 0
                pygame.mixer.music.stop()
            else:
                if life == 0:
                    lose_rect = lose.get_rect(center=(350, 350))
                    screen.blit(lose, lose_rect)
                    score = 0
                    lost = 0
                    game = 0
                    pygame.mixer.music.stop()
                else:
                    life -= 1
                    heal = bass.render(str(life), 1, (255, 255, 255))
                    hero.rect.center = (350, 600)      
        pygame.display.update()   

