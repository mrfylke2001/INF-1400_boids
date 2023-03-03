import numpy as np
import pygame
from pygame.locals import *

class Game:
    BKG_COLOR = (61, 61, 61)
    BOID_COLOR = (109, 157, 201)

    def __init__(self, size: tuple[int, int]):
        pygame.init()
        self.surface = pygame.display.set_mode(size)
        pygame.display.set_caption("Boids")

        self._set_up_objects(64)

    def _set_up_objects(self, num_boids):
        self.boids = np.array([
            self._generate_boid()
            for _ in range(num_boids)
        ])

        self.objects = self.boids

    def _generate_boid(self):
        # Initial position is randomized within the game window
        x = np.random.randint(0, self.surface.get_width())
        y = np.random.randint(0, self.surface.get_height())
        pos = pygame.Vector2(x, y)

        # Initial velocity has given speed in a random direction
        speed = 2
        vel = pygame.Vector2(speed, 0).rotate(np.random.randint(0, 360))

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

    # Starts game loop
    def play(self):
        while True:
            self._event_handler()

            self.surface.fill(self.BKG_COLOR)
            self._move_objects()
            self._draw_objects()

            pygame.display.update()

class GameObject:
    def __init__(self,
                 game: Game,
                 p0: pygame.Vector2,
                 v0: pygame.Vector2,
                 color: tuple[int, int, int]):
        self.game = game
        self.pos = p0 # initial position
        self.vel = v0 # initial velocity
        self.color = color

    def _update_vel(self):
        pass

    def move(self):
        self._update_vel()

        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

    def draw(self):
        pass

class Obstacle(GameObject): # static objects
    pass

class Character(GameObject): # moving objects
    max_speed = 0

    def _accl(self):
        pass

    def _update_vel(self):
        self.vel += self._accl()

        # Character speed will not exceed `max_speed`
        if self.vel.magnitude() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)

        # Character will stay pointing in same direction if velocity is 0
        if self.vel != pygame.Vector2(0, 0):
            self.dir = self.vel.normalize()

class Boid(Character):
    max_speed = 4

    # Returns `Flock` object with other boids within radius r
    def _get_local_flock(self, r: int):
        local_flock = Flock([
            boid
            for boid in self.game.boids
            if self.pos.distance_to(boid.pos) <= r
        ])
        return local_flock
    
    # Steers boids toward avg position of flockmates
    def _toward_local_flock_center(self, flock) -> pygame.Vector2:
        dv = flock.avg_pos() - self.pos
        return dv
    
    # Points boids in line with flockmates
    def _toward_local_flock_vel(self, flock) -> pygame.Vector2:
        dv = flock.avg_vel() - self.vel
        return dv
    
    # Prevents boids from colliding
    def _keep_buffer(self, flock) -> pygame.Vector2:
        r_min = 16 # min comfortable distance between boids

        dv = pygame.Vector2(0, 0)
        for boid in flock.boids:
            if self.pos.distance_to(boid.pos) < r_min:
                dv -= (boid.pos - self.pos)

        return dv

    # Prevents boids from leaving the window
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

    # Calculates 'acceleration' i.e. change in velocity
    def _accl(self) -> pygame.Vector2:
        local_flock = self._get_local_flock(r=50)
        dv1 = self._toward_local_flock_center(local_flock)
        dv2 = self._toward_local_flock_vel(local_flock)
        dv3 = self._keep_buffer(local_flock)

        dv4 = self._stay_within_bounds()

        # Change in velocity is weighted sum of components from each rule
        dv = 0.02*dv1 + 0.03*dv2 + 0.4*dv3 + dv4
        return dv

    def draw(self):
        scale = 6
        vertices = [
            pygame.Vector2(self.pos + scale*self.dir.rotate(120*i))
            for i in range(3)
        ] # for an equilateral triangle centered at `pos`

        pygame.draw.polygon(self.game.surface, self.color, vertices)

class Hoik(Character):
    max_speed = 3

    # Returns `Boid` object to chase
    def _get_target(self):
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

    def avg_vel(self):
        v_sum = pygame.Vector2(0, 0)
        for boid in self.boids:
            v_sum += boid.vel
        v_avg = v_sum / self.num_boids

        return v_avg

if __name__ == "__main__":
    boids_game = Game((800, 600))
    boids_game.play()