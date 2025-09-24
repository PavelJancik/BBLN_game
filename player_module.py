import pygame as pg
from config import SCREEN_WIDTH, GROUND_Y

class Player(pg.sprite.Sprite):
    def __init__(self, w, h):
        super().__init__()
        player_surface = pg.image.load('imgs/pavel.png').convert_alpha()
        player_surface = pg.transform.scale(player_surface, (w, h))
        self.image = player_surface 
        # self.rect = pg.Rect(SCREEN_WIDTH/2, GROUND_Y, w, h) # self.image.get_rect(midbottom = (0,0))
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH/2, GROUND_Y))
        self.vel_y = 0
        self.gravity_force = 1 
        self.on_ground = False 

    def player_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] and self.on_ground:
            self.jump()
        if keys[pg.K_SPACE]:
            self.attack()
            
    def apply_gravity(self):
        self.vel_y += self.gravity_force
        self.rect.y += self.vel_y
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.vel_y = 0 
            self.on_ground = True
        else:
            self.on_ground = False

    def jump(self):
        self.vel_y = -20
        self.on_ground = False

    def attack(self):
        print('attack todo')

    def update(self, blocks):
        self.player_input()
        self.apply_gravity()
        hits = pg.sprite.spritecollide(self, blocks, False)
        for block in hits:
            if self.vel_y > 0 and  self.rect.bottom <= block.rect.top + 10:
                self.rect.bottom = block.rect.top
                self.vel_y = 0
                self.on_ground = True
