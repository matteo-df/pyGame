import sys
import pygame
from random import uniform, randint


class Ship(pygame.sprite.Sprite):
    def __init__(self, group):
        # 1. eseguo l'init della classe parent (Sprite)
        super().__init__(group)
        # 2. creo la Surface, chiamandola image
        self.image = pygame.image.load('files/graphics/ship.png').convert_alpha()
        # 3. creo il Rectangle, chiamandolo rect
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        # 4. aggiungo una mask a partire dalla surface (così per le collisioni posso agire a livello di pixel e non di tutto il Rect)
        self.mask = pygame.mask.from_surface(self.image)
        # 5. aggiungo altri attributi specifici della classe
        self.can_shoot = True
        self.last_shoot_time = None

    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def update_can_shoot(self, delay=500):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if (current_time - self.last_shoot_time) > delay:
                self.can_shoot = True

    def laser_shoot(self):
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if mouse_pressed and self.can_shoot:
            self.last_shoot_time = pygame.time.get_ticks()
            self.can_shoot = False
            Laser(laser_group, pos=self.rect.midtop)

    def meteor_collision(self):
        if pygame.sprite.spritecollide(self, meteor_group, False, pygame.sprite.collide_mask):
            pygame.quit()
            sys.exit()

    def update(self):
        self.input_position()
        self.update_can_shoot()
        self.laser_shoot()
        self.meteor_collision()


class Laser(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        self.image = pygame.image.load('files/graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.dir = pygame.math.Vector2(0,-1)
        self.speed = 600
        self.explosion_sound = pygame.mixer.Sound('files/sounds/explosion.wav')

        # quando si crea il laser eseguo il suono
        pygame.mixer.Sound('files/sounds/laser.ogg').play()

    def move(self):
        self.pos += self.dir * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

    def meteor_collision(self):
        if pygame.sprite.spritecollide(self, meteor_group, True, pygame.sprite.collide_mask):
            self.explosion_sound.play()
            self.kill()

    def update(self):
        self.move()
        if self.rect.bottom < 0:
            self.kill()
        self.meteor_collision()


class Meteor(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        meteor_surf = pygame.image.load('files/graphics/meteor.png').convert_alpha()
        # randomizing the size of the meteor
        scaling_factor = uniform(0.5,3)
        new_size = pygame.math.Vector2(meteor_surf.get_size()) * scaling_factor
        self.image = pygame.transform.scale(meteor_surf, new_size)
        self.rect = self.image.get_rect(midbottom=(randint(0,WINDOW_WIDTH),0))
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.dir = pygame.math.Vector2(uniform(-0.5,0.5),1)
        self.speed = randint(300, 800) / scaling_factor

    def move(self):
        self.pos += self.dir * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

    def update(self):
        self.move()
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()


class Score:
    def __init__(self):
        self.font = pygame.font.Font('files/graphics/subatomic.ttf', 50)
        self.score = 0

    def display(self):
        self.score = pygame.time.get_ticks() // 1000
        text_score = f'Score: {self.score}'
        text_surf = self.font.render(text_score, True, 'white')
        text_rect = text_surf.get_rect(bottomleft=(20,WINDOW_HEIGHT-20))
        display_surface.blit(text_surf, text_rect)


# basic setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

# background
background_surf = pygame.image.load('files/graphics/background.png').convert()
background_music = pygame.mixer.Sound('files/sounds/music.wav')
background_music.set_volume(0.2)
background_music.play(loops=-1)

# score
score = Score()

# sprite groups
ship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

# sprite objects
ship = Ship(ship_group)

# meteor timer
meteor_generation = pygame.event.custom_type()
pygame.time.set_timer(meteor_generation, 400)

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == meteor_generation:
            Meteor(meteor_group)

    # delta time
    dt = clock.tick() / 1000

    # updates
    ship_group.update()
    laser_group.update()
    meteor_group.update()

    # frame background
    display_surface.fill('black')
    display_surface.blit(background_surf,(0,0))

    # score
    score.display()

    # graphics
    ship_group.draw(display_surface)
    laser_group.draw(display_surface)
    meteor_group.draw(display_surface)

    # update the frame
    pygame.display.update()
