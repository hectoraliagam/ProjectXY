import pygame as pg
import sys
import config
from colors import *
from entities import Rectangulo, Cuadricula
from platforms import Tierra, Platform
from collision import CollisionChecker

def main():
    window = pg.display.set_mode((config.WIDTH, config.HEIGHT), pg.FULLSCREEN)
    pg.display.set_caption('ProjectXY')
    window.fill(Blanco)

    plataformas = [
        Platform(config.WIDTH // 2 - 100, config.HEIGHT - 50, 200, 20, Azul_Acero, 0),
        Platform(config.WIDTH // 4, config.HEIGHT - 150, 150, 20, Verde_Claro, 0),
        Platform(config.WIDTH - 300, config.HEIGHT - 250, 150, 20, Aguamarina, 0),
        Platform(config.WIDTH // 2 - 200, config.HEIGHT - 300, 100, 20, Rosado, 0),
        Platform(config.WIDTH // 2 + 150, config.HEIGHT - 400, 100, 20, Amatista, 0),
        Platform(config.WIDTH // 3 - 50, config.HEIGHT - 500, 120, 20, Amarillo, 0),
        Platform(config.WIDTH // 2 - 50, config.HEIGHT - 600, 120, 20, Naranja, 0)
    ]

    tierra = Tierra(config.WIDTH // 2, config.HEIGHT - 100, 25)
    personaje = Rectangulo(config.WIDTH // 2, config.HEIGHT // 2, 40, 40, Rojo_Naranja, 3)
    cuadricula = Cuadricula(config.GRID_SIZE, Granate, Vino, config.WIDTH, config.HEIGHT)
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
                    personaje.jump()

        keys = pg.key.get_pressed()
        dx, dy = 0, 0
        if keys[pg.K_LEFT] and personaje.rect.left > 0:
            dx = -config.SPEED
        if keys[pg.K_RIGHT] and personaje.rect.right < config.WIDTH:
            dx = config.SPEED
        if keys[pg.K_DOWN] and personaje.on_platform:
            personaje.on_platform = False
            personaje.rect.y += 1

        personaje.move(dx, dy)
        personaje.apply_gravity()
        CollisionChecker.check_collision(personaje, plataformas + [tierra])

        if personaje.rect.top > config.HEIGHT:
            personaje.reset_position()

        window.fill(Blanco)
        cuadricula.draw(window)
        for plataforma in plataformas:
            plataforma.draw(window)
        tierra.draw(window)
        personaje.draw(window)

        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
