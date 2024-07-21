import pygame as pg
import sys

SCREEN_RATIO = 16 / 9
SPEED = 5
GRAVITY = 0.5
JUMP_STRENGTH = 15
GRID_SIZE = 50
FONT_SIZE = 20

DESTRUCTION_TIME_TIERRA = 3000  # 3 segundos en milisegundos para destruir tierra
DESTRUCTION_TIME_PIEDRA = 10000  # 10 segundos en milisegundos para destruir piedra

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
CERÚLEO_O_AZUR = (0, 191, 255)
VERDE_ESTÁNDAR = (0, 128, 0)
GRIS = (128, 128, 128)
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
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

class Bloque(pg.sprite.Sprite):
    def __init__(self, x, y, size, color):
        super().__init__()
        self.image = pg.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

class Tierra(Bloque):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, VERDE_ESTÁNDAR)

class Piedra(Bloque):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, GRIS)

class Jugador(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_x = 0
        self.vel_y = 0
        self.jumps_left = 1
        self.on_platform = False
        self.is_jumping = False
        self.jump_start_y = 0
        self.destruction_timer_start = 0
        self.current_block = None

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
    def check_collision(sprite, platforms):
        sprite.on_platform = False
        collisions = pg.sprite.spritecollide(sprite, platforms, False)

        for obj in collisions:
            if sprite.vel_y > 0 and sprite.rect.bottom <= obj.rect.top + abs(sprite.vel_y):
                sprite.rect.bottom = obj.rect.top
                sprite.vel_y = 0
                sprite.on_platform = True
                sprite.jumps_left = 1
            elif sprite.vel_y < 0 and sprite.rect.top >= obj.rect.bottom:
                sprite.rect.top = obj.rect.bottom
                sprite.vel_y = 0

            if sprite.vel_x > 0 and sprite.rect.right > obj.rect.left and sprite.rect.right - sprite.vel_x <= obj.rect.left:
                sprite.rect.right = obj.rect.left
                sprite.vel_x = 0
                return obj  # Return the object collided with on the right
            elif sprite.vel_x < 0 and sprite.rect.left < obj.rect.right and sprite.rect.left - sprite.vel_x >= obj.rect.right:
                sprite.rect.left = obj.rect.right
                sprite.vel_x = 0
                return None
        return None

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

    all_sprites = pg.sprite.Group()
    platforms = pg.sprite.Group()

    plataforma = Plataforma(300, 700, 1000, 20, NEGRO)
    tierra = Tierra(700, 675, 25)
    piedra = Piedra(750, 675, 25)
    jugador = Jugador(WIDTH // 2, HEIGHT // 2, 20, 40, CERÚLEO_O_AZUR)

    all_sprites.add(plataforma, tierra, piedra, jugador)
    platforms.add(plataforma, tierra, piedra)

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
        collided_obj = CollisionChecker.check_collision(jugador, platforms)

        jugador.move(0, jugador.vel_y)
        CollisionChecker.check_collision(jugador, platforms)

        if jugador.rect.top > HEIGHT:
            jugador.reset_position(WIDTH // 2, HEIGHT // 2)

        keys = pg.key.get_pressed()
        if collided_obj and keys[pg.K_b]:
            if jugador.destruction_timer_start == 0 or jugador.current_block != collided_obj:
                jugador.destruction_timer_start = pg.time.get_ticks()
                jugador.current_block = collided_obj
            else:
                destruction_time = DESTRUCTION_TIME_TIERRA if isinstance(collided_obj, Tierra) else DESTRUCTION_TIME_PIEDRA
                if pg.time.get_ticks() - jugador.destruction_timer_start >= destruction_time:
                    collided_obj.kill()
                    jugador.destruction_timer_start = 0
                    jugador.current_block = None
        else:
            jugador.destruction_timer_start = 0
            jugador.current_block = None

        window.fill(BLANCO)
        cuadricula.draw(window)
        all_sprites.draw(window)

        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
