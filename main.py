import numpy as np
import pygame
from pygame.locals import *

class Game:
    def __init__(self, size: tuple[int, int]):
        pygame.init()
        self.surface = pygame.display.set_mode(size)
        pygame.display.set_caption("Boids")

        self.BKG_COLOR = (255, 255, 255) # white

    def _event_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

    def _get_game_objects(self):
        objects = [Boid(self.surface, pygame.Vector2(400, 300))]
        return objects

    def play(self):
        while True:
            self._event_handler()

            self.surface.fill(self.BKG_COLOR)
            for object in self._get_game_objects():
                object.animate(0)

            pygame.display.update()

class GameObject:
    def __init__(self, surface, pos: pygame.Vector2):
        self.surface = surface
        self.pos = pos

    def animate(self):
        pass

class Obstacle(GameObject):
    def animate(self):
        pass

class Character(GameObject):
    def animate(self, speed):
        dir = self._get_dir()
        #vel = dir.scale_to_length(speed)
        #pos_new = (self.pos.x + vel.x, self.pos.y + vel.y)

        #self.move(pos_new)
        self.draw(dir)

    def _get_dir(self):
        pass

    def move(self):
        pass

    def draw(self, dir: pygame.Vector2):
        vertices = [
            pygame.Vector2(self.pos + self.scale*dir.rotate(120*i))
            for i in range(3)
        ] # for an equilateral triangle centered at `pos`

        pygame.draw.polygon(self.surface, "black", vertices)

class Boid(Character):
    scale = 10

    def _get_flock(self, r):
        # Returns `Flock` object with other boids within radius r
        pass

    def _get_dir(self) -> pygame.Vector2:
        return pygame.Vector2(1, 0)

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