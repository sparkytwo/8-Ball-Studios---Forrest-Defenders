import pygame
from colors import *
from GameObject import GameObject
from button import Button

pygame.init()
# Setting up the Window
(screen_width, screen_height) = (1334, 750)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.flip()
pygame.display.set_caption(('Forrest Defenders'))

# Camera
cam_x = screen_width / 2
cam_y = screen_height / 2

# Game Clock
clock = pygame.time.Clock()
dt = clock.tick(60)/1000

# Game Values
game_state = 1  # 0 = Main_Menu, 1 = Idle_Game, 2 = Shooter
mana_int = 0
mana_per_second = 1
alpha = 0
# Fonts

font = pygame.font.SysFont('Futura', 55)
font_small = pygame.font.SysFont('Futura', 35)

# Initialise Sprites
mana_bar = GameObject('Images/Mana.png', (0, 0), (500, 153))
dirt = GameObject('Images/dirt.png', (0, 0), (1334, 750))
menu_panel = GameObject('Images/menu_panel.png', (0, 0), (1334, 750))
mana_drop_x = 600
mana_drop_y = 300
mana_drop = GameObject('Images/manadrop.png', (600, 300), (17, 20))

# Initial Image
menu_img = pygame.image.load('Images/Menu.png')
menu_p_image = pygame.image.load('Images/PressedMenu.png')
left_arrow_img = pygame.image.load('Images/Left Arrow.png')
left_arrow_p_img = pygame.image.load('Images/Left Arrow Pressed.png')
right_arrow_img = pygame.image.load('Images/Right Arrow.png')
right_arrow_p_img = pygame.image.load('Images/Right Arrow Pressed.png')

# Initialise Button
menu = Button(1150, 0, menu_img, menu_p_image, 1)
left_arrow = Button(20, 400, left_arrow_img, left_arrow_p_img, 1)
right_arrow = Button(1230, 400, right_arrow_img, right_arrow_p_img, 1)

# Initialise Text
mana = font.render(str(mana_int), True, WHITE)
mana_incr = font.render(str(mana_per_second) + "/s", True, WHITE)
mana_incr_drop = font_small.render(str(mana_per_second), True, WHITE)
mana_incr_drop_rect = pygame.Rect(630,300,100,100)
# Update Function
def update():
    if game_state == 1:
        global mana_int
        global mana
        global alpha
        # Increments Mana
        mana_int += mana_per_second * dt
        mana = font.render(str(int(mana_int)), True, WHITE)
        # Checks Menu
        if menu.clicked:
            menu.c_img = menu.p_image
        else:
            menu.c_img = menu.d_image

        if left_arrow.clicked:
            left_arrow.c_img = left_arrow.p_image
        else:
            left_arrow.c_img = left_arrow.d_image

        if right_arrow.clicked:
            right_arrow.c_img = right_arrow.p_image
        else:
            right_arrow.c_img = right_arrow.d_image

        # Mana Gain sprite
        mana_drop.rect.y -= 250 * dt
        mana_drop.image.set_alpha(alpha)
        alpha += 300 * dt
        mana_incr_drop_rect.y -= 250 * dt
        if mana_drop.rect.y < 50:
            mana_drop.rect.y = 300
            mana_incr_drop_rect.y = 300
            alpha = 0
    pygame.display.flip()


# Render Function
def render():
    if game_state == 1:
        screen.blit(dirt.image, dirt.rect)
        screen.blit(mana_drop.image, mana_drop.rect)
        screen.blit(mana_incr_drop, mana_incr_drop_rect)
        screen.blit(mana_bar.image, mana_bar.rect)
        screen.blit(mana, (30, 25))
        screen.blit(mana_incr, (70, 100))
        screen.blit(menu.c_img, menu.rect)
        if menu_panel.visibility:
            screen.blit(menu_panel.image, menu_panel.rect)
            screen.blit(left_arrow.c_img, left_arrow.rect)
            screen.blit(right_arrow.c_img, right_arrow.rect)

# Input Function
def inputs():
    if game_state == 1:
        if menu.click():
            if menu_panel.visibility:
                menu_panel.visibility = False
            elif not menu_panel.visibility:
                menu_panel.visibility = True
        left_arrow.click()
        right_arrow.click()


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    update()

    render()
    inputs()
    clock.tick(60)
