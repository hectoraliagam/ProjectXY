# interfaces.py
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
