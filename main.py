import pygame as pg
import sys
from colors import *

# Inicialización de pygame
pg.init()

# Configuraciones de pantalla y constantes
info = pg.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
SPEED = 10
GRAVITY = 1
JUMP_STRENGTH = 20
GRID_SIZE = 50
FONT_SIZE = 20

# Clases base
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

# Clase Rectangulo
class Rectangulo(Drawable, Movable, GravityAffected, Resettable):
    def __init__(self, x, y, width, height, color, border):
        self.initial_x = x
        self.initial_y = y
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.border = border
        self.vel_y = 0
        self.on_platform = False
        self.jumps_left = 2  # Número de saltos disponibles

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect, self.border)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def apply_gravity(self):
        if not self.on_platform:
            self.vel_y += GRAVITY
        self.rect.y += self.vel_y

    def jump(self):
        if self.on_platform or self.jumps_left > 0:
            self.vel_y = -JUMP_STRENGTH
            self.on_platform = False
            self.jumps_left -= 1

    def reset_position(self):
        self.rect.x = self.initial_x
        self.rect.y = self.initial_y
        self.vel_y = 0
        self.on_platform = False
        self.jumps_left = 2  # Restablece los saltos disponibles

# Clase Cuadricula
class Cuadricula(Drawable):
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

# Clase CollisionChecker
class CollisionChecker:
    @staticmethod
    def check_collision(rect, platforms):
        rect.on_platform = False
        for platform in platforms:
            if rect.vel_y > 0 and rect.rect.colliderect(platform.rect):
                if rect.rect.bottom <= platform.rect.top + rect.vel_y:
                    rect.rect.bottom = platform.rect.top
                    rect.vel_y = 0
                    rect.on_platform = True
                    rect.jumps_left = 2  # Restablece los saltos disponibles cuando toca una plataforma
                    return platform
        return None

# Función principal
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
                    cuadrado.jump()  # Solicita el salto

        keys = pg.key.get_pressed()
        dx, dy = 0, 0
        if keys[pg.K_LEFT] and cuadrado.rect.left > 0:
            dx = -SPEED
        if keys[pg.K_RIGHT] and cuadrado.rect.right < WIDTH:
            dx = SPEED

        # Movimiento vertical si está en una plataforma y se presiona la tecla hacia abajo
        if keys[pg.K_DOWN] and cuadrado.on_platform:
            cuadrado.on_platform = False
            cuadrado.rect.y += 1

        cuadrado.move(dx, dy)
        cuadrado.apply_gravity()
        CollisionChecker.check_collision(cuadrado, platforms)

        # Reajustar posición si se cae fuera de la pantalla
        if cuadrado.rect.bottom > HEIGHT:
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