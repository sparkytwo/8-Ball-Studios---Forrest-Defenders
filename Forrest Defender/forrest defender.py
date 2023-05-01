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
        self.mana_per_second = 1
        self.alpha = 0
        # Fonts

        self.font = pygame.font.SysFont('Futura', 55)
        self.font_small = pygame.font.SysFont('Futura', 35)
        self.font_menu = pygame.font.SysFont('Futura', 30)

        # Initialise Sprites
        self.mana_bar = GameObject('Images/Mana.png', (0, 0), (580, 153))
        self.background = GameObject('Images/background 1.png', (0, 0), (580, 1080))
        self.menu_panel = GameObject('Images/menu_panel.png', (self.screen_width, self.screen_height * 0.15), (1334, 750))
        self.mana_drop_x = 600
        self.mana_drop_y = 300
        self.mana_droplet = GameObject('Images/manadrop.png', (600, 300), (17, 20))

        # Initial Menu Images
        self.menu_img = pygame.image.load('Images/Menu.png')
        self.menu_p_image = pygame.image.load('Images/PressedMenu.png')
        self.upgrade_button_img = pygame.image.load("Images/Upgrade Button.png")
        self.upgrade_button_p_img = pygame.image.load("Images/Upgrade Button Pressed.png")



        # Menu Initialise Button
        self.menu = Button(self.screen_width - self.menu_img.get_width(), self.screen_height * 0.4, self.menu_img, self.menu_p_image, 1)
        self.upgrade_button_1 = Button(980, 220, self.upgrade_button_img, self.upgrade_button_p_img, 1)
        self.upgrade_button_2 = Button(980, 385, self.upgrade_button_img, self.upgrade_button_p_img, 1)
        self.upgrade_button_3 = Button(980, 550, self.upgrade_button_img, self.upgrade_button_p_img, 1)
        self.upgrade_button_4 = Button(980, 715, self.upgrade_button_img, self.upgrade_button_p_img, 1)
        self.upgrade_button_5 = Button(980, 875, self.upgrade_button_img, self.upgrade_button_p_img, 1)

        # Upgrade Boolean
        self.upgrade_button_1_boolean = False
        self.upgrade_button_2_boolean = False
        self.upgrade_button_3_boolean = False
        self.upgrade_button_4_boolean = False
        self.upgrade_button_5_boolean = False


        # Initialise Upgrade Cost
        self.upgrade_1_cost = 5
        self.upgrade_2_cost = 30
        self.upgrade_3_cost = 150
        self.upgrade_4_cost = 1000
        self.upgrade_5_cost = 5000

        # Initialise MPS Values
        self.upgrade_1_mps = 1
        self.upgrade_2_mps = 5
        self.upgrade_3_mps = 15
        self.upgrade_4_mps = 100
        self.upgrade_5_mps = 500


        # Initialise Text
        self.mana = self.font.render(self.human_format(int(self.mana_int)), True, WHITE)
        self.mana_rect = pygame.Rect(0, 0, self.mana.get_width(), self.mana.get_height())
        self.mana_bar_droplet = GameObject('Images/manadrop bar.png', (
        self.mana_bar.rect.width * 0.5 - self.mana_rect.width * 0.5 - self.mana_droplet.rect.width, 300), (34, 40))
        self.mana_incr = self.font.render(str(self.mana_per_second) + " m/s", True, WHITE)
        self.mana_incr_rect = pygame.Rect(0, 0, self.mana_incr.get_width(), self.mana_incr.get_height())
        self.mana_incr_drop = self.font_small.render(str(self.mana_per_second), True, WHITE)
        self.mana_incr_drop_rect = pygame.Rect(630, 300, 100, 100)
        #cost text
        self.upgrade_1_cost_text = self.font_menu.render(str(self.upgrade_1_cost), True, BLACK)
        self.upgrade_1_cost_text_rect = pygame.Rect(790, 275, 100, 100)
        self.upgrade_2_cost_text = self.font_menu.render(str(self.upgrade_2_cost), True, BLACK)
        self.upgrade_2_cost_text_rect = pygame.Rect(790, 445, 100, 100)
        self.upgrade_3_cost_text = self.font_menu.render(str(self.upgrade_3_cost), True, BLACK)
        self.upgrade_3_cost_text_rect = pygame.Rect(790, 610, 100, 100)
        self.upgrade_4_cost_text = self.font_menu.render(str(self.upgrade_4_cost), True, BLACK)
        self.upgrade_4_cost_text_rect = pygame.Rect(790, 775, 100, 100)
        self.upgrade_5_cost_text = self.font_menu.render(str(self.upgrade_5_cost), True, BLACK)
        self.upgrade_5_cost_text_rect = pygame.Rect(790, 935, 100, 100)
        #mps text
        self.upgrade_1_mps_text = self.font_menu.render(str(self.upgrade_1_mps), True, BLACK)
        self.upgrade_1_mps_text_rect = pygame.Rect(810, 250, 100, 100)
        self.upgrade_2_mps_text = self.font_menu.render(str(self.upgrade_2_mps), True, BLACK)
        self.upgrade_2_mps_text_rect = pygame.Rect(810, 415, 100, 100)
        self.upgrade_3_mps_text = self.font_menu.render(str(self.upgrade_3_mps), True, BLACK)
        self.upgrade_3_mps_text_rect = pygame.Rect(810, 581, 100, 100)
        self.upgrade_4_mps_text = self.font_menu.render(str(self.upgrade_4_mps), True, BLACK)
        self.upgrade_4_mps_text_rect = pygame.Rect(810, 745, 100, 100)
        self.upgrade_5_mps_text = self.font_menu.render(str(self.upgrade_5_mps), True, BLACK)
        self.upgrade_5_mps_text_rect = pygame.Rect(810, 905, 100, 100)

    # Update Function
    def update(self):
        if self.game_state == 1:
            # Increments Mana
            self.mana_int += self.mana_per_second * self.dt
            self.mana = self.font.render(self.human_format(int(self.mana_int)), True, WHITE)
            self.mana_rect = pygame.Rect(0, 0, self.mana.get_width(), self.mana.get_height())

            if self.upgrade_button_1_boolean:
                self.background = GameObject('Images/background 2.png', (0, 0), (580, 1080))
            if self.upgrade_button_2_boolean:
                self.background = GameObject('Images/background 3.png', (0, 0), (580, 1080))
            if self.upgrade_button_3_boolean:
                self.background = GameObject('Images/background 4.png', (0, 0), (580, 1080))
            if self.upgrade_button_4_boolean:
                self.background = GameObject('Images/background 5.png', (0, 0), (580, 1080))
            if self.upgrade_button_5_boolean:
                self.background = GameObject('Images/background 6.png', (0, 0), (580, 1080))
            # Menu Values
            self.upgrade_1_mps_text = self.font_menu.render(str(self.upgrade_1_mps), True, BLACK)
            self.upgrade_2_mps_text = self.font_menu.render(str(self.upgrade_2_mps), True, BLACK)
            self.upgrade_3_mps_text = self.font_menu.render(str(self.upgrade_3_mps), True, BLACK)
            self.upgrade_4_mps_text = self.font_menu.render(str(self.upgrade_4_mps), True, BLACK)
            self.upgrade_5_mps_text = self.font_menu.render(str(self.upgrade_5_mps), True, BLACK)

            self.upgrade_1_cost_text = self.font_menu.render(str(self.upgrade_1_cost), True, BLACK)
            self.upgrade_2_cost_text = self.font_menu.render(str(self.upgrade_2_cost), True, BLACK)
            self.upgrade_3_cost_text = self.font_menu.render(str(self.upgrade_3_cost), True, BLACK)
            self.upgrade_4_cost_text = self.font_menu.render(str(self.upgrade_4_cost), True, BLACK)
            self.upgrade_5_cost_text = self.font_menu.render(str(self.upgrade_5_cost), True, BLACK)

            if self.menu_panel.visibility:
                if self.menu_panel.rect.x > self.screen_width * 0.2:
                    self.menu_panel.rect.x -= 2000 * self.dt
                    self.upgrade_button_1.rect.x -= 2000 * self.dt
                    self.upgrade_button_2.rect.x -= 2000 * self.dt
                    self.upgrade_button_3.rect.x -= 2000 * self.dt
                    self.upgrade_button_4.rect.x -= 2000 * self.dt
                    self.upgrade_button_5.rect.x -= 2000 * self.dt
                    # Menu Text
                    self.upgrade_1_mps_text_rect.x -= 2000 * self.dt
                    self.upgrade_2_mps_text_rect.x -= 2000 * self.dt
                    self.upgrade_3_mps_text_rect.x -= 2000 * self.dt
                    self.upgrade_4_mps_text_rect.x -= 2000 * self.dt
                    self.upgrade_5_mps_text_rect.x -= 2000 * self.dt

                    self.upgrade_1_cost_text_rect.x -= 2000 * self.dt
                    self.upgrade_2_cost_text_rect.x -= 2000 * self.dt
                    self.upgrade_3_cost_text_rect.x -= 2000 * self.dt
                    self.upgrade_4_cost_text_rect.x -= 2000 * self.dt
                    self.upgrade_5_cost_text_rect.x -= 2000 * self.dt

                    self.menu.rect.x = self.menu_panel.rect.x - self.menu.rect.width
            if not self.menu_panel.visibility:
                if self.menu_panel.rect.x < self.screen_width:
                    self.menu_panel.rect.x += 2000 * self.dt
                    self.upgrade_button_1.rect.x += 2000 * self.dt
                    self.upgrade_button_2.rect.x += 2000 * self.dt
                    self.upgrade_button_3.rect.x += 2000 * self.dt
                    self.upgrade_button_4.rect.x += 2000 * self.dt
                    self.upgrade_button_5.rect.x += 2000 * self.dt
                    # Menu Text
                    self.upgrade_1_mps_text_rect.x += 2000 * self.dt
                    self.upgrade_2_mps_text_rect.x += 2000 * self.dt
                    self.upgrade_3_mps_text_rect.x += 2000 * self.dt
                    self.upgrade_4_mps_text_rect.x += 2000 * self.dt
                    self.upgrade_5_mps_text_rect.x += 2000 * self.dt

                    self.upgrade_1_cost_text_rect.x += 2000 * self.dt
                    self.upgrade_2_cost_text_rect.x += 2000 * self.dt
                    self.upgrade_3_cost_text_rect.x += 2000 * self.dt
                    self.upgrade_4_cost_text_rect.x += 2000 * self.dt
                    self.upgrade_5_cost_text_rect.x += 2000 * self.dt

                    self.menu.rect.x = self.menu_panel.rect.x - self.menu.rect.width
            # Checks Menu
            if self.menu.click():
                if self.menu_panel.visibility:
                    self.menu_panel.visibility = False
                elif not self.menu_panel.visibility:
                    self.menu_panel.visibility =True


            if self.upgrade_button_1.click() and self.mana_int > self.upgrade_1_cost:
                self.mana_int -= self.upgrade_1_cost
                self.upgrade_1_cost += self.upgrade_1_cost * 2
                self.upgrade_1_mps += 1
                self.mana_per_second += self.upgrade_1_mps
                self.upgrade_button_1_boolean = True
            if self.upgrade_button_2.click() and self.mana_int > self.upgrade_2_cost:
                self.mana_int -= self.upgrade_2_cost
                self.upgrade_2_cost += self.upgrade_2_cost * 2
                self.upgrade_2_mps += 5
                self.mana_per_second += self.upgrade_2_mps
                self.upgrade_button_2_boolean = True
            if self.upgrade_button_3.click() and self.mana_int > self.upgrade_3_cost:
                self.mana_int -= self.upgrade_3_cost
                self.upgrade_3_cost += self.upgrade_3_cost * 2
                self.upgrade_3_mps += 15
                self.mana_per_second += self.upgrade_3_mps
                self.upgrade_button_3_boolean = True
            if self.upgrade_button_4.click() and self.mana_int > self.upgrade_4_cost:
                self.mana_int -= self.upgrade_4_cost
                self.upgrade_4_cost += self.upgrade_4_cost * 2
                self.upgrade_4_mps += 100
                self.mana_per_second += self.upgrade_4_mps
                self.upgrade_button_4_boolean = True
            if self.upgrade_button_5.click() and self.mana_int > self.upgrade_5_cost:
                self.mana_int -= self.upgrade_5_cost
                self.upgrade_5_cost += self.upgrade_5_cost * 2
                self.upgrade_5_mps += 500
                self.mana_per_second += self.upgrade_5_mps
                self.upgrade_button_5_boolean = True
            self.mana_incr = self.font.render(str(self.mana_per_second) + " m/s", True, WHITE)



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
            self.screen.blit(self.background.image, self.background.rect)
            self.screen.blit(self.mana_droplet.image, self.mana_droplet.rect)
            self.screen.blit(self.mana_incr_drop, self.mana_incr_drop_rect)
            self.screen.blit(self.mana_bar.image, self.mana_bar.rect)
            self.screen.blit(self.mana, (self.mana_bar.rect.width * 0.5 - self.mana_rect.width * 0.5, 30))
            self.screen.blit(self.mana_bar_droplet.image,(self.mana_bar.rect.width * 0.5 - self.mana_rect.width * 0.5 - self.mana_bar_droplet.rect.width - 10, 30))
            self.screen.blit(self.mana_incr, (self.mana_bar.rect.width * 0.5 - self.mana_incr_rect.width * 0.5, 110))

            self.screen.blit(self.menu.c_img, self.menu.rect)
            self.screen.blit(self.menu_panel.image, self.menu_panel.rect)

            self.screen.blit(self.upgrade_button_1.c_img, self.upgrade_button_1.rect)
            self.screen.blit(self.upgrade_button_2.c_img, self.upgrade_button_2.rect)
            self.screen.blit(self.upgrade_button_3.c_img, self.upgrade_button_3.rect)
            self.screen.blit(self.upgrade_button_4.c_img, self.upgrade_button_4.rect)
            self.screen.blit(self.upgrade_button_5.c_img, self.upgrade_button_5.rect)

            self.screen.blit(self.upgrade_1_mps_text, self.upgrade_1_mps_text_rect)
            self.screen.blit(self.upgrade_2_mps_text, self.upgrade_2_mps_text_rect)
            self.screen.blit(self.upgrade_3_mps_text, self.upgrade_3_mps_text_rect)
            self.screen.blit(self.upgrade_4_mps_text, self.upgrade_4_mps_text_rect)
            self.screen.blit(self.upgrade_5_mps_text, self.upgrade_5_mps_text_rect)

            self.screen.blit(self.upgrade_1_cost_text, self.upgrade_1_cost_text_rect)
            self.screen.blit(self.upgrade_2_cost_text, self.upgrade_2_cost_text_rect)
            self.screen.blit(self.upgrade_3_cost_text, self.upgrade_3_cost_text_rect)
            self.screen.blit(self.upgrade_4_cost_text, self.upgrade_4_cost_text_rect)
            self.screen.blit(self.upgrade_5_cost_text, self.upgrade_5_cost_text_rect)


    # Input Function
    def inputs(self):
        if self.game_state == 1:
            if self.menu.click():
                if self.menu_panel.visibility:
                    self.menu_panel.visibility = False
                elif not self.menu_panel.visibility:
                    self.menu_panel.visibility = True

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

    def human_format(self, num):
        self.num = num
        self.num = float('{:.3g}'.format(self.num))
        magnitude = 0
        while abs(self.num) >= 1000:
            magnitude += 1
            self.num /= 1000.0
        return '{}{}'.format('{:f}'.format(self.num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

pygame.init()
game = Game()
game.run()
