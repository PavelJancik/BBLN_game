import pygame as pg

def draw_health_bar(surf, x, y, w, h, current, maximum):
    pg.draw.rect(surf, '#bb2222', (x, y, w, h))    
    pg.draw.rect(surf, '#22bb22', (x, y, w * current / maximum, h))
    pg.draw.rect(surf, 'White', (x, y, w, h), 2)
    font = pg.font.Font('fonts/Tiny5/Tiny5-Regular.ttf', 30)
    text = font.render(f"{round(current)}", True, 'White')
    text_rect = text.get_rect(center=(x + w // 2, y + h // 2))
    surf.blit(text, text_rect)  

def draw_score(surf, x, y, score):
    font = pg.font.Font('fonts/Tiny5/Tiny5-Regular.ttf', 50)
    text = font.render(f"{round(score)}", True, "White")
    text_rect = text.get_rect(center=(x, y))
    surf.blit(text, text_rect)   

def load_frames(sheet_path, frame_width, frame_height, num_frames, transform_w, transform_h):
    sheet = pg.image.load(sheet_path).convert_alpha()
    frames = []
    for i in range(num_frames):
        frame = sheet.subsurface(pg.Rect(
            i * frame_width, 0, frame_width, frame_height
        ))
        frame = pg.transform.scale(frame, (transform_w, transform_h))
        frames.append(frame)
    return frames 

def game_over(player):
    return player.sprite.health <= 0

