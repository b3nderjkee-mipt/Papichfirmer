import pygame
import pickle
from os import path
import setting
from Stepan import Stepan
from World import World
from Buttons import Buttons
from Papich import Papich

pygame.init()

clock = pygame.time.Clock()
fps = 60

pygame.display.set_caption('Papichformer')

game_text = pygame.font.SysFont('Impact', 70)
score_text = pygame.font.SysFont('Impact ', 25)

game_over = 0
menu = True
level = 1
max_levels = 4
score = 0

backround = pygame.image.load('image/cloud.png')
restart_im = pygame.transform.scale(pygame.image.load('image/r.png'), (100, 70))
start_im = pygame.image.load('image/s.png')
quit_im = pygame.transform.scale(pygame.image.load('image/q.png'), (330, 170))

pygame.mixer.music.load('sounds/music.mp3')
pygame.mixer.music.play(-1, 0.0, 0)
stepan_music = pygame.mixer.Sound('sounds/stepan.wav')
stepan_music.set_volume(0.5)


enemy_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
stakes_group = pygame.sprite.Group()
stepan_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()

stepan = Stepan(setting.tile_size // 2, setting.tile_size // 2)
stepan_group.add(stepan)

if path.exists(f'lvls/level{level}_data'):
    open_file = open(f'lvls/level{level}_data', 'rb')
    data = pickle.load(open_file)

world = World(data, enemy_group, platform_group, stakes_group, stepan_group, portal_group)
papich = Papich(40, setting.Height - 150, enemy_group, platform_group,
                stakes_group, stepan_group, portal_group, world)
# create buttons
restart_button = Buttons(setting.Width // 2 - 150, setting.Height //2 - 70, restart_im)
start_button = Buttons(setting.Width // 2 - 150, setting.Height //2 - 70, start_im)
exit_button = Buttons(setting.Width // 2 - 150, setting.Height // 2 + 50, quit_im)

run = True
while run:

    clock.tick(fps)

    setting.screen.blit(backround, (0, 0))

    if menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            menu = False
    else:
        world.draw()

        if game_over == 0:
            enemy_group.update()
            platform_group.update()

            if pygame.sprite.spritecollide(papich, stepan_group, True):
                score += 1
                stepan_music.play()
            setting.screen.blit(score_text.render(': ' + str(score), True, setting.White),
                                (setting.tile_size, 0))

        enemy_group.draw(setting.screen)
        platform_group.draw(setting.screen)
        stakes_group.draw(setting.screen)
        stepan_group.draw(setting.screen)
        portal_group.draw(setting.screen)

        game_over = papich.position(game_over)

        if game_over == -1:
            if restart_button.draw():
                data = []
                papich.reset(40, setting.Height - 150)
                world = papich.reset_level(level)
                game_over = 0
                score = 0

        if game_over == 1:
            level += 1
            if level <= max_levels:
                data = []
                papich.reset(40, setting.Height - 150)
                world = papich.reset_level(level)
                game_over = 0
            else:
                setting.screen.blit(game_text.render('VI KA!', True, setting.Black),
                                ((setting.Width // 2) - 140, setting.Height // 2 - 100))


                if exit_button.draw():
                    run = False


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()