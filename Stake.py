import pygame
import setting

class Stake(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('image/stake.png')
        self.image = pygame.transform.scale(image, (setting.tile_size, setting.tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y