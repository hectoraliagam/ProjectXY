import pygame as pg
import sys
import string
import time

SCREEN_RATIO = 16 / 9
SPEED = 3
RUN_SPEED = 6
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
        self.coord_color = GRIS
        self.width = width
        self.height = height

    def get_cell_name(self, col, row):
        letters = string.ascii_uppercase
        row_name = letters[row % len(letters)]
        col_name = str(col + 1)
        return row_name + col_name

    def draw(self, surface):
        font = pg.font.Font(None, FONT_SIZE)
        coord_font = pg.font.Font(None, FONT_SIZE - 5)
        max_rows = self.height // self.grid_size
        max_cols = self.width // self.grid_size

        for x in range(0, self.width, self.grid_size):
            pg.draw.line(surface, self.line_color, (x, 0), (x, self.height))
        for y in range(0, self.height, self.grid_size):
            pg.draw.line(surface, self.line_color, (0, y), (self.width, y))

        for col in range(max_cols):
            coord_x = col * self.grid_size
            coord_text = f'{coord_x}'
            coord_label = coord_font.render(coord_text, True, self.text_color)
            coord_rect = coord_label.get_rect(topleft=(coord_x + 2, 2))
            surface.blit(coord_label, coord_rect)

        for row in range(max_rows):
            coord_y = row * self.grid_size
            coord_text = f'{coord_y}'
            coord_label = coord_font.render(coord_text, True, self.text_color)
            coord_rect = coord_label.get_rect(topleft=(2, coord_y + 2))
            surface.blit(coord_label, coord_rect)

        for row in range(max_rows):
            for col in range(max_cols):
                cell_name = self.get_cell_name(col, row)
                label = font.render(cell_name, True, self.coord_color)
                label_rect = label.get_rect(center=(col * self.grid_size + self.grid_size // 2, row * self.grid_size + self.grid_size // 2))
                surface.blit(label, label_rect)

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
        font = pg.font.Font(None, FONT_SIZE)
        text = font.render(self.content, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(self.image, self.rect.topleft)
        surface.blit(text, text_rect)

class TextoDestruccion(Text):
    def __init__(self, x, y, width, height, bg_color, text_color):
        super().__init__(x, y, width, height, bg_color, text_color, '')
        self.bg_color = bg_color
        self.text_color = text_color
        self.last_update_time = time.time()
        self.update_interval = 2.5

    def actualizar(self, bloque):
        current_time = time.time()
        if bloque and bloque.is_damaging:
            percentage = (bloque.current_points / bloque.destruction_points) * 100
            new_content = f'{bloque.__class__.__name__}: {int(percentage)}%'
            self.last_update_time = current_time
        else:
            if current_time - self.last_update_time > self.update_interval:
                new_content = ''
            else:
                new_content = self.content
        
        if self.content != new_content:
            self.content = new_content

    def draw(self, surface):
        self.image.fill(self.bg_color)
        font = pg.font.Font(None, FONT_SIZE)
        text = font.render(self.content, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(self.image, self.rect.topleft) 
        surface.blit(text, text_rect) 

class Bloque(pg.sprite.Sprite):
    def __init__(self, x, y, size, color, destruction_points):
        super().__init__()
        self.image = pg.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.destruction_points = destruction_points
        self.current_points = destruction_points
        self.is_damaging = False
        self.destruction_speed = 1

    def update_life(self, destruction_direction):
        if self.is_damaging:
            self.destruction_speed = 1
            self.current_points -= self.destruction_speed
            if self.current_points <= 0:
                self.current_points = 0
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
        super().__init__(x, y, size, VERDE_ESTÁNDAR, 150)

class Piedra(Bloque):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, GRIS, 500)

class Madera(Bloque):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, MARRON, 250)

class Jugador(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color, texto_destruccion):
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
        self.is_damaging = False
        self.destruction_direction = None
        self.texto_destruccion = texto_destruccion
        self.is_running = False

    def move(self, dx, dy, platforms):
        if not self.is_running:
            if dx > 0: 
                self.auto_jump(platforms, 'right')
            elif dx < 0: 
                self.auto_jump(platforms, 'left')

        if not self.is_damaging:
            self.rect.x += dx
            self.rect.y += dy

    def auto_jump(self, platforms, direction):
        if not self.is_running and self.on_platform:
            if direction == 'right':
                check_rect = pg.Rect(self.rect.right, self.rect.top, 1, self.rect.height)
            elif direction == 'left':
                check_rect = pg.Rect(self.rect.left - 1, self.rect.top, 1, self.rect.height)
            else:
                return

            for block in platforms:
                if isinstance(block, Bloque) and check_rect.colliderect(block.rect):
                    if direction == 'right':
                        if self.rect.right <= block.rect.left:
                            self.jump()
                            break
                    elif direction == 'left':
                        if self.rect.left >= block.rect.right:
                            self.jump()
                            break

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

    def destroy_adjacent_blocks(self, platforms):
        keys = pg.key.get_pressed()
        if self.on_platform and keys[pg.K_b]:
            self.is_damaging = True
            self.vel_x = 0
            player_cell_x, player_cell_y = get_cell_coordinates(self.rect, GRID_SIZE)

            cell_x = player_cell_x * GRID_SIZE
            cell_y = player_cell_y * GRID_SIZE
            cell_rect = pg.Rect(cell_x, cell_y, GRID_SIZE, GRID_SIZE)

            if cell_rect.contains(self.rect):
                adjacent_x, adjacent_y = cell_x, cell_y
                destruction_direction = None
                
                if keys[pg.K_UP]:
                    adjacent_y -= GRID_SIZE
                    destruction_direction = 'vertical'
                if keys[pg.K_DOWN]:
                    adjacent_y += GRID_SIZE
                    destruction_direction = 'vertical'
                if keys[pg.K_LEFT]:
                    adjacent_x -= GRID_SIZE
                    destruction_direction = 'horizontal'
                if keys[pg.K_RIGHT]:
                    adjacent_x += GRID_SIZE
                    destruction_direction = 'horizontal'

                if destruction_direction:
                    block_rect = pg.Rect(adjacent_x, adjacent_y, GRID_SIZE, GRID_SIZE)
                    blocks_to_destroy = [s for s in platforms if isinstance(s, Bloque) and block_rect.colliderect(s.rect)]

                    if blocks_to_destroy:
                        block = blocks_to_destroy[0]
                        block.is_damaging = True
                        block.update_life(destruction_direction)
                        self.texto_destruccion.actualizar(block)
        else:
            self.is_damaging = False
            self.destruction_direction = None
            for block in platforms:
                if isinstance(block, Bloque):
                    block.is_damaging = False
            self.texto_destruccion.actualizar(None)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

def get_cell_coordinates(rect, grid_size):
    cell_x = rect.x // grid_size
    cell_y = rect.y // grid_size
    return cell_x, cell_y

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

def handle_input(jugador, platforms):
    keys = pg.key.get_pressed()

    if keys[pg.K_b]:
        jugador.vel_x = 0
    else:
        if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
            jugador.is_running = True
            jugador.vel_x = RUN_SPEED * (keys[pg.K_RIGHT] - keys[pg.K_LEFT])
        else:
            jugador.is_running = False
            jugador.vel_x = SPEED * (keys[pg.K_RIGHT] - keys[pg.K_LEFT])

    if not keys[pg.K_b] and keys[pg.K_SPACE] and jugador.on_platform:
        jugador.jump()

    if keys[pg.K_ESCAPE]:
        pg.quit()
        sys.exit()

    jugador.destroy_adjacent_blocks(platforms)

def main():
    window, WIDTH, HEIGHT = setup_screen()
    pg.display.set_caption('ProjectXY')

    all_sprites = pg.sprite.Group()
    platforms = pg.sprite.Group()

    plataforma = Plataforma(100, 700, 1150, 20, NEGRO)
    tierra1 = Tierra(700, 650, 50)
    tierra2 = Tierra(600, 600, 50)
    tierra3 = Tierra(900, 650, 50)
    tierra4 = Tierra(500, 650, 50)
    tierra5 = Tierra(450, 600, 50)
    tierra6 = Tierra(350, 650, 50)
    tierra7 = Tierra(450, 500, 50)
    piedra1 = Piedra(750, 650, 50)
    piedra2 = Piedra(800, 650, 50)
    madera1 = Madera(400, 650, 50)
    cuadro_texto = Text(100, 100, 1150, 20, NEGRO, CERÚLEO_O_AZUR, 'ProjectXY')
    texto_destruccion = TextoDestruccion(100, 50, 100, 50, BLANCO, CERÚLEO_O_AZUR)
    jugador = Jugador(WIDTH // 2, HEIGHT // 2, 25, 40, CERÚLEO_O_AZUR, texto_destruccion)

    plataformas = [plataforma, tierra1, tierra2, tierra3, tierra4, tierra5, tierra6, tierra7, piedra1, piedra2, madera1]
    all_sprites.add(*plataformas, jugador, cuadro_texto, texto_destruccion)
    platforms.add(*plataformas)

    cuadricula = Cuadricula(GRID_SIZE, GRANATE, VINO, WIDTH, HEIGHT)
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        handle_input(jugador, platforms)

        if jugador.vel_x != 0:
            if jugador.vel_x > 0:
                jugador.auto_jump(platforms, 'right')
            else:
                jugador.auto_jump(platforms, 'left')

        jugador.apply_gravity()

        jugador.move(jugador.vel_x, 0, platforms)
        CollisionChecker.check_horizontal_collision(jugador, platforms)

        jugador.move(0, jugador.vel_y, platforms)
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
