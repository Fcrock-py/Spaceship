from pygame import *
from random import *

clock = time.Clock()
window = display.set_mode((1200, 700))

time.delay(1000)
fon = image.load('galaxy.jpg')
fon = transform.scale(fon, (1200, 700))

class Base(sprite.Sprite):
    def __init__(self, name, x, y, w=100, h=100):
        super().__init__()
        self.image = image.load(name)
        self.image = transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, self.rect)

class Player(Base):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d]:
            self.rect.x += 18
            if self.rect.x > 1220:
                self.rect.x = 0
        if keys[K_a]:
            self.rect.x -= 18
            if self.rect.x < -20:
                self.rect.x = 1200
    def shoot(self):
        global score
        shot.play()
        if score < 10:
            b1 = Bullet('bullet.png', self.rect.x+40, self.rect.y+5, 20, 20)
            fire.add(b1)
        elif score < 20:
            b1 = Bullet('bullet.png', self.rect.x+10, self.rect.y+5, 20, 20)
            b2 = Bullet('bullet.png', self.rect.x+30, self.rect.y+5, 20, 20)
            fire.add(b1, b2)
        elif score < 30:
            b1 = Bullet('bullet.png', self.rect.x, self.rect.y+5, 20, 20)
            b2 = Bullet('bullet.png', self.rect.x+20, self.rect.y+5, 20, 20)
            b3 = Bullet('bullet.png', self.rect.x+40, self.rect.y+5, 20, 20)
            fire.add(b1, b2, b3)
        else:
            b1 = Bullet('bullet.png', self.rect.x+40, self.rect.y+5, 100, 50)
            fire.add(b1)

class Bullet(Base):
    def update(self):
        self.rect.y -= 30
        if self.rect.y < 0:
            fire.remove(self)

class Vrag(Base):
    def update(self):
        global health
        global score
        if score < 10:
            self.rect.y += 4
        elif score < 20:
            self.rect.y += 5
        else:
            self.rect.y += 6
        if self.rect.y >= 790:
            self.rect.y = -25
            self.rect.x = randint(0, 1150)
            health -= 1
        if sprite.spritecollide(self, fire, True):
            self.rect.y = -25
            self.rect.x = randint(0, 1150)
            score += 1
        if sprite.collide_rect(self, hero):
            health -= 1
            self.rect.y = -25
            self.rect.x = randint(0, 1150)

class Asteroid(Base):
    def update(self):
        global health
        self.rect.y += 5
        if self.rect.y >= 790:
            self.rect.y = -25
            self.rect.x = randint(0, 1150)
            health -= 1
        if sprite.collide_rect(self, hero):
            health -= 1
            self.rect.y = -20
            self.rect.x = randint(0, 1150)
        if sprite.spritecollide(self, fire, True):
            self.rect.y = -25
            self.rect.x = randint(0, 1150)
            global score
            score += 2

class Boss(Base):
    def start_hp(self):
        self.hp = 25
        self.side = 4
    def update(self):
        self.rect.x += self.side
        if self.rect.x < 100 or self.rect.x > 900:
            self.side = - self.side

        self.rect.y += 0.5
        if self.rect.y >= 790 or sprite.collide_rect(self, hero):
            global health
            health = 0
        if sprite.spritecollide(self, fire, True):
            self.hp -= 1

v1 = Vrag("asteroid.png", randint(0, 1150), -50, 50, 50)
v2 = Vrag("asteroid.png", randint(0, 1150), -50, 50, 50)
v3 = Vrag("asteroid.png", randint(0, 1150), -50, 50, 50)
hero = Player('rocket.png', 550, 600, 100, 100)
fire = sprite.Group()
vrags = sprite.Group()
vrags.add(v1, v2, v3)
boss = Boss("asteroid.png", 300, -200, 500, 500)
boss.start_hp()
a1 = Asteroid('asteroid.png', randint(0, 1150), -50, 50, 50)
a2 = Asteroid('asteroid.png', randint(0, 1150), -50, 50, 50)

health = 7
score = 0

font.init()
shrift = font.Font(None, 35)

mixer.init()
shot = mixer.Sound('fire.ogg')

#mixer.music.load('andan.mp3')
#mixer.music.play(-1)

while health > 0:
    for e in event.get():
        if e.type == QUIT:
            quit()
            exit()
        if e.type == MOUSEBUTTONDOWN:
            hero.shoot()

    window.blit(fon, (0, 0))  
    hero.update()
    hero.reset()

    fire.update()
    fire.draw(window)

    health_txt = shrift.render('Здоровье : '+str(health), 1, (255,0,0))
    window.blit(health_txt, (0,0))

    score_txt = shrift.render('Очки : '+str(score), 1, (255,0,0))
    window.blit(score_txt, (0,20))

    if score >= 50:
        boss.update()
        boss.reset()
        a1.reset()
        a1.update()
        a2.reset()
        a2.update()
        if boss.hp <= 0:
            shrift_max = font.Font(None, 100)
            window.blit(fon, (0,0))
            winchik = shrift_max.render('ПОБЕДА!', 1, (255,0,0))
            score_txt = shrift_max.render('Очки : '+str(score), 1, (255,0,0))
            ess = shrift_max.render('Харооооооош', 1, (255,0,0))
            win = Base('kaif.jpg', 400, 100, 500, 200)
            win.update()
            win.reset()
            window.blit(winchik, (400, 300))
            window.blit(score_txt, (400, 370))
            window.blit(ess, (400, 450))
            display.update()
            time.delay(5000)
    else:
        vrags.update()
        vrags.draw(window)

    display.update()
    clock.tick(60)

shrift_max = font.Font(None, 100)

window.blit(fon, (0,0))
end = shrift_max.render('ПОРАЖЕНИЕ(', 1, (255,0,0))
score_txt = shrift_max.render('Очки : '+str(score), 1, (255,0,0))
puf = shrift_max.render('Не вешай нос,иди играй', 1, (255,0,0))
proigral = Base('proigral.jpg', 400, 100, 500, 200)
proigral.update()
proigral.reset()
window.blit(end, (400, 300))
window.blit(score_txt, (400, 370))
window.blit(puf, (200, 450))
display.update()
time.delay(4000)