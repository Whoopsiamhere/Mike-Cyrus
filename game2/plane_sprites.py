import random
import pygame
# screen size
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# game frame
FRAME_PER_SEC = 60
# create enemy plane
CREATE_ENEMY_EVENT = pygame.USEREVENT
# plane shooting bullets
Hero_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """sprite base"""
    def __init__(self, image_name, speed=1):
        # initial 
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        # record speed
        self.speed = speed

    def update(self, *args):
        # moves horizontally
        self.rect.y += self.speed


class Background(GameSprite):
    """game background"""

    def __init__(self, is_alt=False):

        # use image named background.png
        image_name = "./images/background.png"
        super().__init__(image_name)
        # move the image to the top
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self, *args):

        super().update()
        # move to the top if out of the screen 
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """enemy plane"""
    def __init__(self):
        # create enemy planes using enemy1.png
        super().__init__("./images/enemy1.png")
        # set random enemy speed 
        self.speed = random.randint(1, 3)
        # random location and moves vertically
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self, *args):
        super().update()
        # delete enemy if out of the screen
        if self.rect.y >= SCREEN_RECT.height:
            print("enemy out of screen...")
        # delete 
            self.kill()

    def __del__(self):
        print("enemy dies　%s" % self.rect)


class Hero(GameSprite):
    """player's plane"""
    def __init__(self):
        super().__init__("./images/me1.png", 0)
        # set initial location
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        # fire bullets every 0.5s
        pygame.time.set_timer(Hero_FIRE_EVENT, 500)
        # create bullets
        self.bullets = pygame.sprite.Group()

    def update(self, *args):
        # moves horizontally
        self.rect.x += self.speed
        # set the boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        print("shooting bullets...")
        # 3 bullets each shooting
        for i in (1, 2, 3):
            # create bullets
            bullet = Bullet()
            # set bullets location
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx
            # add bullets to the sprite
            self.bullets.add(bullet)


class Bullet(GameSprite):
    """bullet"""
    def __init__(self):
        super().__init__("./images/bullet1.png", -2)

    def update(self, *args):
        super().update()
        # delete bullets when out of the screen
        if self.rect.bottom < 0:
            self.kill()
