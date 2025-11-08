import pygame
from sprites import Player


pygame.init()



WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rogue Lite")



player = Player(WIDTH // 2, HEIGHT // 2)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()


