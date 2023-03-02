import numpy as np
import pygame
from pygame.locals import *
import random

class Game:
    BKG_COLOR = (61, 61, 61)
    BOID_COLOR = (109, 157, 201)

    def __init__(self, size: tuple[int, int]):
        pygame.init()
        self.surface = pygame.display.set_mode(size)
        pygame.display.set_caption("Boids")

        self._set_up_objects(16)

    def _set_up_objects(self, num_boids):
        self.boids = [
            self._generate_boid()
            for _ in range(num_boids)
        ]

        self.objects = self.boids

    def _generate_boid(self):
        # Initial position is randomized within the game window
        x = random.randint(0, self.surface.get_width())
        y = random.randint(0, self.surface.get_height())
        pos = pygame.Vector2(x, y)

        # Initial velocity has given speed in a random direction
        speed = 3
        vel = pygame.Vector2(speed, 0).rotate(random.randint(0, 359))

        boid = Boid(self, pos, vel, self.BOID_COLOR)
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
    def __init__(self, game, p_init, v_init, color):
        self.game = game
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
    def _get_local_flock(self, r: int):
        # Returns `Flock` object with other boids within radius r
        local_flock = Flock([
            boid
            for boid in self.game.boids
            if (boid.pos - self.pos).magnitude() <= r
        ])
        return local_flock
    
    def _toward_local_flock_center(self) -> pygame.Vector2:
        weight = 0.01 # scale factor for resulting change in velocity

        local_flock = self._get_local_flock(r=60)
        dv = weight*(local_flock.avg_pos() - self.pos)

        return dv

    def _stay_within_bounds(self) -> pygame.Vector2:
        buffer = 30
        x_min, y_min = buffer, buffer
        x_max = self.game.surface.get_width() - buffer
        y_max = self.game.surface.get_height() - buffer

        rebound_speed = 2
        dv = pygame.Vector2(0, 0)

        if self.pos.x < x_min:
            dv.x = rebound_speed
        elif self.pos.x > x_max:
            dv.x = -rebound_speed

        if self.pos.y < y_min:
            dv.y = rebound_speed
        elif self.pos.y > y_max:
            dv.y = -rebound_speed

        return dv

    def _accl(self) -> pygame.Vector2:
        # Calculate 'acceleration' i.e. change in velocity
        dv1 = self._toward_local_flock_center()
        dv2 = self._stay_within_bounds()

        dv = dv1 + dv2
        return dv

    def move(self):
        self.vel += self._accl()
        self.dir = self.vel.normalize()

        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

    def draw(self):
        scale = 6
        vertices = [
            pygame.Vector2(self.pos + scale*self.dir.rotate(120*i))
            for i in range(3)
        ] # for an equilateral triangle centered at `pos`

        pygame.draw.polygon(self.game.surface, self.color, vertices)

class Hoik(GameObject):
    def _get_dir(self):
        pass

    def _get_target(self):
        # Returns `Boid` object to chase
        pass

class Flock:
    def __init__(self, boids: list[Boid]):
        self.boids = np.array(boids)
        self.num_boids = len(boids)

    def avg_pos(self):
        p_sum = pygame.Vector2(0, 0)
        for boid in self.boids:
            p_sum += boid.pos
        p_avg = p_sum / self.num_boids
        return p_avg

    def avg_dir(self):
        # Returns average heading of boids in flock as a unit vector
        pass

if __name__ == "__main__":
    boids_game = Game((800, 600))
    boids_game.play()