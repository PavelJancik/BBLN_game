import pygame as pg
from config import MAX_CAMERA_X_DIVIDED_BY_SPEED

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

    def block_input(self, camera_x):
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.move_right(camera_x)
        if keys[pg.K_LEFT]:
            self.move_left(camera_x)

    # player is moving to the right, background is moving to the left
    def move_right(self, camera_x):
        if camera_x > -MAX_CAMERA_X_DIVIDED_BY_SPEED:
            self.rect.x -= self.move_step

    # player is moving to the left, background is moving to the right
    def move_left(self, camera_x):
        if camera_x < 0:
            self.rect.x += self.move_step

    def update(self, camera_x):
        self.block_input(camera_x)
 
        
        