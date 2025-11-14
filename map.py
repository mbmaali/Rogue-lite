import pygame
import random


class Room:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return (center_x, center_y)

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

class Dungeon:
    def __init__(self, map_w, map_h, max_rooms, min_room, max_room):
        self.map_width = map_w
        self.map_height = map_h
        
        self.max_rooms = max_rooms
        self.min_room_size = min_room
        self.max_room_size = max_room

        self.map_data = []
        self.rooms = []
        self.wall_group = pygame.sprite.Group()
        self.player_start_pos = (0, 0)
        self.stairs_pos = (0, 0)

    def generate(self):
        
        self.map_data = [[1 for _ in range(self.map_width)] for _ in range(self.map_height)]
        self.rooms = []
        
        for r in range(self.max_rooms):
            w = random.randint(self.min_room_size, self.max_room_size)
            h = random.randint(self.min_room_size, self.max_room_size)
            x = random.randint(1, self.map_width - w - 2)
            y = random.randint(1, self.map_height - h - 2)

            new_room = Room(x, y, w, h)
            
            
            self.carve_room(new_room)
            
            if len(self.rooms) == 0:
                self.player_start_pos = new_room.center()
            else:
                
                prev_room = self.rooms[-1]
                self.connect_rooms(new_room, prev_room)

            self.rooms.append(new_room)
            
        
        self.stairs_pos = self.rooms[-1].center()

    def carve_room(self, room):
        for x in range(room.x1, room.x2):
            for y in range(room.y1, room.y2):
                if 0 < x < self.map_width-1 and 0 < y < self.map_height-1:
                    self.map_data[y][x] = 0

    def connect_rooms(self, room1, room2):
        x1, y1 = room1.center()
        x2, y2 = room2.center()

        if random.randint(0, 1) == 1:
            self.carve_h_tunnel(x1, x2, y1)
            self.carve_v_tunnel(y1, y2, x2)
        else:
            self.carve_v_tunnel(y1, y2, x1)
            self.carve_h_tunnel(x1, x2, y2)

    def carve_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if 0 < x < self.map_width-1 and 0 < y < self.map_height-1:
                self.map_data[y][x] = 0

    def carve_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if 0 < x < self.map_width-1 and 0 < y < self.map_height-1:
                self.map_data[y][x] = 0

    def create_wall_sprites(self, TILESIZE, Wall):
        self.wall_group.empty()
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile == 1:
                    wall = Wall(x * TILESIZE, y * TILESIZE, TILESIZE)
                    self.wall_group.add(wall)