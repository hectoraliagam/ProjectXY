import config  # Importa el módulo config
from platforms import Tierra, Platform

class CollisionChecker:
    @staticmethod
    def check_collision(rect, objects):
        rect.on_platform = False
        for obj in objects:
            if isinstance(obj, Tierra):
                # Colisiones con Tierra
                if rect.rect.colliderect(obj.rect):
                    if rect.vel_y > 0 and rect.rect.bottom > obj.rect.top:
                        rect.rect.bottom = obj.rect.top
                        rect.vel_y = 0
                        rect.on_platform = True
                        rect.jumps_left = 2
            elif isinstance(obj, Platform):
                # Colisiones con Platform
                if rect.vel_y > 0 and rect.rect.colliderect(obj.rect):
                    if rect.rect.bottom <= obj.rect.top + rect.vel_y:
                        rect.rect.bottom = obj.rect.top
                        rect.vel_y = 0
                        rect.on_platform = True
                        rect.jumps_left = 2
        if rect.rect.top > config.HEIGHT:
            rect.reset_position()
