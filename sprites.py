import pygame



screen_width = 800
screen_hieght = 600


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()


        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 0, 255))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.vx = 0
        self.vy = 0
        self.speed = 1

    def update(self):
        keys = pygame.key.get_pressed()

        self.vx = 0
        self.vy = 0

        if keys[pygame.K_w]:
            self.vy = -self.speed

        if keys[pygame.K_a]:
            self.vx = -self.speed

        if keys[pygame.K_s]:
            self.vy = self.speed



        if keys[pygame.K_d]:
            self.vx = self.speed


        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_hieght:
            self.rect.bottom = screen_hieght



