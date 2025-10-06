import pygame as pg

class Block(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, move_step, img):
        super().__init__()
        if img: 
            bg_surface = pg.image.load('imgs/' + img).convert_alpha()
            self.image = pg.transform.scale(bg_surface, (w, h))                        
        else:
            self.image = pg.Surface((w, h))
            self.image.fill('White')    
        self.rect = self.image.get_rect(topleft = (x, y))    
        self.move_step = move_step    

    def update(self, can_move_left, can_move_right):
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] and can_move_right:
            self.rect.x -= self.move_step
        if keys[pg.K_LEFT] and can_move_left:
            self.rect.x += self.move_step
 
        
        