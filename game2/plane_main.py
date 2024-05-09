import pygame
from plane_sprites import *


class PlaneGame(object):
    """main game"""

    def __init__(self):
        print("Initializing")

        # create window
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # create time
        self.clock = pygame.time.Clock()
        # create sprites
        self.__create_sprites()
        # create enemy
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)

    def __create_sprites(self):
        """create sprites"""
        # create background
        bg1 = Background()
        bg2 = Background(True)
        bg2.rect.y = -bg2.rect.height
        self.back_group = pygame.sprite.Group(bg1, bg2)
        # create enemy group
        self.enemy_group = pygame.sprite.Group()
        # create player's plane
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        print("Game Starting...")
        while True:
            # set the frame
            self.clock.tick(FRAME_PER_SEC)
            # handle event
            self.__event_handle()
            # check collide
            self.__check_collide()
            # update sprites
            self.__update_sprites()
            # update display
            pygame.display.update()

    def __event_handle(self):
        """handle event"""

        for event in pygame.event.get():
            # check if game is over
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            # check if enemy is creating 
            elif event.type == CREATE_ENEMY_EVENT:
                print("Enemy appers...")
                # create enemy
                enemy = Enemy()
                self.enemy_group.add(Enemy())
            # player's plane shoots
            elif event.type == Hero_FIRE_EVENT:
                self.hero.fire()
        # get movement from the user
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        else:
            self.hero.speed = 0

    def __check_collide(self):
        """Check Crushing"""
        # destorying enemy 
        pygame.sprite.groupcollide(self.hero.bullets,
                                   self.enemy_group, True, True)
        # player's plane got destoryed
        enemies = pygame.sprite.spritecollide(self.hero,
                                              self.enemy_group, True)
        # check enemy
        if len(enemies) > 0:
            # player's plane killed
            self.hero.kill()
            # gameover
            PlaneGame.__game_over()

    def __update_sprites(self):
        """update sprites"""
        # update background display
        self.back_group.update()
        self.back_group.draw(self.screen)
        # 2.update enemy display
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        # 3.update player's plane display
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        # update bullet display
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod
    def __game_over():
        """gameover"""
        print("The Game is OVER")
        pygame.quit()
        exit()


if __name__ == '__main__':
    # create game
    game = PlaneGame()
    # start game
    game.start_game()
