import pygame as pg
from sys import exit
import player_module
import background_module
import block_module
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_Y, TOP_LAYER_SPEED, BOTTOM_LAYER_SPEED
 
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Babyløn')
clock = pg.time.Clock()

player = pg.sprite.GroupSingle()
player.add(player_module.Player(100,100))

top_layer = pg.sprite.Group()
top_layer.add(background_module.Background('ground.png', 0, GROUND_Y - 25, 0, 0, TOP_LAYER_SPEED))

bottom_layer = pg.sprite.GroupSingle()
bottom_layer.add(background_module.Background('sky.png', 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 1))

font = pg.font.Font('fonts/Tiny5/Tiny5-Regular.ttf', 50)
text_surface = font.render('Hello World!', False, '#efefef')
text_rect = text_surface.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

blocks = pg.sprite.Group(
    block_module.Block(0, 350, 600, 50, TOP_LAYER_SPEED),
    block_module.Block(600, 500, 100, 20, TOP_LAYER_SPEED),
    block_module.Block(400, 180, 100, 20, TOP_LAYER_SPEED),
)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.MOUSEBUTTONUP:
            print('clicked')
        
    bottom_layer.draw(screen)
    bottom_layer.update()

    player.draw(screen)
    player.update(blocks)

    top_layer.draw(screen)
    top_layer.update()

    blocks.draw(screen)
    blocks.update()

    screen.blit(text_surface, text_rect)

    pg.display.update()
    clock.tick(60)