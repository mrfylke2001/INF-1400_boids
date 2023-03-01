import numpy as np
# import pygame

def normalize(vec: tuple[float, float]):
    mag = np.sqrt(vec[0]**2 + vec[1]**2)
    unit_vec = (vec[0]/mag, vec[1]/mag)

    return unit_vec

class Game:
    pass

class GameSpace:
    pass

class GameObject:
    def __init__(self, space: GameSpace, pos: tuple[float, float]):
        self.animate()

    def animate(self):
        pass

class Obstacle(GameObject):
    def animate(self):
        pass

class Character(GameObject):
    def animate(self):
        vel = self._get_vel()
        dir = normalize(vel)
        pos_new = (self.pos[0] + vel[0], self.pos[1] + vel[1])

        self.orient(dir)
        self.move(pos_new)

    def _get_vel(self):
        pass

    def orient(self):
        pass

    def move(self):
        pass

class Boid(Character):
    def _get_flock(self, r):
        # Returns `Flock` object with other boids within radius r
        pass

    def _get_vel(self):
        pass

class Hoik(Character):
    def _get_vel(self):
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