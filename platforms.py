import pygame as pg
from colors import Marrón_o_Pardo

class Tierra(pg.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.rect = pg.Rect(x, y, size, size)
        self.color = Marrón_o_Pardo

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect)

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color, border):
        super().__init__()
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.border = border

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect, self.border)
