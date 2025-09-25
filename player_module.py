import pygame as pg
from config import SCREEN_WIDTH, GROUND_Y

def load_frames(sheet_path, frame_width, frame_height, num_frames):
    sheet = pg.image.load(sheet_path).convert_alpha()
    frames = []
    for i in range(num_frames):
        frame = sheet.subsurface(pg.Rect(
            i * frame_width, 0, frame_width, frame_height
        ))
        frames.append(frame)
    return frames

class Player(pg.sprite.Sprite):
    def __init__(self, w, h):
        super().__init__()        
        frames = load_frames('imgs/char.png', 100, 100, 3)
        self.frames = frames  
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH / 2, GROUND_Y))
        self.animation_speed = 0.15 
        self.counter = 0
        
        # vertikalni pohyb
        self.vel_y = 0
        self.gravity_force = 1
        self.on_ground = False  

        self.jump_sound = pg.mixer.Sound('audio/sounds_effects/jump_sound.wav')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] and self.on_ground:
            self.jump()
        if keys[pg.K_DOWN] and self.on_ground:
            self.rect.y += 1
        if keys[pg.K_SPACE]:
            self.attack()

    def jump(self):
        self.vel_y = -20
        self.on_ground = False
        self.jump_sound.play()

    def attack(self):
        print("attack todo")

    def handle_collisions(self, blocks):
        # vertikalni pohyb
        self.rect.y += self.vel_y
        hits = pg.sprite.spritecollide(self, blocks, False)

        self.on_ground = False  # reset před kontrolou
        for block in hits:
            # kolize jen pokud hrac pada dolu a je nad blokem
            if self.vel_y > 0 and self.rect.bottom - self.vel_y <= block.rect.top:
                self.rect.bottom = block.rect.top
                self.vel_y = 0
                self.on_ground = True

        # země jako pojistka
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.vel_y = 0
            self.on_ground = True

    def animate_walk(self, flip):
        self.counter += self.animation_speed
        if self.counter >= len(self.frames):
            self.counter = 0
        self.index = int(self.counter)
        self.image = pg.transform.flip(self.frames[self.index], True, False) if flip else self.frames[self.index] 
   
    def update(self, blocks):
        self.player_input()
        self.vel_y += self.gravity_force 
        self.handle_collisions(blocks)
        # animations
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.animate_walk(False)         
        if keys[pg.K_LEFT]:
            self.animate_walk(True)   
        
