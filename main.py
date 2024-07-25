import pygame as pg
import sys

SCREEN_RATIO = 16 / 9
SPEED = 5
GRAVITY = 1
JUMP_STRENGTH = 25
GRID_SIZE = 50
FONT_SIZE = 20

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
CERÚLEO_O_AZUR = (0, 191, 255)
VERDE_ESTÁNDAR = (0, 128, 0)
GRIS = (128, 128, 128)
MARRON = (139, 69, 19)
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
        self.width = width
        self.height = height

    def draw(self, surface):
        font = pg.font.Font(None, FONT_SIZE)
        for x in range(0, self.width, self.grid_size):
            pg.draw.line(surface, self.line_color, (x, 0), (x, self.height))
            label = font.render(f'{x}', True, self.text_color)
            surface.blit(label, (x + 2, 2))
        for y in range(0, self.height, self.grid_size):
            pg.draw.line(surface, self.line_color, (0, y), (self.width, y))
            label = font.render(f'{y}', True, self.text_color)
            surface.blit(label, (2, y + 2))

class Plataforma(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Text(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, bg_color, text_color, content):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.image.fill(bg_color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.text_color = text_color
        self.content = content

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        font = pg.font.Font(None, FONT_SIZE)
        text = font.render(self.content, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

class Bloque(pg.sprite.Sprite):
    def __init__(self, x, y, size, color, destruction_points, arbol=None):
        super().__init__()
        self.image = pg.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.destruction_points = destruction_points
        self.current_points = destruction_points
        self.is_damaging = False
        self.arbol = arbol
        self.destruction_speed = 1

    def update_life(self, destruction_direction):
        if destruction_direction == 'vertical':
            self.destruction_speed = 2
        else:
            self.destruction_speed = 1

        keys = pg.key.get_pressed()
        if keys[pg.K_b] and (keys[pg.K_LEFT] or keys[pg.K_RIGHT] or keys[pg.K_SPACE] or keys[pg.K_DOWN]):
            self.is_damaging = True
        else:
            self.is_damaging = False

        if self.is_damaging:
            self.current_points -= self.destruction_speed
            if self.current_points <= 0:
                self.current_points = 0
                if self.arbol:
                    self.arbol.destroy()
                self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        font = pg.font.Font(None, FONT_SIZE)
        if self.destruction_points > 0:
            percentage = (self.current_points / self.destruction_points) * 100
            text = font.render(f'{int(percentage)}%', True, BLANCO)
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)

class Tierra(Bloque):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, VERDE_ESTÁNDAR, 300)

class Piedra(Bloque):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, GRIS, 1000)

class Madera(Bloque):
    def __init__(self, x, y, size, arbol=None):
        super().__init__(x, y, size, MARRON, 500, arbol)

class Arbol:
    def __init__(self, x, y, size):
        self.bloques = [
            Madera(x, y, size, self),
            Madera(x, y - size, size, self),
            Madera(x, y - 2 * size, size, self)
        ]

    def destroy(self):
        for bloque in self.bloques:
            bloque.kill()

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

        if self.is_jumping and self.rect.y <= self.jump_start_y - 50:
            self.vel_y = 0
            self.is_jumping = False

    def reset_position(self, x, y):
        self.rect.topleft = (x, y)
        self.vel_x = self.vel_y = 0
        self.on_platform = False
        self.jumps_left = 1
        self.is_jumping = False

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class CollisionChecker:
    @staticmethod
    def check_horizontal_collision(sprite, platforms):
        collisions = pg.sprite.spritecollide(sprite, platforms, False)
        for obj in collisions:
            if sprite.vel_x > 0:
                if sprite.rect.right > obj.rect.left and sprite.rect.left < obj.rect.right:
                    sprite.rect.right = obj.rect.left
                    sprite.vel_x = 0
                    CollisionChecker.handle_destruction(sprite, obj, 'horizontal')
            elif sprite.vel_x < 0:
                if sprite.rect.left < obj.rect.right and sprite.rect.right > obj.rect.left:
                    sprite.rect.left = obj.rect.right
                    sprite.vel_x = 0
                    CollisionChecker.handle_destruction(sprite, obj, 'horizontal')

    @staticmethod
    def check_vertical_collision(sprite, platforms):
        sprite.on_platform = False
        collisions = pg.sprite.spritecollide(sprite, platforms, False)
        for obj in collisions:
            if sprite.vel_y > 0:
                if sprite.rect.bottom > obj.rect.top and sprite.rect.top < obj.rect.bottom:
                    sprite.rect.bottom = obj.rect.top
                    sprite.vel_y = 0
                    sprite.on_platform = True
                    sprite.jumps_left = 1
                    CollisionChecker.handle_destruction(sprite, obj, 'vertical')
            elif sprite.vel_y < 0:
                if sprite.rect.top < obj.rect.bottom and sprite.rect.bottom > obj.rect.top:
                    sprite.rect.top = obj.rect.bottom
                    sprite.vel_y = 0
                    CollisionChecker.handle_destruction(sprite, obj, 'vertical')

    @staticmethod
    def handle_destruction(sprite, obj, destruction_direction):
        if isinstance(obj, Bloque):
            obj.update_life(destruction_direction)

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
    tierra1 = Tierra(700, 650, 50)
    tierra2 = Tierra(600, 600, 50)
    tierra3 = Tierra(900, 650, 50)
    tierra4 = Tierra(500, 650, 50)
    tierra5 = Tierra(450, 600, 50)
    tierra6 = Tierra(350, 650, 50)
    piedra1 = Piedra(750, 650, 50)
    piedra2 = Piedra(800, 650, 50)
    arbol1 = Arbol(400, 650, 50)
    cuadro_texto = Text(100, 100, 1000, 20, NEGRO, CERÚLEO_O_AZUR, 'Texto inicial')

    jugador = Jugador(WIDTH // 2, HEIGHT // 2, 25, 50, CERÚLEO_O_AZUR)

    plataformas = [plataforma, tierra1, tierra2, tierra3, tierra4, tierra5, tierra6, piedra1, piedra2]
    arboles = arbol1.bloques
    all_sprites.add(*plataformas, jugador, cuadro_texto, *arboles)
    platforms.add(*plataformas, *arboles)

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
        CollisionChecker.check_horizontal_collision(jugador, platforms)

        jugador.move(0, jugador.vel_y)
        CollisionChecker.check_vertical_collision(jugador, platforms)

        if jugador.rect.top > HEIGHT:
            jugador.reset_position(WIDTH // 2, HEIGHT // 2)

        window.fill(BLANCO)
        cuadricula.draw(window)

        for sprite in all_sprites:
            sprite.draw(window)

        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
