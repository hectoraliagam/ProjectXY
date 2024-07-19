import pygame as pg 
from colors import *
import sys

WIDTH = 600
HEIGHT = 600
SPEED = 10

class Rectangulo:
    def __init__(self, x, y, width, height, color, border):
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.border = border
    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect, self.border)
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

pg.init()
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('ProjectXY')
window.fill(Azul_Púrpura)
cuadrado = Rectangulo(300, 300, 40, 20, Rojo_Naranja, 3)
clock = pg.time.Clock()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        
    keys = pg.key.get_pressed()
    dx, dy = 0, 0
    if keys[pg.K_a] and cuadrado.rect.left > 0:
        dx = -SPEED
    if keys[pg.K_d] and cuadrado.rect.right < WIDTH:
        dx = SPEED
    if keys[pg.K_w] and cuadrado.rect.top > 0:
        dy = -SPEED
    if keys[pg.K_s] and cuadrado.rect.bottom < HEIGHT:
        dy = SPEED
    
    cuadrado.move(dx, dy)
    window.fill(Azul_Púrpura)
    cuadrado.draw(window)
    pg.display.flip()
    clock.tick(60)