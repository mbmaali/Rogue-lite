import pygame
import random
import math


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill((120, 120, 120))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Stairs(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill((255, 255, 80))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, p_type):
        super().__init__()
        self.type = p_type
        self.image = pygame.Surface((20, 20))
        
        if self.type == 'health':
            self.image.fill((0, 255, 0))
        elif self.type == 'speed':
            self.image.fill((255, 255, 0))
            
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((random.randint(2, 5), random.randint(2, 5)))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.lifetime = random.randint(15, 30)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, sword_damage, sword_cooldown_max, screen_width, screen_height):
        super().__init__()

        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 0, 255)) 

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.vx = 0
        self.vy = 0
        
        self.base_speed = speed
        self.speed = self.base_speed
        self.speed_boost_timer = 0
        self.invincible_timer = 60

        
        self.health = 100
        self.max_health = 100

        
        self.facing = 'right'

        
        self.sword_cooldown = 0
        self.sword_cooldown_max = sword_cooldown_max 
        self.sword_damage = sword_damage 
        
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.xp = 0
        self.level = 1
        self.xp_to_next_level = 100

    def update(self, enemy_group=None, wall_group=None):
        
        self.image.set_alpha(255)
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            if (self.invincible_timer // 3) % 2 == 0:
                self.image.set_alpha(100)
    
        if self.speed_boost_timer > 0:
            self.speed = self.base_speed * 1.5
            self.speed_boost_timer -= 1
        else:
            self.speed = self.base_speed
    
    
        keys = pygame.key.get_pressed()

        self.vx = 0
        self.vy = 0

        if keys[pygame.K_w]:
            self.vy = -self.speed
            self.facing = 'up'
        if keys[pygame.K_a]:
            self.vx = -self.speed
            self.facing = 'left'
        if keys[pygame.K_s]:
            self.vy = self.speed
            self.facing = 'down'
        if keys[pygame.K_d]:
            self.vx = self.speed
            self.facing = 'right'
            
        
        if self.vx != 0 and self.vy != 0:
            self.vx /= math.sqrt(2)
            self.vy /= math.sqrt(2)

        self.rect.x += self.vx
        if wall_group:
            hits = pygame.sprite.spritecollide(self, wall_group, False)
            if hits:
                if self.vx > 0:
                    self.rect.right = hits[0].rect.left
                if self.vx < 0:
                    self.rect.left = hits[0].rect.right

        self.rect.y += self.vy
        if wall_group:
            hits = pygame.sprite.spritecollide(self, wall_group, False)
            if hits:
                if self.vy > 0:
                    self.rect.bottom = hits[0].rect.top
                if self.vy < 0:
                    self.rect.top = hits[0].rect.bottom
        
        if self.sword_cooldown > 0:
            self.sword_cooldown -= 1

        
        if enemy_group is not None:
            if keys[pygame.K_SPACE] and self.sword_cooldown <= 0:
                
                self.sword_cooldown = self.sword_cooldown_max
                
                hw = 40 
                hh = 40 
                if self.facing == 'right':
                    hit_box = pygame.Rect(self.rect.right, self.rect.centery - hh // 2, hw, hh)
                elif self.facing == 'left':
                    hit_box = pygame.Rect(self.rect.left - hw, self.rect.centery - hh // 2, hw, hh)
                elif self.facing == 'up':
                    hit_box = pygame.Rect(self.rect.centerx - hw // 2, self.rect.top - hh, hw, hh)
                else:  
                    hit_box = pygame.Rect(self.rect.centerx - hw // 2, self.rect.bottom, hw, hh)
                
                for enemy in enemy_group:
                    if hit_box.colliderect(enemy.rect):
                        
                        enemy.health -= self.sword_damage
        
        
        if self.xp >= self.xp_to_next_level:
            self.level += 1
            self.xp = self.xp - self.xp_to_next_level
            self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
            self.max_health += 20
            self.health = self.max_health


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, chase_radius, health, screen_width, screen_height):
        super().__init__()

        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 0, 0)) 

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.vx = 0
        self.vy = 0
        self.speed = speed 
        self.chase_radius = chase_radius 
        self.wander_timer = 0
        
        self.health = health 
        self.max_health = health 
        
        
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, player, wall_group=None):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)

        if dist < self.chase_radius and dist != 0:
            
            dx /= dist
            dy /= dist
            self.vx = dx * self.speed
            self.vy = dy * self.speed
        else:
            
            self.wander()

        
        self.rect.x += self.vx
        if wall_group:
            hits = pygame.sprite.spritecollide(self, wall_group, False)
            if hits:
                if self.vx > 0:
                    self.rect.right = hits[0].rect.left
                if self.vx < 0:
                    self.rect.left = hits[0].rect.right

        self.rect.y += self.vy
        if wall_group:
            hits = pygame.sprite.spritecollide(self, wall_group, False)
            if hits:
                if self.vy > 0:
                    self.rect.bottom = hits[0].rect.top
                if self.vy < 0:
                    self.rect.top = hits[0].rect.bottom

    def wander(self):
        self.wander_timer -= 1
        if self.wander_timer <= 0:
            angle = random.uniform(0, math.tau)
            
            self.vx = math.cos(angle) * self.speed * 0.5
            self.vy = math.sin(angle) * self.speed * 0.5
            self.wander_timer = random.randint(30, 120)


