import pygame as pg

class Hitbox(pg.sprite.Sprite):
    def __init__(self, npc, w, h):
        super().__init__()          
        self.rect = pg.Rect(0,0,w,h)
        self.rect.center = npc.rect.center        

    def update(self, npc):
        self.rect.center = npc.rect.center        