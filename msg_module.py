import pygame as pg
from config import SCREEN_WIDTH

class Msg(pg.sprite.Sprite):
    def __init__(self, msg):
        super().__init__()
        self.full_text = msg
        self.curr_text = ''
        self.font = pg.font.Font('fonts/Tiny5/Tiny5-Regular.ttf', 20)
        self.speed = 50 # ms
        self.color = '#3e3e3e'
        self.index = 0
        self.last_update = pg.time.get_ticks()    
        self.image = self.font.render("", True, self.color)
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH / 2, 200))   

        
    def msg_completed(self):
        return self.full_text == self.curr_text  

    def update(self):
        now = pg.time.get_ticks()
        if self.index < len(self.full_text) and now - self.last_update > self.speed:
            self.index += 1
            self.curr_text = self.full_text[:self.index]
            self.image = self.font.render(self.curr_text, True, self.color)
            self.rect = self.image.get_rect(center = (SCREEN_WIDTH / 2, 200))
            self.last_update = now
