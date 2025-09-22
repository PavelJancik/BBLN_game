import pygame as pg
from sys import exit
import player_module
from constants import SCREEN_WIDTH, SCREEN_HEIGHT 

window = {
    "width": 1200,
    "height": 800
}

pg.init()
screen = pg.display.set_mode((1200, 800))
pg.display.set_caption('Babyløn')
clock = pg.time.Clock()

ground_surface = pg.image.load('imgs/ground.png').convert_alpha()
sky_surface = pg.image.load('imgs/sky.png').convert()
sky_surface = pg.transform.scale(sky_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))

 
player = pg.sprite.GroupSingle()
player.add(player_module.Player(100,100))

font = pg.font.Font('fonts/Tiny5/Tiny5-Regular.ttf', 50)
text_surface = font.render('Hello World!', False, '#efefef')
text_rect = text_surface.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
 
        # if event.type = pg.KEYUP:
        
    screen.blit(sky_surface, (0, 0))

    screen.blit(text_surface, text_rect)

    player.draw(screen)
    player.update()

    # if some_rectangle.colliderrect(another_rect):
        # do something
    
    
    mouse_pos = pg.mouse.get_pos() # (x, y)
    # some_rect.collidepoint(mouse_pos)
    # some_rect.collidepoint((x, y))
    mouse_pressed = pg.mouse.get_pressed() # [bool, bool, bool]
    
    # keys = pg.key.get_key_pressed()
 



    screen.blit(ground_surface, (0, 700))

    pg.display.update()
    clock.tick(60)