import pygame

class GameObject(pygame.sprite.Sprite):
    def __init__(self,file, pos, scale):
        super().__init__()
        self.rect = pygame.Rect(pos[0], pos[1], scale[0], scale[1])
        self.image = pygame.image.load(file)
