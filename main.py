import pygame as pg
from sys import exit
import player_module
import block_module
import msg_module
import NPC_module
import engine_module
from config import *

# engine
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Babyløn')
clock = pg.time.Clock()
score = 0
display_home_screen = True

# NPC timer
npcs = pg.sprite.Group()
CREATE_NPC = pg.USEREVENT + 1
pg.time.set_timer(CREATE_NPC, ZOMBIE_SPAWN_TIME) 

def init_player():    
    player = pg.sprite.GroupSingle()
    player.add(player_module.Player())
    return player
player = init_player()

# ground floor
top_layer = pg.sprite.Group()
ground_w = 256
num_of_ground_blocks = SCREEN_WIDTH // ground_w * 3
for i in range(num_of_ground_blocks):
    top_layer.add(
        block_module.Block(0 + i * ground_w, GROUND_Y - 25, ground_w, 128, TOP_LAYER_SPEED, 'ground.png')
    )

# middle layer
middle_layer = pg.sprite.Group()
middle_layer_block_w = 576
num_of_middle_blocks = SCREEN_WIDTH // middle_layer_block_w * 3
for i in range(num_of_middle_blocks):
    middle_layer.add(
        block_module.Block(0 + i * middle_layer_block_w, GROUND_Y - 300, middle_layer_block_w, 324, 3, 'bg_middle.png')
    )

# sky
bottom_layer = pg.sprite.Group()
bottom_layer.add(block_module.Block(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 1, 'sky_1.png'))
bottom_layer.add(block_module.Block(SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 1, 'sky_2.png'))

# Blocks
start_block = block_module.Block(player.sprite.rect.left-400, GROUND_Y-400, 400, 400, TOP_LAYER_SPEED, 'building.png')
end_block = block_module.Block(3200, GROUND_Y - 300, 50, 300, TOP_LAYER_SPEED, None)
stage_x = 550
blocks = pg.sprite.Group(
    start_block,
    end_block,     
    block_module.Block(SCREEN_WIDTH+20, GROUND_Y-210, 350, 220, TOP_LAYER_SPEED, 'vozik.png'),
    block_module.Block(SCREEN_WIDTH-470, GROUND_Y-220, 500, 220, TOP_LAYER_SPEED, 'van.png'),
    block_module.Block(SCREEN_WIDTH + stage_x, GROUND_Y-500, 900, 500, TOP_LAYER_SPEED, 'stage.png'),
    block_module.Block(SCREEN_WIDTH + stage_x, GROUND_Y-95, 900, 1, TOP_LAYER_SPEED, 'BBLN_transparent.png'), # stage floor
    block_module.Block(SCREEN_WIDTH + stage_x+75, GROUND_Y-220, 90, 1, TOP_LAYER_SPEED, 'BBLN_transparent.png'), # Repro left
    block_module.Block(SCREEN_WIDTH + stage_x+735, GROUND_Y-220, 90, 1, TOP_LAYER_SPEED, 'BBLN_transparent.png'), # Repro right   
)

# music
music = pg.mixer.Sound('audio/music/Salieri_8-bit.mp3')
# music.play(loops = -1)

# messenger
msg1 = pg.sprite.GroupSingle(msg_module.Msg('Ale ne! Na druhé stagy právě dohrál @#^+!&* a vymyl všem lidem mozky!', SCREEN_WIDTH / 2, 200, 30, '#3e3e3e'))
msg2 = pg.sprite.GroupSingle(msg_module.Msg('Teď z nich jsou vyzobaný slepice a valí se na nás!', SCREEN_WIDTH / 2, 200, 30, '#3e3e3e'))
msg3 = pg.sprite.GroupSingle(msg_module.Msg('',0,0,0, '#3e3e3e'))
# messages = [msg1, msg2, msg3] # for prod
messages = [msg3] # for dev
curr_msg_index = 0

