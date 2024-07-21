import pygame as pg
import sys

SCREEN_RATIO = 16 / 9
SPEED = 5
GRAVITY = 0.5
JUMP_STRENGTH = 15
GRID_SIZE = 50
FONT_SIZE = 20

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
CERÚLEO_O_AZUR = (0, 191, 255)
VERDE_ESTÁNDAR = (0, 128, 0)
GRANATE = (128, 0, 0)
VINO = (139, 0, 0)

def setup_screen():
    pg.init()
    info = pg.display.Info()
    screen_width = info.current_w
    screen_height = int(screen_width / SCREEN_RATIO)
    return pg.display.set_mode((screen_width, screen_height), pg.FULLSCREEN), screen_width, screen_height

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
        self.color = VERDE_ESTÁNDAR

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect)

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

        if self.is_jumping and self.rect.y <= self.jump_start_y - 25:
            self.vel_y = 0
            self.is_jumping = False

    def reset_position(self, x, y):
        self.rect.topleft = (x, y)
        self.vel_x = self.vel_y = 0
        self.on_platform = False
        self.jumps_left = 1
        self.is_jumping = False

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

                if rect.vel_x > 0 and rect.rect.right > obj.rect.left and rect.rect.right - rect.vel_x <= obj.rect.left:
                    rect.rect.right = obj.rect.left
                    rect.vel_x = 0
                elif rect.vel_x < 0 and rect.rect.left < obj.rect.right and rect.rect.left - rect.vel_x >= obj.rect.right:
                    rect.rect.left = obj.rect.right
                    rect.vel_x = 0

def handle_input(jugador):
    keys = pg.key.get_pressed()
    jugador.vel_x = SPEED * (keys[pg.K_RIGHT] - keys[pg.K_LEFT])
    if keys[pg.K_SPACE]:
        jugador.jump()
    if keys[pg.K_ESCAPE]:
        pg.quit()
        sys.exit()

def main():
    window, WIDTH, HEIGHT = setup_screen()
    pg.display.set_caption('ProjectXY')

    plataformas = [Plataforma(300, 700, 1000, 20, NEGRO)]
    tierra_bajo_plataforma = Tierra(700, 675, 25)
    jugador = Jugador(WIDTH // 2, HEIGHT // 2, 20, 40, CERÚLEO_O_AZUR)
    cuadricula = Cuadricula(GRID_SIZE, GRANATE, VINO, WIDTH, HEIGHT)
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

        window.fill(BLANCO)
        cuadricula.draw(window)
        for plataforma in plataformas:
            plataforma.draw(window)
        tierra_bajo_plataforma.draw(window)
        jugador.draw(window)

        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
