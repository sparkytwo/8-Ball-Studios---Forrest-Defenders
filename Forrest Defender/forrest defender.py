import pygame
from GameObject import GameObject


# Setting up the Window
(screen_width, screen_height) = (1334,750)
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.flip()
pygame.display.set_caption(('Forrest Defenders'))

# Camera
cam_x = screen_width / 2
cam_y = screen_height / 2

# Game Clock
clock = pygame.time.Clock()

# Game Values
game_state = 1 # 0 = Main_Menu, 1 = Idle_Game, 2 = Shooter
mana = 0
mana_per_second = 1

# Initialise Sprites
mana_bar = GameObject('Images/Mana.png', (0, 0), (500, 153))
tree = GameObject('Images/tree.png', (cam_x - 75, cam_y - 100), (150, 200))
grass = GameObject('Images/grass.png', (cam_x - 200, cam_y - 200), (400, 400))


# Update Function
def update():
    pygame.display.flip()

# Render Function
def render():
    if game_state == 1:
        screen.blit(grass.image, grass.rect)
        screen.blit(tree.image, tree.rect)
        screen.blit(mana_bar.image, mana_bar.rect)
        

# Input Function
def inputs():
    pass
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    update()

    render()
    inputs()
    clock.tick(60)

