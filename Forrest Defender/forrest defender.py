import pygame
from colors import *
from GameObject import GameObject
from button import Button


class Game(object):
    def __init__(self):
        # Setting up the Window
        self.screen_width = 580
        self.screen_height = 1080
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Forrest Defenders')

        # Camera
        self.cam_x = self.screen_width / 2
        self.cam_y = self.screen_height / 2

        # Game Clock
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60)/1000

        # Game Values
        self.game_state = 1  # 0 = Main_Menu, 1 = Idle_Game, 2 = Shooter
        self.mana_int = 0
        self.mana_per_second = 100
        self.alpha = 0
        # Fonts

        self.font = pygame.font.SysFont('Futura', 55)
        self.font_small = pygame.font.SysFont('Futura', 35)

        # Initialise Sprites
        self.mana_bar = GameObject('Images/Mana.png', (0, 0), (580, 153))
        self.dirt = GameObject('Images/dirt.png', (0, 0), (580, 1080))
        self.menu_panel = GameObject('Images/menu_panel.png', (self.screen_width, self.screen_height * 0.15), (1334, 750))
        self.mana_drop_x = 600
        self.mana_drop_y = 300
        self.mana_droplet = GameObject('Images/manadrop.png', (600, 300), (17, 20))

        # Initial Image
        self.menu_img = pygame.image.load('Images/Menu.png')
        self.menu_p_image = pygame.image.load('Images/PressedMenu.png')
        self.left_arrow_img = pygame.image.load('Images/Left Arrow.png')
        self.left_arrow_p_img = pygame.image.load('Images/Left Arrow Pressed.png')
        self.right_arrow_img = pygame.image.load('Images/Right Arrow.png')
        self.right_arrow_p_img = pygame.image.load('Images/Right Arrow Pressed.png')

        # Initialise Button
        self.menu = Button(self.screen_width - self.menu_img.get_width(), self.screen_height * 0.4, self.menu_img, self.menu_p_image, 1)
        self.left_arrow = Button(20, 400, self.left_arrow_img, self.left_arrow_p_img, 1)
        self.right_arrow = Button(1230, 400, self.right_arrow_img, self.right_arrow_p_img, 1)

        # Initialise Text
        self.mana = self.font.render(str(self.mana_int), True, WHITE)
        self.mana_rect = pygame.Rect(0, 0, self.mana.get_width(), self.mana.get_height())
        self.mana_bar_droplet = GameObject('Images/manadrop bar.png', (
        self.mana_bar.rect.width * 0.5 - self.mana_rect.width * 0.5 - self.mana_droplet.rect.width, 300), (34, 40))

        self.mana_incr = self.font.render(str(self.mana_per_second) + " m/s", True, WHITE)
        self.mana_incr_rect = pygame.Rect(0, 0, self.mana_incr.get_width(), self.mana_incr.get_height())
        self.mana_incr_drop = self.font_small.render(str(self.mana_per_second), True, WHITE)
        self.mana_incr_drop_rect = pygame.Rect(630, 300, 100, 100)
    # Update Function
    def update(self):
        if self.game_state == 1:
            # Increments Mana
            self.mana_int += self.mana_per_second * self.dt
            self.mana = self.font.render(str(int(self.mana_int)), True, WHITE)
            self.mana_rect = pygame.Rect(0, 0, self.mana.get_width(), self.mana.get_height())

            if self.menu_panel.visibility == True:
                if self.menu_panel.rect.x > self.screen_width * 0.2:
                    self.menu_panel.rect.x -= 2000 * self.dt
                    self.menu.rect.x = self.menu_panel.rect.x - self.menu.rect.width
            if self.menu_panel.visibility == False:
                if self.menu_panel.rect.x < self.screen_width:
                    self.menu_panel.rect.x += 2000 * self.dt
                    self.menu.rect.x = self.menu_panel.rect.x - self.menu.rect.width
            # Checks Menu
            if self.menu.clicked:
                self.menu.c_img = self.menu.p_image
            else:
                self.menu.c_img = self.menu.d_image



            # Mana Gain sprite
            self.mana_droplet.rect.y -= 250 * self.dt
            self.mana_droplet.image.set_alpha(self.alpha)
            self.alpha += 300 * self.dt
            self.mana_incr_drop_rect.y -= 250 * self.dt
            
            if self.mana_droplet.rect.y < 50:
                self.mana_droplet.rect.y = 300
                self.mana_incr_drop_rect.y = 300
                self.alpha = 0
            pygame.display.flip()


    # Render Function
    def render(self):
        if self.game_state == 1:
            self.screen.blit(self.dirt.image, self.dirt.rect)
            self.screen.blit(self.mana_droplet.image, self.mana_droplet.rect)
            self.screen.blit(self.mana_incr_drop, self.mana_incr_drop_rect)
            self.screen.blit(self.mana_bar.image, self.mana_bar.rect)
            self.screen.blit(self.mana, (self.mana_bar.rect.width * 0.5 - self.mana_rect.width * 0.5, 30))
            self.screen.blit(self.mana_bar_droplet.image,(self.mana_bar.rect.width * 0.5 - self.mana_rect.width * 0.5 - self.mana_bar_droplet.rect.width - 10, 30))
            self.screen.blit(self.mana_incr, (self.mana_bar.rect.width * 0.5 - self.mana_incr_rect.width * 0.5, 110))
            self.screen.blit(self.menu.c_img, self.menu.rect)
            self.screen.blit(self.menu_panel.image, self.menu_panel.rect)

    # Input Function
    def inputs(self):
        if self.game_state == 1:
            if self.menu.click():
                if self.menu_panel.visibility:
                    self.menu_panel.visibility = False
                elif not self.menu_panel.visibility:
                    self.menu_panel.visibility = True
            if self.left_arrow.click():
               self.screen_width = 580
               self.screen_height = 1080
               self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            self.right_arrow.click()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update()

            self.render()
            self.inputs()
            self.clock.tick(60)


pygame.init()
game = Game()
game.run()
