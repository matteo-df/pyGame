import pygame
import sys
from random import randint, uniform


def laser_update(laser_list, speed=200):
    for rect in laser_list:
        rect.y -= round(speed*dt)
        if rect.bottom < 0:
            laser_list.remove(rect)


def meteor_update(meteor_list, speed=500):
    for rect, dir in meteor_list:
        rect.center += dir * speed * dt
        if rect.top > WINDOW_HEIGHT:
            meteor_list.remove((rect, dir))


def check_can_shoot(can_shoot, duration=500):
    if not can_shoot:
        current_time = pygame.time.get_ticks()
        if (current_time - shoot_time) > duration:
            can_shoot = True
    return can_shoot


def display_score():
    score_txt = f'Score: {pygame.time.get_ticks() // 1000}'
    text_surf = font.render(score_txt, True, 'white')
    text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 30))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, 'white', text_rect.inflate(30, 30), width=8, border_radius=5)


pygame.init()
GAME_TITLE = 'Asteroid Shooter'
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode(size=(WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

clock = pygame.time.Clock()

# font
font = pygame.font.Font('files/graphics/subatomic.ttf', 50)

# background
background_surf = pygame.image.load('files/graphics/background.png').convert()

# ship
ship_surf = pygame.image.load('files/graphics/ship.png').convert_alpha()
ship_rect = ship_surf.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

# laser
laser_surf = pygame.image.load('files/graphics/laser.png').convert_alpha()
laser_list = []

# meteor
meteor_surf = pygame.image.load('files/graphics/meteor.png').convert_alpha()
meteor_list = []
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 1000)

# sounds
laser_sound = pygame.mixer.Sound('files/sounds/laser.ogg')
explosion_sound = pygame.mixer.Sound('files/sounds/explosion.wav')
background_sound = pygame.mixer.Sound('files/sounds/music.wav')


can_shoot = True
shoot_time = 0

background_sound.play(loops=-1)

play_game = True

while play_game:
    # 1. Input of the player (sono chiamati 'event' e può essere la pressione di un tasto, il movimento del mouse,
    # il click del mouse, un tocco sul touchscreen...)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # <- tipo evento realtivo a quando si preme la x della finstra del tab in alto
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:
            laser_rect = laser_surf.get_rect(midbottom=ship_rect.midtop)
            laser_list.append(laser_rect)
            laser_sound.play()
            shoot_time = pygame.time.get_ticks()
            can_shoot = False
        if event.type == meteor_timer:
            meteor_rect = meteor_surf.get_rect(midbottom=(randint(0,WINDOW_WIDTH),0))
            meteor_dir = pygame.math.Vector2(uniform(-0.5,0.5),1)
            meteor_list.append((meteor_rect, meteor_dir))

    # Limit the framerate
    dt = clock.tick(120) / 1000

    ship_rect.center = pygame.mouse.get_pos()

    can_shoot = check_can_shoot(can_shoot)

    laser_update(laser_list)
    meteor_update(meteor_list)

    # ship-meteor collision
    for meteor_rect, _ in meteor_list:
        if meteor_rect.colliderect(ship_rect):
            play_game = False

    # laser-meteor collision
    for laser_rect in laser_list:
        for meteor_tuple in meteor_list:
            if laser_rect.colliderect(meteor_tuple[0]):
                explosion_sound.play()
                laser_list.remove(laser_rect)
                meteor_list.remove(meteor_tuple)

    # 2. Updates
    display_surface.fill((0,0,0))
    display_surface.blit(background_surf, (0,0))
    display_score()

    display_surface.blit(ship_surf, ship_rect)

    for laser_rect in laser_list:
        display_surface.blit(laser_surf, laser_rect)
    for meteor_rect, _ in meteor_list:
        display_surface.blit(meteor_surf, meteor_rect)
    # 3. Show the resulting frame (updating the display surface)
    pygame.display.update()

# You Lost!
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # <- tipo evento realtivo a quando si preme la x della finstra del tab in alto
            pygame.quit()
            sys.exit()
    background_sound.stop()
    display_surface.fill((0,0,0))
    lose_text_surf = font.render('You lost!', True, 'red')
    lose_text_rect = lose_text_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
    display_surface.blit(lose_text_surf, lose_text_rect)
    pygame.display.update()
