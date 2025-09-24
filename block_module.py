import pygame as pg

class Block(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, move_step):
        super().__init__()
        self.image = pg.Surface((w, h))
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.move_step = move_step
       

    def block_input(self):
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
        self.block_input()
 
        
        