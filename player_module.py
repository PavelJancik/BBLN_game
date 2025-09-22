import pygame as pg
from constants import SCREEN_WIDTH, GROUND_Y

class Player(pg.sprite.Sprite):
    def __init__(self, w, h):
        super().__init__()
        player_surface = pg.image.load('imgs/pavel.png').convert_alpha()
        player_surface = pg.transform.scale(player_surface, (w, h))
        self.image = player_surface 
        self.rect = pg.Rect(0, GROUND_Y, w, h) # self.image.get_rect(midbottom = (0,0))
        self.gravity = 0        

    def player_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] and self.rect.bottom >= GROUND_Y:
            self.jump()
        if keys[pg.K_RIGHT]:
            self.move_right()
        if keys[pg.K_LEFT]:
            self.move_left()
        if keys[pg.K_SPACE]:
            self.attack()
            

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity            
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y

    def jump(self):
        self.gravity = -20

    def move_right(self):
        if self.rect.right <= SCREEN_WIDTH:
            self.rect.x += 4

    def move_left(self):
        if self.rect.left >= 0:
            self.rect.x -= 4

    def attack():
        print('attack todo')


    def update(self):
        self.player_input()
        self.apply_gravity()

    
