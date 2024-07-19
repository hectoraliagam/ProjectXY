import pygame as pg

# Resolución y proporciones adaptativas
SCREEN_RATIO = 16 / 9

# Inicializa Pygame para obtener las dimensiones de la pantalla
pg.init()
info = pg.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Configura las dimensiones basadas en la relación de aspecto
WIDTH = SCREEN_WIDTH
HEIGHT = int(SCREEN_WIDTH / SCREEN_RATIO)

# Configuraciones del juego
SPEED = 10
GRAVITY = 1
JUMP_STRENGTH = 20
GRID_SIZE = 50
FONT_SIZE = 20
