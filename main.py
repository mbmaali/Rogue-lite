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

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

game_state = "PLAYING"


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # restart
                player = Player(WIDTH // 2, HEIGHT // 2)
                all_sprites = pygame.sprite.Group()
                all_sprites.add(player)

                enemy_group = pygame.sprite.Group()
                
                enemy_x = random.randint(0, WIDTH)
                enemy_y = random.randint(0, HEIGHT)
                enemy = Enemy(enemy_x, enemy_y)

                enemy_group.add(enemy)
                all_sprites.add(enemy)

                game_state = "PLAYING"

    if game_state == "PLAYING":
        all_sprites.update()

        hits = pygame.sprite.spritecollide(player, enemy_group, False)
        if hits:
            game_state = "GAME_OVER"

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)

    elif game_state == "GAME_OVER":
        screen.fill((150, 0, 0))

        text_surface = font.render("GAME OVER", True, (255, 255, 255))
        restart_surface = small_font.render("press R to restart the game", True, (255, 255, 255))

        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(restart_surface, (WIDTH // 2 - restart_surface.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()