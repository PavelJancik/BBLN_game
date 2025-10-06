import pygame as pg
import NPC_module
import hitbox_module
from config import SCREEN_WIDTH, GROUND_Y
import engine_module

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()                     
        self.frames =  engine_module.load_frames('imgs/char.png', 100, 200, 4, 75, 150)
        self.index = 0
        self.image = self.frames[self.index]                 
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH / 2, GROUND_Y))
        self.animation_speed = 0.15 
        self.counter = 0
        self.max_health = 100
        self.health = 100
        self.right_direction = True
        self.damage_range = self.rect.w / 2 + 80
        self.damage = 21
        self.attack_cooldown = 500
        self.last_attack = 0
        
        # vertikalni pohyb
        self.vel_y = 0
        self.gravity_force = 1
        self.on_ground = False  

        self.jump_sound = pg.mixer.Sound('audio/sounds_effects/jump_sound.wav')
        self.jump_sound.set_volume(0.5)

    def player_input(self, npcs):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] and self.on_ground:
            self.jump()
        if keys[pg.K_DOWN] and self.on_ground:
            self.rect.y += 1
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_attack >= self.attack_cooldown:
                self.attack(npcs)
                self.last_attack = now     
        if keys[pg.K_RIGHT]:
            self.right_direction = True
            self.animate_walk()         
        if keys[pg.K_LEFT]:
            self.right_direction = False
            self.animate_walk()

    def jump(self):
        self.vel_y = -20
        self.on_ground = False
        self.jump_sound.play()

    def attack(self, npcs):
        npcs_in_range = self.get_npcs_in_range(npcs)
        for zombie in npcs_in_range:
            zombie.health -= self.damage
            print(zombie.health)

    def get_npcs_in_range(self, group):
        result = []
        x1 = self.rect.centerx if self.right_direction else self.rect.centerx - self.damage_range
        x2 = self.rect.centerx + self.damage_range if self.right_direction else self.rect.centerx
        y = self.rect.centery
        y_dev = 10 # deviation
        for zombie in group:            
            if x1 <= zombie.rect.centerx <= x2 and zombie.rect.centery < y + y_dev and zombie.rect.centery > y - y_dev:
                result.append(zombie)
        return result         

    def handle_collisions(self, blocks, npcs):
        # vertikalni pohyb
        self.rect.y += self.vel_y
        hits_blocks = pg.sprite.spritecollide(self, blocks, False)
        hits_npcs = pg.sprite.spritecollide(self, npcs, False)
        hits = hits_blocks + hits_npcs

        self.on_ground = False  # reset před kontrolou
        for block in hits:
            # if isinstance(block, NPC_module.NPC): # tohle je kolize pouze shora, kolize z boku je resena v NPC_module
                # self.health -= block.damage
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

    def animate_walk(self):
        self.counter += self.animation_speed
        if self.counter >= len(self.frames):
            self.counter = 0
        self.index = int(self.counter)
        self.image = pg.transform.flip(self.frames[self.index], True, False) if not self.right_direction else self.frames[self.index] 
   
    def update(self, blocks, npcs):
        self.player_input(npcs)
        self.vel_y += self.gravity_force 
        self.handle_collisions(blocks, npcs)

        
