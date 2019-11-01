import math
import pygame

import field


class CONTROLTYPE:
    NOPLAN = 1
    JOYSTICK = 2


class Robot:
    def __init__(self, team_color, field_, init_pos=(0, 0), init_ori=0,
                 control_type=CONTROLTYPE.NOPLAN, radio_id=0, vision_id=0):
        """
        :param team_color:
        :param init_pos:
        :param init_ori:
        :param control_type:
        """
        self.team_color = team_color
        self.orientation = init_ori
        self.position = init_pos
        self.control_type = control_type

        self.radio_id = radio_id
        self.vision_id = vision_id

        self.field = field_

        self.player_image = pygame.image.load(
            'resources/{}_robot.png'.format(self.team_color)
        )
        self.size = (int(75 / 2), int(75 / 2))
        self.player_image = pygame.transform.scale(self.player_image, self.size)

    def update(self, screen, command_message):
        dt = 0.1
        linear = command_message[2]
        angular = command_message[3]
        delta_pos = (
            math.cos(self.orientation) * -linear * dt,
            math.sin(self.orientation) * -linear * dt
        )
        delta_theta = angular * dt/2 # numero magico pra angular parecer com vida real

        if delta_theta:
            self.orientation = self.orientation - delta_theta * math.pi/180

        if delta_pos:
            self.position = self.position[0] + delta_pos[0], self.position[1] + delta_pos[1]

        image = pygame.transform.rotate(self.player_image, math.degrees(-self.orientation))

        w, h = image.convert().get_width(), image.convert().get_height()
        w = self.position[0]/2 - w/2
        h = self.position[1]/2 - h/2

        screen.blit(image, field.field_to_game(w, h))
