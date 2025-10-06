import pygame as pg
from config import GROUND_Y
import random
import time
import hitbox_module


class NPC(pg.sprite.Sprite):
    def __init__(self, x):
        super().__init__()   
        sex = 'male' if bool(random.getrandbits(1)) else 'female'
        walk_frames = []        
        for i in range(1, 10):
            img = pg.image.load(f"imgs/zombie/{sex}/Walk ({i}).png").convert_alpha()           
            img = pg.transform.scale(img, (3*43,3*52))
            walk_frames.append(img)
        attack_frames = []
        for i in range(1, 8):
            img = pg.image.load(f"imgs/zombie/{sex}/Attack ({i}).png").convert_alpha()
            img = pg.transform.scale(img, (3*43,3*52))
            attack_frames.append(img)
        dead_frames = []
        for i in range(1, 12):
            img = pg.image.load(f"imgs/zombie/{sex}/Dead ({i}).png").convert_alpha()
            img = pg.transform.scale(img, (3*43,3*52))
            dead_frames.append(img)
        self.walk_frames = walk_frames          
        self.attack_frames = attack_frames 
        self.dead_frames = dead_frames 
        self.index = 0
        self.image = self.walk_frames[self.index]

        self.rect = self.image.get_rect(midbottom=(x, GROUND_Y))  
        
        # self.rect.width = int(self.rect.width * 0.2) 
        # self.rect.height = int(self.rect.height * 0.5)   

        # self.rect.inflate_ip(-80, 0)      
        self.hitbox = hitbox_module.Hitbox(self, 60, 90)
      
        # self.rect = self.image.get_bounding_rect()    
        # self.rect.midbottom = (x, GROUND_Y)
        self.animation_speed = 0.30 
        self.counter = 0
        self.health = 100  
        self.damage = 0.1
        self.player_can_move = [True, True]  
        self.reverse_image = False   
        self.kill_time = None        

    def animate_walk(self):        
        self.counter += self.animation_speed
        if self.counter >= len(self.walk_frames):
            self.counter = 0
        self.index = int(self.counter)
        self.image = pg.transform.flip(self.walk_frames[self.index], True, False) if self.reverse_image else self.walk_frames[self.index]                  

    def animate_attack(self):
        self.counter += self.animation_speed / 10
        if self.counter >= len(self.attack_frames):
            self.counter = 0
        self.index = int(self.counter)
        self.image = pg.transform.flip(self.attack_frames[self.index], True, False) if self.reverse_image else self.attack_frames[self.index]         
   
    def animate_death(self):
        if self.counter < len(self.dead_frames)-1:
            self.counter += self.animation_speed      
        self.index = int(self.counter)
        self.image = pg.transform.flip(self.dead_frames[self.index], True, False) if self.reverse_image else self.dead_frames[self.index] 

    def update(self, move_step, player_s, npcs, can_move_left, can_move_right): 
        # adjust camera movements
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] and can_move_right:
            self.rect.centerx -= move_step
        if keys[pg.K_LEFT] and can_move_left:
            self.rect.centerx += move_step   
        # death
        if self.health < 0:
            self.player_can_move = [True, True]
            self.animate_death()  
            if not self.kill_time:                
                self.kill_time = time.time()
            elif time.time() - self.kill_time >= 2:
                self.kill()        
        else:  
            old_x = self.rect.centerx 
            # normal moving
            if player_s.rect.centerx < self.rect.centerx:                
                self.rect.centerx -= 1                          
                self.animate_walk()
                self.reverse_image = True
            elif player_s.rect.centerx > self.rect.x:                                
                self.rect.centerx += 1
                self.reverse_image = False
                self.animate_walk() 
            # colisions with other npc             
            npc_hits = pg.sprite.spritecollide(self, npcs, False)
            for other in npc_hits:
                if other is not self:
                    if pg.sprite.collide_rect(self.hitbox, other.hitbox):           
                        if other.rect.centerx > self.rect.centerx:
                            # other.rect.centerx += 1
                            self.rect.centerx -= 1
                        else:
                            # other.rect.centerx -= 1
                            self.rect.centerx += 1 
                        # self.hitbox.update(self)                   
            # move hitbox
            self.hitbox.update(self)
            # colisions with player from side            
            if self.hitbox.rect.colliderect(player_s.rect):                   
                self.animate_attack()
                self.rect.centerx = old_x   
                self.hitbox.rect.centerx = old_x                 
                player_s.health -= self.damage   
                if player_s.rect.centerx > self.hitbox.rect.x: self.player_can_move = [False, True]  
                else: self.player_can_move = [True, False]
            else: self.player_can_move = [True, True]
