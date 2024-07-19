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
                    rect.jumps_left = 2
                    return platform
        return None