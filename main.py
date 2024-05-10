import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hero Something")

# sets frames
clock = pygame.time.Clock()
frames = 55

# game vars
GRAVITY = 1
SCROLL_TRESH = 350
scroll = 0
bg_scroll = 0
game_over = False
lives = 3
score = 0

# fonts
font_big = pygame.font.SysFont("Times New Roman", 36)

# images
background = pygame.image.load("./assets/bg_1.PNG").convert_alpha()
#hero_img = pygame.image.load("./assets/hero_idle_0.png").convert_alpha()
idle_images = [pygame.image.load(f"./assets/idle_{i}.png").convert_alpha() for i in range(10)]
moving_images = [pygame.image.load(f"./assets/moving_{i}.png").convert_alpha() for i in range(10)]
floors = pygame.image.load("./assets/floor_0.png").convert_alpha()

def draw_bg(bg_scroll):
    screen.blit(background, (0, 0 + bg_scroll))
    screen.blit(background, (0, -700 + bg_scroll))

def draw_text(text, font, text_col, x, y):
    txt_img = font.render(text, True, text_col)
    screen.blit(txt_img, (x, y))

class Player():
    def __init__(self, x, y):
        #self.image = pygame.transform.scale(hero_img, (100, 100))
        self.idle_images = [pygame.transform.scale(img, (100, 100)) for img in idle_images]
        self.moving_images = [pygame.transform.scale(img, (100, 100)) for img in moving_images]
        self.width = 60
        self.height = 70
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = True
        self.jump_counter = 0 
        self.animation_state = 'idle'
        self.animation_index = 0 
        self.image = self.idle_images[0]

    def update_animation(self):
        if self.animation_state == 'idle':
            self.image = self.idle_images[self.animation_index]
        elif self.animation_state == 'moving':
            self.image = self.moving_images[self.animation_index]
        self.animation_index = (self.animation_index + 1) % len(self.idle_images)


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 20))
        

    def jump(self):
        if self.jump_counter <= 2: 
            self.vel_y = -15
            self.jump_counter += 1

    def move(self):
        # offscreen
        scroll = 0
        dx = 0
        dy = 0

        # key presses
        key = pygame.key.get_pressed()
        
        if key[pygame.K_a]:
            dx -= 10
            self.flip = False
            self.animation_state = 'moving'
        elif key[pygame.K_d]:
            dx += 10
            self.flip = True
            self.animation_state = 'moving'
        if key[pygame.K_w]:
            self.jump()

        self.vel_y += GRAVITY
        dy += self.vel_y

        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        # other platforms
        for platform in plat_group:
            if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.jump_counter = 0
                    break

        if self.rect.top <=SCROLL_TRESH:
            if self.vel_y < 0:
                scroll = -dy

        # update
        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(floors, (width, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        self.rect.y += scroll 

    
hero = Player(0, 570)


# Put into levels later
plat_group = pygame.sprite.Group()

def load_level_one():
    plat_positions = [
        (0, 570, 250),
        (550, 405, 250),
        (50, 200, 250),
        (100, 200, 250),
        (500, -5, 250),
        (200, -205, 250),
        (300, -405, 250),
        (500, -605, 250),
        (300, -805, 250),
        (500, -1005, 250),
        (300, -1105, 250)
    ]

    plat_group.empty()

    for pos in plat_positions:
        platform = Platform(*pos)
        plat_group.add(platform)


load_level_one()

run = True
while run:
    clock.tick(frames)

    if (game_over == False):
        scroll = hero.move()
        
        bg_scroll += scroll
        if bg_scroll >= 700:
            bg_scroll = 0
        draw_bg(bg_scroll)

        plat_group.update(scroll)

        plat_group.draw(screen)
        hero.draw()
        hero.update_animation()

        if hero.rect.bottom > SCREEN_HEIGHT:
            game_over = True
    else:
        draw_text("Game Over!", font_big, (255, 255, 255), 130, 200)
        draw_text("Score: " + str(score), font_big, (255, 255, 255), 130, 250)
        draw_text("Space To Restart!", font_big, (255, 255, 255), 130, 300)

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            game_over = False
            score = 0
            scroll = 0
            hero.rect.center = (0, 570)
            # Will get changed to Level load one 
            load_level_one()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()