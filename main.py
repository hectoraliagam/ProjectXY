import pygame as pg 
from colors import *
import sys

pg.init()

info = pg.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
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

class Circulo:
    def __init__(self, x, y, radius, color, border):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.border = border
    def draw(self, surface):
        pg.draw.circle(surface, self.color, (self.x, self.y), self.radius, self.border)
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

window = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
pg.display.set_caption('ProjectXY')
window.fill(Azul_Púrpura)

cuadrado = Rectangulo(300, 300, 40, 20, Rojo_Naranja, 3)
circulo = Circulo(150, 150, 20, Verde_Bosque, 3)

clock = pg.time.Clock()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
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

    dx, dy = 0, 0
    if keys[pg.K_LEFT] and circulo.x - circulo.radius > 0:
        dx = -SPEED
    if keys[pg.K_RIGHT] and circulo.x + circulo.radius < WIDTH:
        dx = SPEED
    if keys[pg.K_UP] and circulo.y - circulo.radius > 0:
        dy = -SPEED
    if keys[pg.K_DOWN] and circulo.y + circulo.radius < HEIGHT:
        dy = SPEED
    circulo.move(dx, dy)

    window.fill(Azul_Púrpura)
    cuadrado.draw(window)
    circulo.draw(window)

    pg.display.flip()
    clock.tick(60)