class Tank(Enemy):
    def __init__(self, x, y, speed, chase_radius, health, screen_width, screen_height):
        
        super().__init__(x, y, speed * 0.5, chase_radius, health * 3, screen_width, screen_height)
        
        self.image = pygame.Surface((48, 48))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(center=(x,y))
        
        self.health = health * 3
        self.max_health = health * 3


class Shooter(Enemy):
    def __init__(self, x, y, speed, chase_radius, health, screen_width, screen_height):
        super().__init__(x, y, speed, chase_radius, health, screen_width, screen_height)
        self.image.fill((0, 150, 0))
        self.shoot_cooldown = 0
        self.shoot_cooldown_max = 120
        self.flee_radius = 150
        self.enemy_bullet_speed = 6
        self.action = None
        self.shoot_vx = 0
        self.shoot_vy = 0

    def update(self, player, wall_group=None):
        self.action = None
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        
        if dist > 0:
            norm_dx = dx / dist
            norm_dy = dy / dist
        else:
            norm_dx, norm_dy = 0, 0

        
        if dist < self.flee_radius:
            self.vx = -norm_dx * self.speed * 0.8
            self.vy = -norm_dy * self.speed * 0.8
        
        elif dist < self.chase_radius:
            self.vx = 0
            self.vy = 0
            if self.shoot_cooldown == 0:
                self.action = "shoot"
                self.shoot_vx = norm_dx * self.enemy_bullet_speed
                self.shoot_vy = norm_dy * self.enemy_bullet_speed
                self.shoot_cooldown = self.shoot_cooldown_max
        else:
            self.wander()

        
        self.rect.x += self.vx
        if wall_group:
            hits = pygame.sprite.spritecollide(self, wall_group, False)
            if hits:
                if self.vx > 0:
                    self.rect.right = hits[0].rect.left
                if self.vx < 0:
                    self.rect.left = hits[0].rect.right

        self.rect.y += self.vy
        if wall_group:
            hits = pygame.sprite.spritecollide(self, wall_group, False)
            if hits:
                if self.vy > 0:
                    self.rect.bottom = hits[0].rect.top
                if self.vy < 0:
                    self.rect.top = hits[0].rect.bottom


class Charger(Enemy):
    def __init__(self, x, y, speed, chase_radius, health, screen_width, screen_height):
        super().__init__(x, y, speed, chase_radius, health, screen_width, screen_height)
        self.image.fill((200, 100, 0))
        self.state = 'wander'
        self.charge_timer = 0
        self.charge_duration = 45
        self.charge_cooldown = 0
        self.charge_cooldown_max = 180
        self.charge_vx = 0
        self.charge_vy = 0

    def update(self, player, wall_group=None):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        
        if dist > 0:
            norm_dx = dx / dist
            norm_dy = dy / dist
        else:
            norm_dx, norm_dy = 0, 0

        if self.charge_cooldown > 0:
            self.charge_cooldown -= 1

        
        if self.state == 'wander':
            self.wander()
            if dist < self.chase_radius and self.charge_cooldown == 0:
                self.state = 'pre_charge'
                self.charge_timer = 30 
                self.vx, self.vy = 0, 0
                self.charge_vx = norm_dx * self.speed * 3
                self.charge_vy = norm_dy * self.speed * 3
        
        elif self.state == 'pre_charge':
            self.image.fill((255, 150, 0))
            self.charge_timer -= 1
            if self.charge_timer <= 0:
                self.state = 'charge'
                self.charge_timer = self.charge_duration
        
        elif self.state == 'charge':
            self.image.fill((200, 100, 0))
            self.vx = self.charge_vx
            self.vy = self.charge_vy
            self.charge_timer -= 1
            if self.charge_timer <= 0:
                self.state = 'wander'
                self.charge_cooldown = self.charge_cooldown_max

        
        self.rect.x += self.vx
        if wall_group:
            hits = pygame.sprite.spritecollide(self, wall_group, False)
            if hits:
                if self.vx > 0:
                    self.rect.right = hits[0].rect.left
                if self.vx < 0:
                    self.rect.left = hits[0].rect.right
                self.vx = 0
                self.state = 'wander'
                self.charge_cooldown = self.charge_cooldown_max

        self.rect.y += self.vy
        if wall_group:
            hits = pygame.sprite.spritecollide(self, wall_group, False)
            if hits:
                if self.vy > 0:
                    self.rect.bottom = hits[0].rect.top
                if self.vy < 0:
                    self.rect.top = hits[0].rect.bottom
                self.vy = 0
                self.state = 'wander'
                self.charge_cooldown = self.charge_cooldown_max


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy, screen_width, screen_height, shot_by_player=True):
        super().__init__()
        
        self.shot_by_player = shot_by_player
        
        if self.shot_by_player:
            self.image = pygame.Surface((8, 8))
            self.image.fill((255, 255, 0)) 
        else:
            self.image = pygame.Surface((10, 10))
            self.image.fill((255, 100, 100))
            
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vx = vx
        self.vy = vy
        
        
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        
        if (
            self.rect.right < 0 or
            self.rect.left > self.screen_width or
            self.rect.bottom < 0 or
            self.rect.top > self.screen_height
        ):
            self.kill()