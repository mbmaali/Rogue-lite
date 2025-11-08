import pygame
from sprites import Player,Enemy
import random


pygame.init()



WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rogue Lite")



player = Player(WIDTH // 2, HEIGHT // 2)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


enemy_group = pygame.sprite.Group()

enemy_x = random.randint(0,WIDTH)
enemy_y = random.randint(0, HEIGHT)
enemy= Enemy(enemy_x,enemy_y)


enemy_group.add(enemy)
all_sprites.add(enemy)



clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()




