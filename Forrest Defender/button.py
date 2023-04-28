#---imports---
import pygame
from colors import *


#---create button class
class Button():
    def __init__(self, x, y, image, pressed_image, scale):
        width = image.get_width() #gets the width of image
        height = image.get_height() #gets the height of image
        self.d_image = pygame.transform.scale(image, (int(width * scale), int(height * scale))) #assigns image
        self.p_image = pygame.transform.scale(pressed_image, (int(width * scale), int(height * scale)))
        self.c_img = None
        self.rect = self.p_image.get_rect() #creates rectangle for image
        self.rect.topleft = (x, y) #sets image location
        self.clicked = False #starts not clicked
        self.action = False
    def click(self):
        self.action = False
        #get mouse pos
        pos = pygame.mouse.get_pos() #gets the coordinates of the mouse
        #print(pos) #used for testing
        
        #check if mouse is over a button and clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #0 is the left mouse button being clicked
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0 and self.clicked: #if button let go, reset
                self.clicked = False
                self.action = True

        return self.action


