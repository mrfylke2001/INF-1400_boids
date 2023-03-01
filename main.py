import numpy as np
import pygame
from pygame.locals import *

class Game:
    def __init__(self, size: tuple[int, int]):
        pygame.init()
        self.game_display = pygame.display.set_mode(size)
        pygame.display.set_caption("Boids")

        self.BKG_COLOR = (255, 255, 255) # white

    def _event_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

    def _get_game_objects(self):
        pass

    def play(self):
        while True:
            self._event_handler()

            self.game_display.fill(self.BKG_COLOR)

            pygame.display.update()

class GameObject:
    def __init__(self, pos: pygame.math.Vector2):
        self.pos = pos

    def animate(self):
        pass

class Obstacle(GameObject):
    def animate(self):
        pass

class Character(GameObject):
    def animate(self, speed):
        dir = self._get_dir()
        vel = dir.scale_to_length(speed)
        pos_new = (self.pos.x + vel.x, self.pos.y + vel.y)

        self.orient(dir)
        self.move(pos_new)

    def _get_dir(self):
        pass

    def orient(self):
        pass

    def move(self):
        pass

class Boid(Character):
    def _get_flock(self, r):
        # Returns `Flock` object with other boids within radius r
        pass

    def _get_dir(self) -> pygame.math.Vector2:
        pass

class Hoik(Character):
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