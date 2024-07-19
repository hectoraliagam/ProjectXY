import pygame as pg
import sys
import config
from colors import *
from entities import Rectangulo, Cuadricula
from collision import CollisionChecker

pg.init()

info = pg.display.Info()
MONITOR_WIDTH = info.current_w
MONITOR_HEIGHT = info.current_h

if MONITOR_WIDTH / MONITOR_HEIGHT >= config.SCREEN_RATIO:
    WIDTH = int(MONITOR_HEIGHT * config.SCREEN_RATIO)
    HEIGHT = MONITOR_HEIGHT
else:
    WIDTH = MONITOR_WIDTH
    HEIGHT = int(MONITOR_WIDTH / config.SCREEN_RATIO)

def main():
    window = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
    pg.display.set_caption('ProjectXY')
    window.fill(Blanco)

    platforms = [
        Rectangulo(WIDTH // 2 - 100, HEIGHT - 50, 200, 20, Azul_Acero, 0),
        Rectangulo(WIDTH // 4, HEIGHT - 150, 150, 20, Verde_Claro, 0),
        Rectangulo(WIDTH - 300, HEIGHT - 250, 150, 20, Aguamarina, 0),
        Rectangulo(WIDTH // 2 - 200, HEIGHT - 300, 100, 20, Rosado, 0),
        Rectangulo(WIDTH // 2 + 150, HEIGHT - 400, 100, 20, Amatista, 0),
        Rectangulo(WIDTH // 3 - 50, HEIGHT - 500, 120, 20, Amarillo, 0),
        Rectangulo(WIDTH // 2 - 50, HEIGHT - 600, 120, 20, Naranja, 0)
    ]

    cuadrado = Rectangulo(WIDTH // 2, HEIGHT // 2, 40, 20, Rojo_Naranja, 3)
    cuadricula = Cuadricula(config.GRID_SIZE, Granate, Vino, WIDTH, HEIGHT)
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
                    cuadrado.jump()

        keys = pg.key.get_pressed()
        dx, dy = 0, 0
        if keys[pg.K_LEFT] and cuadrado.rect.left > 0:
            dx = -config.SPEED
        if keys[pg.K_RIGHT] and cuadrado.rect.right < WIDTH:
            dx = config.SPEED
        if keys[pg.K_DOWN] and cuadrado.on_platform:
            cuadrado.on_platform = False
            cuadrado.rect.y += 1

        cuadrado.move(dx, dy)
        cuadrado.apply_gravity()
        CollisionChecker.check_collision(cuadrado, platforms)

        if cuadrado.rect.top > HEIGHT:
            cuadrado.reset_position()

        window.fill(Blanco)
        cuadricula.draw(window)
        for platform in platforms:
            platform.draw(window)
        cuadrado.draw(window)

        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()