# home screen 
homeScreenBgImg = pg.image.load("imgs/homeScreen.jpg").convert() 
homeScreenBgImg = pg.transform.scale(homeScreenBgImg, (SCREEN_WIDTH, SCREEN_HEIGHT))
img_h = 100
line_h = 50
names = ['Honza', 'Jirka', 'David', 'Radim', 'Pavel']
selectedName_i = 0
homeScreenImgs = pg.sprite.Group()
homeScreenText = pg.sprite.Group(
    msg_module.Msg('Babyløn', SCREEN_WIDTH / 4, line_h*2, 40, 'White'),
    msg_module.Msg('← Move Left', SCREEN_WIDTH / 4, line_h*4, 20, 'White'),
    msg_module.Msg('→ Move Right', SCREEN_WIDTH / 4, line_h*5, 20, 'White'),
    msg_module.Msg('↑ Jump', SCREEN_WIDTH / 4, line_h*6, 20, 'White'),
    msg_module.Msg('↓ Jump Off', SCREEN_WIDTH / 4, line_h*7, 20, 'White'),
    msg_module.Msg('Space - Attack', SCREEN_WIDTH / 4, line_h*8, 20, 'White'),
    msg_module.Msg('Choose your character', SCREEN_WIDTH / 4, line_h*10, 20, 'White'),  
)
for index, name in enumerate(names):    
    homeScreenImgs.add(block_module.Block(SCREEN_WIDTH - 400, 1.1*img_h*(1+index), img_h, img_h, 0, f'char_{name}.png'))
    homeScreenText.add( msg_module.Msg(name, SCREEN_WIDTH-250, img_h/2+1.1*img_h*(1+index), 20, 'White'))

player_can_move_left = True
player_can_move_right = True
def can_move_left():
    return player_can_move_left and player.sprite.rect.left > start_block.rect.right
def can_move_right():
    return player_can_move_right and player.sprite.rect.right < end_block.rect.left
 
npcs.add(NPC_module.NPC(start_block.rect.x+600))
npcs.add(NPC_module.NPC(start_block.rect.x+300))
running = True
while running:
    game_over = engine_module.game_over(player)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()   
        # home screen
        if display_home_screen:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER: 
                    display_home_screen = False
                    # TODO dodelat char selection
                    print('Index ', selectedName_i, ' > ', names[selectedName_i])
                if event.key == pg.K_UP: 
                    if selectedName_i >= 1:
                        selectedName_i -= 1                        
                if event.key == pg.K_DOWN: 
                    if selectedName_i < len(names)-1:
                        selectedName_i += 1                        
        # game over
        elif game_over:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER: 
                    display_home_screen = True
                    # todo remove player instance and create new
                    # a vlastne asi u vseho to bude nejjednodusi
                    # takze vsechno do metod a pak je jen volat ve funkci init_new_game()
        # game is running
        else:     
            if event.type == pg.KEYDOWN: 
                if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER: 
                    if curr_msg_index < len(messages) - 1 and messages[curr_msg_index].sprite.msg_completed():
                        curr_msg_index += 1
            if event.type == CREATE_NPC:                
                if len(npcs)+2 <= MAX_ZOMBIE_COUNT:
                    npcs.add(NPC_module.NPC(start_block.rect.x-200))
                    npcs.add(NPC_module.NPC(end_block.rect.x+200))
            
    # home screen
    if display_home_screen:
        screen.blit(homeScreenBgImg, (0, 0))
        homeScreenText.draw(screen)
        homeScreenText.update()
        homeScreenImgs.draw(screen)
        pg.draw.rect(screen, 'White', (homeScreenImgs.sprites()[selectedName_i].rect.x, homeScreenImgs.sprites()[selectedName_i].rect.y, 200, 100), width=5)        
    # game over
    elif game_over:
        screen.fill('Black')        
    # game is running
    else:        
        bottom_layer.draw(screen)
        middle_layer.draw(screen)
        blocks.draw(screen)
        player.draw(screen)
        npcs.draw(screen)
        top_layer.draw(screen)             

        messages[curr_msg_index].draw(screen)    
        messages[curr_msg_index].update()

        engine_module.draw_health_bar(screen, 20, 20, 200, 50, player.sprite.health, player.sprite.max_health)
        engine_module.draw_score(screen, SCREEN_WIDTH - 40, 40, score)

        if curr_msg_index == len(messages) - 1 and messages[curr_msg_index].sprite.msg_completed():
            # player
            player.update(blocks, npcs)
            # npc
            npcs.update(TOP_LAYER_SPEED, player.sprite, npcs, can_move_left(), can_move_right())    
            # blocks            
            blocks.update(can_move_left(), can_move_right())
            bottom_layer.update(can_move_left(), can_move_right())
            middle_layer.update(can_move_left(), can_move_right())
            top_layer.update(can_move_left(), can_move_right())    

        if any(not z.player_can_move[0] for z in npcs): player_can_move_left = False
        else: player_can_move_left = True
        if any(not z.player_can_move[1] for z in npcs): player_can_move_right = False
        else: player_can_move_right = True

        # for zombie in npcs:        
        #     if zombie.health <= 0:
        #         zombie.kill()
        #         score += 1

    pg.display.update()
    clock.tick(60)