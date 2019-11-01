import pygame


def field_to_game(x, y):
    w, h = pygame.display.get_surface().get_size()
    return x + w/2, y + h/2


class Field:
    def __init__(self):
        self.image = pygame.image.load(
            'resources/field.png'
        )
        self.size = (int(1500/2), int(1300/2))
        self.image = pygame.transform.scale(self.image, self.size)

    def update(self, screen):
        w, h = pygame.display.get_surface().get_size()

        w = w/2 - self.size[0]/2
        h = h/2 - self.size[1]/2

        screen.blit(self.image, (w, h))
