import pygame
import random
import math
from sprites import Player, Enemy, Projectile, Wall, Stairs, PowerUp, Particle
from map import Dungeon

pygame.init()
pygame.mixer.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rogue Lite")


PLAYER_SPEED = 5
SWORD_DAMAGE = 8
SWORD_COOLDOWN = 20  
BULLET_SPEED = 8


ENEMY_SPEED = 2
ENEMY_HEALTH = 20
CHASE_RADIUS = 250
PROJECTILE_DAMAGE = 5
ENEMY_XP = 15


TILESIZE = 32
MAP_WIDTH = 50
MAP_HEIGHT = 40
MAX_ROMS = 12
ROOM_MIN_SIZE = 6
ROOM_MAX_SIZE = 10



def spawn_enemies(dungeon, enemy_group, all_sprites_group, game_level):
    
    
    for room in dungeon.rooms[1:]: 
        
        num_to_spawn = random.randint(1, 2) + game_level
        for _ in range(num_to_spawn):
            
            enemy_x = random.randint(room.x1, room.x2 - 1) * TILESIZE
            enemy_y = random.randint(room.y1, room.y2 - 1) * TILESIZE

            
            new_health = ENEMY_HEALTH + (game_level * 3)
            new_speed = ENEMY_SPEED + (game_level * 0.2)
            
            enemy = Enemy(enemy_x, enemy_y, new_speed, CHASE_RADIUS, new_health, MAP_WIDTH * TILESIZE, MAP_HEIGHT * TILESIZE)
            enemy_group.add(enemy)
            all_sprites_group.add(enemy)


font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)


try:
    shoot_sound = pygame.mixer.Sound('shoot.wav')
    enemy_hit_sound = pygame.mixer.Sound('enemy_hit.wav')
    player_hit_sound = pygame.mixer.Sound('player_hit.wav')
    level_up_sound = pygame.mixer.Sound('level_up.wav')
    pickup_powerup_sound = pygame.mixer.Sound('pickup_powerup.wav')
    
    pygame.mixer.music.load('music.wav')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(loops=-1)
except FileNotFoundError:
    print("could not load some audio files, game will run without them")
    shoot_sound = None
    enemy_hit_sound = None
    player_hit_sound = None
    level_up_sound = None
    pickup_powerup_sound = None


game_state = "MENU"
game_level = 1
previous_player_level = 1
shake_timer = 0


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        
        x = min(0, x) 
        y = min(0, y) 
        x = max(-(self.width - WIDTH), x) 
        y = max(-(self.height - HEIGHT), y) 
        self.camera = pygame.Rect(x, y, self.width, self.height)



