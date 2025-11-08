import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((40, 40))

        self.image.fill((0, 0, 255))


        self.rect = self.image.get_rect()
        self.rect.center = (x, y)