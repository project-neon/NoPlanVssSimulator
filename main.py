import json
import socket
import threading

import pygame

import ball
import constants
import field
import robot

pygame.init()
screen = pygame.display.set_mode((1200, 600))

# Title and Icon🤖
pygame.display.set_caption('🤖Neon VSS Simulation🤖')
icon = pygame.image.load('resources/icon.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

NOPLAN_LISTENER = ('localhost', 5778)
listener_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

NOPLAN_SENDER = ('localhost', 5777)
sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class Game:

    def no_plan_listener(self):
        listener_sock.bind(NOPLAN_LISTENER)
        while True:
            data, address = listener_sock.recvfrom(4096)
            if data:
                self.message = data.decode('utf-8')
                print(self.message)

    def sent_to_no_plan(self, data):
        sender_sock.sendto(bytes(json.dumps(data), 'utf-8'), NOPLAN_SENDER)

    def __init__(self, blue_robots=None, yellow_robots=None, ball_pos=(0, 0)):
        if yellow_robots is None:
            yellow_robots = []

        if blue_robots is None:
            blue_robots = []

        self.message = []

        self.field = field.Field()
        self.ball = ball.Ball(pos=ball_pos)

        self.robots = []

        self.running = False

        for robot_ in blue_robots:
            self.robots.append(
                robot.Robot('blue', self.field, robot_['start_position'], robot_['orientation'],
                            radio_id=robot_['radio_id'], vision_id=robot_['vision_id'])
            )

        for robot_ in yellow_robots:
            self.robots.append(
                robot.Robot('yellow', self.field, robot_['start_position'], robot_['orientation'],
                            radio_id=robot_['radio_id'], vision_id=robot_['vision_id'])
            )

    def build_for_noplan(self):
        self.timestamp += 1
        entities_data = {
            't_capture': self.timestamp,
            'robots_blue': [
                {
                    'x': r.position[0],
                    'y': r.position[1],
                    'orientation': r.orientation,
                    'robot_id': r.vision_id
                } for r in self.robots if r.team_color == 'blue'
            ],
            'robots_yellow': [
                {
                    'x': r.position[0],
                    'y': r.position[1],
                    'orientation': r.orientation,
                    'robot_id': r.vision_id
                } for r in self.robots if r.team_color == 'yellow'
            ],
            'balls': [{'x': self.ball.position[0], 'y': self.ball.position[1], 'speed': {'x': 0, 'y': 0}}]}

        data = {
            'detection': entities_data,
            'geometry': {}
        }

        return data

    def start(self):
        self.timestamp = 0
        self.running = True

        listener_thread = threading.Thread(target=self.no_plan_listener, args=())

        listener_thread.start()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    w, h = pygame.display.get_surface().get_size()
                    self.ball.position = (pos[0] - w/2)*2, (pos[1] - h/2)*2
            screen.fill(constants.COLORS.NEON_BLACK)

            self.field.update(screen)
            self.ball.update(screen)

            for rb in self.robots:
                try:
                    rb_message = list(filter(lambda x: x[0] == rb.vision_id, json.loads(self.message)))
                    if rb_message:
                        rb.update(screen, rb_message[0])
                    else:
                        rb.update(screen, [0, 1, 0, 0])
                except:
                    pass

            pygame.display.update()
            self.sent_to_no_plan(self.build_for_noplan())


config = json.loads(open('match_config.json', 'r').read())

match = Game(**config)

match.start()