def setup_new_level(game_level, player_obj):
    
    all_sprites = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    projectile_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    stairs_group = pygame.sprite.Group()
    powerup_group = pygame.sprite.Group()
    particle_group = pygame.sprite.Group()

    
    dungeon = Dungeon(MAP_WIDTH, MAP_HEIGHT, MAX_ROMS, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
    dungeon.generate()
    dungeon.create_wall_sprites(TILESIZE, Wall)
    wall_group = dungeon.wall_group
    all_sprites.add(wall_group)

    player_start_pos = (dungeon.player_start_pos[0] * TILESIZE, dungeon.player_start_pos[1] * TILESIZE)
    
    
    if player_obj is None:
        player = Player(player_start_pos[0], player_start_pos[1], PLAYER_SPEED, SWORD_DAMAGE, SWORD_COOLDOWN, MAP_WIDTH * TILESIZE, MAP_HEIGHT * TILESIZE)
        global previous_player_level
        previous_player_level = 1
    else:
        player = player_obj
        player.rect.center = player_start_pos
        player.health = player.max_health
    
    all_sprites.add(player)
    

    stairs_pos = (dungeon.stairs_pos[0] * TILESIZE, dungeon.stairs_pos[1] * TILESIZE)
    stairs = Stairs(stairs_pos[0], stairs_pos[1], TILESIZE)
    all_sprites.add(stairs)
    stairs_group.add(stairs)


    spawn_enemies(dungeon, enemy_group, all_sprites, game_level)

    camera = Camera(MAP_WIDTH * TILESIZE, MAP_HEIGHT * TILESIZE)
    
    return player, all_sprites, enemy_group, projectile_group, wall_group, stairs_group, powerup_group, particle_group, dungeon, camera




clock = pygame.time.Clock()

def draw_ui(surface, player_obj):
    
    
    bar_x = 10
    bar_y = 10
    bar_w = 200
    bar_h = 20
    
    pygame.draw.rect(surface, (150, 0, 0), (bar_x, bar_y, bar_w, bar_h))  

    
    health_pct = max(0, min(1.0, player_obj.health / player_obj.max_health))
    fg_w = int(bar_w * health_pct)
    pygame.draw.rect(surface, (0, 200, 0), (bar_x, bar_y, fg_w, bar_h))  
    
    health_text = small_font.render(f"{int(player_obj.health)} / {player_obj.max_health}", True, (255, 255, 255))
    surface.blit(health_text, (bar_x + bar_w + 8, bar_y - 2))


    
    xp_bar_y = bar_y + bar_h + 5
    pygame.draw.rect(surface, (50, 50, 50), (bar_x, xp_bar_y, bar_w, 15))
    
    if player_obj.xp_to_next_level > 0:
        xp_pct = max(0, min(1.0, player_obj.xp / player_obj.xp_to_next_level))
        xp_w = int(bar_w * xp_pct)
        pygame.draw.rect(surface, (255, 255, 0), (bar_x, xp_bar_y, xp_w, 15))
    
    lvl_text = small_font.render(f"LVL: {player_obj.level}", True, (255, 255, 200))
    surface.blit(lvl_text, (bar_x, xp_bar_y + 20))



player = None
all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
stairs_group = pygame.sprite.Group()
powerup_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()
dungeon = None
camera = None


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "MENU":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_level = 1
                player, all_sprites, enemy_group, projectile_group, wall_group, stairs_group, powerup_group, particle_group, dungeon, camera = setup_new_level(game_level, None)
                game_state = "PLAYING"

        elif game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                
                game_level = 1
                player, all_sprites, enemy_group, projectile_group, wall_group, stairs_group, powerup_group, particle_group, dungeon, camera = setup_new_level(game_level, None)
                game_state = "PLAYING"

        elif game_state == "PLAYING":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                
                
                player_screen_x, player_screen_y = camera.apply(player.rect).center
                
                dx = mx - player_screen_x
                dy = my - player_screen_y

                dist = math.hypot(dx, dy)
                if dist != 0:
                    dx /= dist
                    dy /= dist
                vx = dx * BULLET_SPEED
                vy = dy * BULLET_SPEED
                
                
                bullet = Projectile(player.rect.centerx, player.rect.centery, vx, vy, MAP_WIDTH * TILESIZE, MAP_HEIGHT * TILESIZE)
                all_sprites.add(bullet)
                projectile_group.add(bullet)
                if shoot_sound:
                    shoot_sound.play()

    if game_state == "PLAYING":
        
        
        player.update(enemy_group, wall_group)
        
        if player.level > previous_player_level:
            previous_player_level = player.level
            if level_up_sound:
                level_up_sound.play()
        
        for e in enemy_group:
            e.update(player, wall_group)
        projectile_group.update()
        particle_group.update()
        
        camera.update(player)


        
        
        
        if player.invincible_timer == 0:
            hits = pygame.sprite.spritecollide(player, enemy_group, False)
            if hits:
                
                player.health -= 1
                player.invincible_timer = 30 
                shake_timer = 15
                
                if player_hit_sound:
                    player_hit_sound.play()
                if player.health <= 0:
                    player.health = 0 
                    game_state = "GAME_OVER"

        
        hits = pygame.sprite.groupcollide(enemy_group, projectile_group, False, True)
        for enemy_hit, projectiles_that_hit in hits.items():
            
            enemy_hit.health -= len(projectiles_that_hit) * PROJECTILE_DAMAGE
            if enemy_hit_sound:
                enemy_hit_sound.play()
            if enemy_hit.health <= 0:
                player.xp += ENEMY_XP
                
                for _ in range(random.randint(10, 15)):
                    p = Particle(enemy_hit.rect.centerx, enemy_hit.rect.centery, (255, 0, 0))
                    all_sprites.add(p)
                    particle_group.add(p)
                
                
                if random.random() < 0.1:
                    p_type = random.choice(['health', 'speed'])
                    new_powerup = PowerUp(enemy_hit.rect.centerx, enemy_hit.rect.centery, p_type)
                    all_sprites.add(new_powerup)
                    powerup_group.add(new_powerup)
                
                enemy_hit.kill()
        
        
        proj_wall_hits = pygame.sprite.groupcollide(projectile_group, wall_group, True, False)
        for proj, walls in proj_wall_hits.items():
            for _ in range(random.randint(2, 4)):
                p = Particle(proj.rect.centerx, proj.rect.centery, (255, 255, 0))
                all_sprites.add(p)
                particle_group.add(p)

        
        powerup_hits = pygame.sprite.spritecollide(player, powerup_group, True)
        for hit in powerup_hits:
            if pickup_powerup_sound:
                pickup_powerup_sound.play()
            if hit.type == 'health':
                player.health = min(player.max_health, player.health + 25)
            elif hit.type == 'speed':
                player.speed_boost_timer = 300
        
        
        
        hits = pygame.sprite.spritecollide(player, stairs_group, False)
        if hits:
            game_level += 1
            player, all_sprites, enemy_group, projectile_group, wall_group, stairs_group, powerup_group, particle_group, dungeon, camera = setup_new_level(game_level, player)


        
        if shake_timer > 0:
            camera_offset = (random.randint(-5, 5), random.randint(-5, 5))
            shake_timer -= 1
        else:
            camera_offset = (0, 0)
        
        
        screen.fill((20, 20, 20))
        
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite.rect).move(camera_offset))

        
        for enemy in enemy_group:
            bar_w = enemy.rect.width
            bar_h = 6
            
            bar_rect = pygame.Rect(0, 0, bar_w, bar_h)
            bar_rect.centerx = enemy.rect.centerx
            bar_rect.bottom = enemy.rect.top - 6
            
            
            
            pygame.draw.rect(screen, (120, 0, 0), camera.apply(bar_rect).move(camera_offset)) 
            hp_pct = max(0, min(1.0, enemy.health / enemy.max_health)) 
            fg_w = int(bar_w * hp_pct)
            fg_rect = pygame.Rect(bar_rect.x, bar_rect.y, fg_w, bar_h)
            pygame.draw.rect(screen, (0, 200, 0), camera.apply(fg_rect).move(camera_offset))

        
        draw_ui(screen, player)

    elif game_state == "GAME_OVER":
        screen.fill((150, 0, 0))
        text_surface = font.render("GAME OVER", True, (255, 255, 255))
        restart_surface = small_font.render("Press R to Reestart", True, (255, 255, 255))
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(restart_surface, (WIDTH // 2 - restart_surface.get_width() // 2, HEIGHT // 2 + 20))

    elif game_state == "MENU":
        screen.fill((10, 10, 30))
        title_text = font.render("Rogue Ltie 2", True, (255, 255, 255))
        start_text = small_font.render("Press SPACE to Start", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 20))


    pygame.display.flip()
    clock.tick(60)

pygame.quit()