import pygame as pg
import sys

SCREEN_RATIO = 16 / 9
pg.init()
info = pg.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
WIDTH = SCREEN_WIDTH
HEIGHT = int(SCREEN_WIDTH / SCREEN_RATIO)
SPEED = 5
GRAVITY = 0.5
JUMP_STRENGTH = 15
GRID_SIZE = 50
FONT_SIZE = 20

Blanco = (255, 255, 255)
Negro = (0, 0, 0)
Rojo_Naranja = (255, 69, 0)
Verde_Estandar = (0, 128, 0)
Granate = (128, 0, 0)
Vino = (139, 0, 0)

class Cuadricula:
    def __init__(self, grid_size, line_color, text_color, width, height):
        self.grid_size = grid_size
        self.line_color = line_color
        self.text_color = text_color
        self.font = pg.font.Font(None, FONT_SIZE)
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

class Jugador(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.vel_x = 0
        self.vel_y = 0
        self.jumps_left = 1
        self.on_platform = False
        self.is_jumping = False
        self.jump_start_y = 0

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def jump(self):
        if self.on_platform or self.jumps_left > 0:
            self.vel_y = -JUMP_STRENGTH
            self.jump_start_y = self.rect.y
            self.jumps_left -= 1
            self.is_jumping = True
            self.on_platform = False

    def apply_gravity(self):
        if not self.on_platform:
            self.vel_y += GRAVITY

        # Limit the maximum height of the jump
        if self.is_jumping and self.rect.y <= self.jump_start_y - 25:
            self.vel_y = 0
            self.is_jumping = False

    def reset_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.on_platform = False
        self.jumps_left = 1
        self.is_jumping = False

class Plataforma(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.rect = pg.Rect(x, y, width, height)
        self.color = color

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect)

class Tierra(pg.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.rect = pg.Rect(x, y, size, size)
        self.color = Verde_Estandar

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect)

class CollisionChecker:
    @staticmethod
    def check_collision(rect, objects):
        rect.on_platform = False
        for obj in objects:
            if rect.rect.colliderect(obj.rect):
                if rect.vel_y > 0 and rect.rect.bottom <= obj.rect.top + abs(rect.vel_y):
                    rect.rect.bottom = obj.rect.top
                    rect.vel_y = 0
                    rect.on_platform = True
                    rect.jumps_left = 1
                elif rect.vel_y < 0 and rect.rect.top >= obj.rect.bottom:
                    rect.rect.top = obj.rect.bottom
                    rect.vel_y = 0

                if rect.vel_x > 0 and rect.rect.right > obj.rect.left and rect.rect.left < obj.rect.left:
                    rect.rect.right = obj.rect.left
                    rect.vel_x = 0
                elif rect.vel_x < 0 and rect.rect.left < obj.rect.right and rect.rect.right > obj.rect.right:
                    rect.rect.left = obj.rect.right
                    rect.vel_x = 0

def handle_input(jugador):
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        jugador.vel_x = -SPEED
    elif keys[pg.K_RIGHT]:
        jugador.vel_x = SPEED
    else:
        jugador.vel_x = 0

    if keys[pg.K_SPACE]:
        jugador.jump()

    if keys[pg.K_ESCAPE]:
        pg.quit()
        sys.exit()

def main():
    pg.init()
    window = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
    pg.display.set_caption('ProjectXY')

    plataformas = [
        Plataforma(300, 700, 1000, 20, Negro)
    ]

    tierra_bajo_plataforma = Tierra(700, 675, 25)
    jugador = Jugador(WIDTH // 2, HEIGHT // 2, 40, 40, Rojo_Naranja)
    cuadricula = Cuadricula(GRID_SIZE, Granate, Vino, WIDTH, HEIGHT)
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        handle_input(jugador)

        jugador.apply_gravity()

        jugador.move(jugador.vel_x, 0)
        CollisionChecker.check_collision(jugador, plataformas + [tierra_bajo_plataforma])

        jugador.move(0, jugador.vel_y)
        CollisionChecker.check_collision(jugador, plataformas + [tierra_bajo_plataforma])

        if jugador.rect.top > HEIGHT:
            jugador.reset_position(WIDTH // 2, HEIGHT // 2)

        window.fill(Blanco)
        cuadricula.draw(window)
        for plataforma in plataformas:
            plataforma.draw(window)
        tierra_bajo_plataforma.draw(window)
        jugador.draw(window)

        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
