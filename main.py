import numpy as np
import pygame
from pygame.locals import *

class Game:
    BKG_COLOR = (255, 255, 255) # white

    def __init__(self, size: tuple[int, int]):
        pygame.init()
        self.surface = pygame.display.set_mode(size)
        pygame.display.set_caption("Boids")

        self.objects = [Boid(self.surface, pygame.Vector2(400, 300))]

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
    def __init__(self, surface: pygame.Surface, pos: pygame.Vector2):
        self.surface = surface
        self.pos = pos

    def move(self):
        pass

    def draw(self):
        pass

class Obstacle(GameObject):
    pass

class Boid(GameObject):
    scale = 6
    vel = pygame.Vector2(3, 4)

    def _get_flock(self, r):
        # Returns `Flock` object with other boids within radius r
        pass

    def _stay_within_bounds(self):
        buffer = 30
        x_min, y_min = buffer, buffer
        x_max = self.surface.get_width() - buffer
        y_max = self.surface.get_height() - buffer

        vel = pygame.Vector2(0, 0)

        rebound_speed = 5

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
        vertices = [
            pygame.Vector2(self.pos + self.scale*self.dir.rotate(120*i))
            for i in range(3)
        ] # for an equilateral triangle centered at `pos`

        pygame.draw.polygon(self.surface, "black", vertices)

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