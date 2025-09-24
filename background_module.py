import pygame as pg
from config import SCREEN_WIDTH

class Background(pg.sprite.Sprite):
    def __init__(self, img, x, y, w, h, move_step):
        super().__init__()
        bg_surface = pg.image.load('imgs/' + img).convert_alpha()
        if w and h:
            bg_surface = pg.transform.scale(bg_surface, (w, h))
            self.rect = pg.Rect(x, y, w, h) 
        else:
            self.rect = bg_surface.get_rect(topleft = (x, y))
        self.image = bg_surface 
        self.move_step = move_step


    def bg_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.move_right()
        if keys[pg.K_LEFT]:
            self.move_left()

    def move_right(self):        
        self.rect.x -= self.move_step

    def move_left(self):        
        self.rect.x += self.move_step

    def update(self):
        self.bg_input()