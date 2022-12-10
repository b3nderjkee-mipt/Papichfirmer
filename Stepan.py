import pygame
import setting

class Stepan(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('image/coin.png')
        self.image = pygame.transform.scale(image, (setting.tile_size // 1.5, setting.tile_size // 1.5))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)