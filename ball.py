import pygame

import field


class Ball:
    def __init__(self, pos=(0, 0)):
        self.position = pos

        self.ball_image = pygame.image.load(
            'resources/ball.png'
        )
        self.size = (int(40 / 2), int(40 / 2))
        self.ball_image = pygame.transform.scale(self.ball_image, self.size)

    def update(self, screen):
        image = self.ball_image
        w, h = image.convert().get_width(), image.convert().get_height()
        w = self.position[0]/2 - w/2
        h = self.position[1]/2 - h/2

        screen.blit(image, field.field_to_game(w, h))
