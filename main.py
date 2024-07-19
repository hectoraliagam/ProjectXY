import pygame as pg 
from colors import *
import sys

pg.init()

info = pg.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
SPEED = 10
GRAVITY = 1
JUMP_STRENGTH = 20
GRID_SIZE = 50
FONT_SIZE = 20

class Rectangulo:
    def __init__(self, x, y, width, height, color, border):
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.border = border
        self.vel_y = 0
    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect, self.border)
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    def aply_gravity(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
    def jump(self):
        self.vel_y = -JUMP_STRENGTH

class Cuadricula:
    def __init__(self, grid_size, line_color, text_color):
        self.grid_size = grid_size
        self.line_color = line_color
        self.text_color = text_color
        self.font = pg.font.Font(None, FONT_SIZE)
    def draw(self, surface):
        for x in range(0, WIDTH, self.grid_size):
            pg.draw.line(surface, self.line_color, (x, 0), (x, HEIGHT))
            label = self.font.render(f'{x}', True, self.text_color)
            surface.blit(label, (x + 2, 2))
        for y in range(0, HEIGHT, self.grid_size):
            pg.draw.line(surface, self.line_color, (0, y), (WIDTH, y))
            label = self.font.render(f'{y}', True, self.text_color)
            surface.blit(label, (2, y + 2))

def check_collision(rect, platform):
    if rect.rect.colliderect(platform.rect) and rect.vel_y > 0:
        rect.rect.bottom = platform.rect.top
        rect.vel_y = 0

window = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
pg.display.set_caption('ProjectXY')

window.fill(Blanco)

platform1 = Rectangulo(WIDTH//2 - 100, HEIGHT - 50, 200, 20, Azul_Acero, 0)

cuadrado = Rectangulo(WIDTH//2, HEIGHT//2, 40, 20, Rojo_Naranja, 3)
cuadricula = Cuadricula(GRID_SIZE, Granate, Vino)

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
            elif event.key == pg.K_SPACE:
                if cuadrado.vel_y == 0:
                    cuadrado.jump()
        
    keys = pg.key.get_pressed()

    dx, dy = 0, 0
    if keys[pg.K_LEFT] and cuadrado.rect.left > 0:
        dx = -SPEED
    if keys[pg.K_RIGHT] and cuadrado.rect.right < WIDTH:
        dx = SPEED
    cuadrado.move(dx, dy)
    cuadrado.aply_gravity()
    check_collision(cuadrado, platform1)

    window.fill(Blanco)
    cuadricula.draw(window)
    platform1.draw(window)
    cuadrado.draw(window)

    pg.display.flip()
    clock.tick(60)