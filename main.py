import numpy as np
import pygame
from pygame.locals import *
import random

class Game:
    BKG_COLOR = (61, 61, 61)
    BOID_COLOR = (90, 142, 191)

    def __init__(self, size: tuple[int, int]):
        pygame.init()
        self.surface = pygame.display.set_mode(size)
        pygame.display.set_caption("Boids")

        self._set_up_objects(5)

    def _set_up_objects(self, num_boids):
        self.objects = [
            self._generate_boid()
            for _ in range(num_boids)
        ]

    def _generate_boid(self):
        # Initial position is randomized within the game window
        x = random.randint(0, self.surface.get_width())
        y = random.randint(0, self.surface.get_height())
        pos = pygame.Vector2(x, y)

        # Initial velocity has given speed in a random direction
        speed = 5
        vel = pygame.Vector2(speed, 0).rotate(random.randint(0, 359))

        boid = Boid(self.surface, pos, vel, self.BOID_COLOR)
        return boid

    def _event_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

    def _move_objects(self):
        for object in self.objects:
            object.move()

    def _draw_objects(self):
        for object in self.objects:
            object.draw()

    def play(self):
        while True:
            self._event_handler()

            self.surface.fill(self.BKG_COLOR)
            self._move_objects()
            self._draw_objects()

            pygame.display.update()

class GameObject:
    def __init__(self, surface: pygame.Surface, p_init, v_init, color):
        self.surface = surface
        self.pos = p_init # initial position
        self.vel = v_init # initial velocity
        self.color = color

    def move(self):
        pass

    def draw(self):
        pass

class Obstacle(GameObject):
    pass

class Boid(GameObject):
    def _get_flock(self, r):
        # Returns `Flock` object with other boids within radius r
        pass

    def _stay_within_bounds(self):
        buffer = 30
        x_min, y_min = buffer, buffer
        x_max = self.surface.get_width() - buffer
        y_max = self.surface.get_height() - buffer

        vel = pygame.Vector2(0, 0)

        rebound_speed = 3

        if self.pos.x < x_min:
            vel.x = rebound_speed
        elif self.pos.x > x_max:
            vel.x = -rebound_speed

        if self.pos.y < y_min:
            vel.y = rebound_speed
        elif self.pos.y > y_max:
            vel.y = -rebound_speed

        return vel

    def _addtl_vel(self) -> pygame.Vector2:
        v2 = self._stay_within_bounds()

        return v2

    def move(self):
        self.vel += self._addtl_vel()
        self.dir = self.vel.normalize()

        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

    def draw(self):
        scale = 6
        vertices = [
            pygame.Vector2(self.pos + scale*self.dir.rotate(120*i))
            for i in range(3)
        ] # for an equilateral triangle centered at `pos`

        pygame.draw.polygon(self.surface, self.color, vertices)

class Hoik(GameObject):
    def _get_dir(self):
        pass

    def _get_target(self):
        # Returns `Boid` object to chase
        pass

class Flock:
    def __init__(self, boids: list[Boid]):
        self.boids = np.array(boids)

    def avg_pos(self):
        pass

    def avg_dir(self):
        # Returns average heading of boids in flock as a unit vector
        pass

if __name__ == "__main__":
    boids_game = Game((800, 600))
    boids_game.play()