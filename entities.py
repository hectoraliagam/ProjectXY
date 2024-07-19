import pygame as pg
from colors import *
import config

class Drawable:
    def draw(self, surface):
        raise NotImplementedError

class Movable:
    def move(self, dx, dy):
        raise NotImplementedError

class GravityAffected:
    def apply_gravity(self):
        raise NotImplementedError

class Resettable:
    def reset_position(self):
        raise NotImplementedError

class Rectangulo(Drawable, Movable, GravityAffected, Resettable):
    def __init__(self, x, y, width, height, color, border):
        self.initial_x = x
        self.initial_y = y
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.border = border
        self.vel_y = 0
        self.on_platform = False
        self.jumps_left = 2

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect, self.border)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def apply_gravity(self):
        if not self.on_platform:
            self.vel_y += config.GRAVITY
        self.rect.y += self.vel_y

    def jump(self):
        if self.on_platform or self.jumps_left > 0:
            self.vel_y = -config.JUMP_STRENGTH
            self.on_platform = False
            self.jumps_left -= 1

    def reset_position(self):
        self.rect.x = self.initial_x
        self.rect.y = self.initial_y
        self.vel_y = 0
        self.on_platform = False
        self.jumps_left = 2

class Cuadricula(Drawable):
    def __init__(self, grid_size, line_color, text_color, width, height):
        self.grid_size = grid_size
        self.line_color = line_color
        self.text_color = text_color
        self.font = pg.font.Font(None, config.FONT_SIZE)
        self.width = width
        self.height = height

    def draw(self, surface):
        for x in range(0, self.width, self.grid_size):
            pg.draw.line(surface, self.line_color, (x, 0), (x, self.height))
            label = self.font.render(f'{x}', True, self.text_color)
            surface.blit(label, (x + 2, 2))
        for y in range(0, self.height, self.grid_size):
            pg.draw.line(surface, self.line_color, (0, y), (self.width, y))
            label = self.font.render(f'{y}', True, self.text_color)
            surface.blit(label, (2, y + 2))