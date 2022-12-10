import pygame
import setting
import pickle
from os import path
from Stepan import Stepan
from World import World



class Papich():
    def __init__(self, x, y, enemy, platform, stake, stepan, portal, world):
        self.reset(x, y)
        self._enemy = enemy
        self._platform = platform
        self._stake = stake
        self._stepan = stepan
        self._portal = portal
        self._world = world


    def position(self, game_over):
        dx = 0
        dy = 0
        col_thresh = 20

        if game_over == 0:

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                jump_music = pygame.mixer.Sound('sounds/eazy.wav')
                jump_music.set_volume(0.5)
                jump_music.play()
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]



            self.vel_y += 1
            if self.vel_y > 9.8:
                self.vel_y = 9.8
            dy += self.vel_y


            self.in_air = True


            for tile in self._world.tile_list:


                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0

                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False


            if pygame.sprite.spritecollide(self, self._enemy, False):
                game_over = -1
                game_over_fx = pygame.mixer.Sound('sounds/game_over.wav')
                game_over_fx.set_volume(0.5)
                game_over_fx.play()


            if pygame.sprite.spritecollide(self, self._stake, False):
                game_over = -1
                game_over_fx = pygame.mixer.Sound('sounds/game_over.wav')
                game_over_fx.set_volume(0.5)
                game_over_fx.play()


            if pygame.sprite.spritecollide(self, self._portal, False):
                game_over = 1


            for platform in self._platform:

                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top

                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0

                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            self.rect.x += dx
            self.rect.y += dy


        elif game_over == -1:


            img = pygame.font.SysFont('Impact', 70).render('YOU LOST!', True, setting.Black)
            setting.screen.blit(img, ((setting.Width // 2) - 200, setting.Height // 2))

            if self.rect.y > 200:
                self.rect.y -= 5

        setting.screen.blit(self.image, self.rect)

        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load('image/papich.png')
            img_right = pygame.transform.scale(img_right, (30, 50))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

    def reset_level(self, level):
        self._enemy.empty()
        self. _platform.empty()
        self._stepan.empty()
        self._stake.empty()
        self._portal.empty()

        if path.exists(f'lvls/level{level}_data'):
            open_file = open(f'lvls/level{level}_data', 'rb')
            data = pickle.load(open_file)
        self._world = World(data, self._enemy, self._platform, self._stake, self._stepan, self._portal)
        stepan = Stepan(setting.tile_size // 2, setting.tile_size // 2)
        self._stepan.add(stepan)
        return self._world