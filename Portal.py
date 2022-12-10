import pygame
import setting

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('image/exitfromlevel.png')
        self.image = pygame.transform.scale(image, (setting.tile_size, int(setting.tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y