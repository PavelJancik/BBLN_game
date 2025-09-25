import pygame as pg
from sys import exit
import player_module
import block_module
import msg_module
from config import *

# engine
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Babyløn')
clock = pg.time.Clock()

# player
player = pg.sprite.GroupSingle()
player.add(player_module.Player(100,100))

# ground floor
top_layer = pg.sprite.Group()
ground_w = 256
num_of_ground_blocks = SCREEN_WIDTH // ground_w * 3
for i in range(num_of_ground_blocks):
    top_layer.add(
        block_module.Block(0 + i * ground_w, GROUND_Y - 25, ground_w, 128, TOP_LAYER_SPEED, 'ground.png')
    )

# sky
bottom_layer = pg.sprite.Group()
bottom_layer.add(block_module.Block(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 1, 'sky_1.png'))
bottom_layer.add(block_module.Block(SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 1, 'sky_2.png'))

blocks = pg.sprite.Group(
    # Start
    block_module.Block(player.sprite.rect.left-50, GROUND_Y-300, 50, 300, TOP_LAYER_SPEED, None),
    # Konec
    block_module.Block(player.sprite.rect.x + player.sprite.rect.w + MAX_CAMERA_X,
     GROUND_Y - 300, 50, 300, TOP_LAYER_SPEED, None),
    # Dodavka
    block_module.Block(SCREEN_WIDTH, GROUND_Y-200, 300, 200, TOP_LAYER_SPEED, None),
    # Vozik
    block_module.Block(SCREEN_WIDTH-470, GROUND_Y-200, 450, 200, TOP_LAYER_SPEED, None),
    # stage
    block_module.Block(SCREEN_WIDTH + 400, GROUND_Y-500, 900, 500, TOP_LAYER_SPEED, 'stage.png'),
    # stage podlaha
    block_module.Block(SCREEN_WIDTH + 400, GROUND_Y-50, 900, 50, TOP_LAYER_SPEED, 'stageFloor.png'),
)

# music
music = pg.mixer.Sound('audio/music/Salieri_8-bit.mp3')
# music.play(loops = -1)

# camera
camera = pg.sprite.GroupSingle(block_module.Block(0,0,0,0,1,None))

# messenger
msg1 = pg.sprite.GroupSingle(msg_module.Msg('Koncert za chvíli začíná, pospěš si! Musíme to všechno stihnout nachystat.'))
msg2 = pg.sprite.GroupSingle(msg_module.Msg('Vylez nahoru na stage a nachystej backdrop!'))
msg3 = pg.sprite.GroupSingle(msg_module.Msg(''))
messages = [msg1, msg2, msg3]
curr_msg_index = 0
 
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()        
        if event.type == pg.KEYDOWN: 
            if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER: 
                if curr_msg_index < len(messages) - 1 and messages[curr_msg_index].sprite.msg_completed():
                    curr_msg_index += 1
                
        
    bottom_layer.draw(screen)
    bottom_layer.update(camera.sprite.rect.x)

    blocks.draw(screen)
    blocks.update(camera.sprite.rect.x)

    player.draw(screen)
    player.update(blocks)

    top_layer.draw(screen)
    top_layer.update(camera.sprite.rect.x)

    camera.draw(screen)
    camera.update(camera.sprite.rect.x)

    messages[curr_msg_index].draw(screen)
    messages[curr_msg_index].update()

    pg.display.update()
    clock.tick(60)