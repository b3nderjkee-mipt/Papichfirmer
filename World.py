import pygame
import setting
from Stake import Stake
from Stepan import Stepan
from Platform import Platform
from Enemy import Enemy
from Portal import Portal


class World():
    def __init__(self, data, blob, platform, stake, stepan, portal):
        self._blob = blob
        self._platform = platform
        self._stake = stake
        self._stepan = stepan
        self._portal = portal
        self.tile_list = []

        block_1 = pygame.image.load('image/block.png')
        block_2 = pygame.image.load('image/block_1.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(block_1, (setting.tile_size, setting.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * setting.tile_size
                    img_rect.y = row_count * setting.tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(block_2, (setting.tile_size, setting.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * setting.tile_size
                    img_rect.y = row_count * setting.tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count * setting.tile_size, row_count * setting.tile_size + 15)
                    self._blob.add(blob)
                if tile == 4:
                    platform = Platform(col_count * setting.tile_size, row_count * setting.tile_size, 1, 0)
                    self._platform.add(platform)
                if tile == 5:
                    platform = Platform(col_count * setting.tile_size, row_count * setting.tile_size, 0, 1)
                    self._platform.add(platform)
                if tile == 6:
                    stake = Stake(col_count * setting.tile_size, row_count * setting.tile_size + (setting.tile_size // 2))
                    self._stake.add(stake)
                if tile == 7:
                    stepan = Stepan(col_count * setting.tile_size + (setting.tile_size// 2), row_count * setting.tile_size + (setting.tile_size // 2))
                    self._stepan.add(stepan)
                if tile == 8:
                    portal = Portal(col_count * setting.tile_size, row_count * setting.tile_size - (setting.tile_size // 2))
                    self._portal.add(portal)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            setting.screen.blit(tile[0], tile[1])
