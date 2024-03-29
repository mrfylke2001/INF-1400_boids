import numpy as np
import pygame
from pygame.locals import *

# Returns sum of 2D vectors
def v2_sum(vectors: tuple[pygame.Vector2]) -> pygame.Vector2:
    vector_sum = pygame.Vector2(0, 0)
    for vec in vectors:
        vector_sum += vec
    return vector_sum

# Returns a 2D unit vector in a random direction
def rand_unit_v2(theta_min=0, theta_max=360) -> pygame.Vector2:
    theta = np.random.randint(theta_min, theta_max)
    vec = pygame.Vector2(1, 0).rotate(theta)
    return vec

class Game:
    BKG_COLOR = (61, 61, 61)
    BOID_COLOR = (109, 157, 201)
    HOIK_COLOR = (227, 177, 52)
    OBST_COLOR = (0, 0, 0)

    BOID_SIZE = 6
    HOIK_SIZE = 24
    OBST_SIZE_MIN, OBST_SIZE_MAX = 32, 64

    def __init__(self,
                 size: tuple[int, int],
                 n_boids: int,
                 n_hoiks: int,
                 n_obstacles: int):
        pygame.init()
        self.surface = pygame.display.set_mode(size)
        pygame.display.set_caption("Boids")

        self._set_up_objects(n_boids, n_hoiks, n_obstacles)

    def _set_up_objects(self, n_boids, n_hoiks, n_obstacles):
        self.boids = np.array([
            self._generate_boid()
            for _ in range(n_boids)
        ])

        self.obstacles = np.array([
            self._generate_obst()
            for _ in range(n_obstacles)
        ])

        self.hoiks = np.array([
            self._generate_hoik()
            for _ in range(n_hoiks)
        ])

        self.objects = np.concatenate((self.boids, self.obstacles, self.hoiks))

    # Returns a random position within the game window
    def _random_pos(self, buffer=0) -> pygame.Vector2:
        x = np.random.randint(buffer, self.surface.get_width() - buffer)
        y = np.random.randint(buffer, self.surface.get_height() - buffer)
        pos = pygame.Vector2(x, y)
        return pos

    def _generate_boid(self):
        pos = self._random_pos(buffer=self.BOID_SIZE)
        vel = 3*rand_unit_v2() # starting speed is 3

        boid = Boid(self, pos, vel, self.BOID_COLOR, self.BOID_SIZE)
        return boid
    
    def _generate_hoik(self):
        pos = self._random_pos(buffer=self.HOIK_SIZE)
        vel = 2*rand_unit_v2() # starting speed is 2

        hoik = Hoik(self, pos, vel, self.HOIK_COLOR, self.HOIK_SIZE)
        return hoik

    def _generate_obst(self):
        size = np.random.randint(self.OBST_SIZE_MIN, self.OBST_SIZE_MAX)

        # Edge of obstacle should have some distance from window edge
        pos = self._random_pos(buffer=1.5*size)
        vel = pygame.Vector2(0, 0)

        obst = Obstacle(self, pos, vel, self.OBST_COLOR, size)
        return obst

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
                 color: tuple[int, int, int],
                 size: int):
        self.game = game
        self.pos = p0 # initial position
        self.vel = v0 # initial velocity
        self.color = color
        self.size = size # radius

    def move(self):
        pass

    def draw(self):
        pass

class Obstacle(GameObject): # static objects
    def draw(self):
        pygame.draw.circle(self.game.surface, self.color, self.pos, self.size)

class Character(GameObject): # moving objects
    MAX_SPEED = 0
    dir = pygame.Vector2(0, 1) # direction character points

    # Prevents characters from leaving the window
    def _stay_within_bounds(self) -> pygame.Vector2:
        buffer = 30
        x_min, y_min = buffer, buffer
        x_max = self.game.surface.get_width() - buffer
        y_max = self.game.surface.get_height() - buffer

        rebound_speed = 10
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
        dv = self._stay_within_bounds()
        return dv

    def _update_vel(self):
        self.vel += self._accl()

        # Character speed will not exceed `MAX_SPEED`
        if self.vel.magnitude() > self.MAX_SPEED:
            self.vel.scale_to_length(self.MAX_SPEED)

        # Character will stay pointing in same direction if velocity is 0
        if self.vel != pygame.Vector2(0, 0):
            self.dir = self.vel.normalize()

    def move(self):
        self._update_vel()

        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

    def draw(self):
        vertices = [
            pygame.Vector2(self.pos + self.size*self.dir.rotate(120*i))
            for i in range(3)
        ] # for an equilateral triangle centered at `pos`

        pygame.draw.polygon(self.game.surface, self.color, vertices)

class Boid(Character):
    MAX_SPEED = 4

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
    def _avoid_flockmates(self, flock) -> pygame.Vector2:
        r_min = 16 # min comfortable distance between boids
        dv = v2_sum([
            self.pos - boid.pos # vector pointing away from flockmate
            for boid in flock.boids
            if self.pos.distance_to(boid.pos) < r_min
        ])
        return dv
    
    def _avoid_hoiks(self) -> pygame.Vector2:
        r_min = 64 # min comfortable distance to hoik
        dv = v2_sum([
            self.pos - hoik.pos # vector pointing away from hoik
            for hoik in self.game.hoiks
            if self.pos.distance_to(hoik.pos) < r_min
        ])
        return dv
    
    def _avoid_obstacles(self) -> pygame.Vector2:
        r_min = 16 # min comfortable distance to edge of obstacle
        dv = v2_sum([
            self.pos - obst.pos # vector pointing away from obstacle
            for obst in self.game.obstacles
            if self.pos.distance_to(obst.pos) < r_min + obst.size
        ])
        return dv

    def _accl(self) -> pygame.Vector2:
        local_flock = self._get_local_flock(r=64)
        accl_components = np.array([
            0.01*self._toward_local_flock_center(local_flock),
            0.08*self._toward_local_flock_vel(local_flock),
            0.4*self._avoid_flockmates(local_flock),
            0.2*self._avoid_hoiks(),
            0.2*self._avoid_obstacles(),
            self._stay_within_bounds()
        ]) # components are weighted for desired behavior
        dv = v2_sum(accl_components)
        return dv

class Hoik(Character):
    MAX_SPEED = 2

    def _get_new_target(self) -> Boid:
        # Sort boids by distance
        dist_key = lambda boid : self.pos.distance_squared_to(boid.pos)
        boids_by_dist = sorted(self.game.boids, key=dist_key)

        # Return the closest boid not already targeted by another hoik
        for boid in boids_by_dist:
            if not any([
                hoik.target is boid
                for hoik in self.game.hoiks
                if hasattr(hoik, "target") and hoik is not self
            ]):
                return boid
    
    def _chase_target(self) -> pygame.Vector2:
        r_max = 200

        # Choose initial target if one does not exist
        if not hasattr(self, "target"):
            self.target = self._get_new_target()

        # Choose new target if current target is too far
        elif self.pos.distance_to(self.target.pos) > r_max:
            self.target = self._get_new_target()
        
        dv = self.target.pos - self.pos
        dv.scale_to_length(self.MAX_SPEED)
        return dv
    
    def _accl(self) -> pygame.Vector2:
        dv1 = self._chase_target()
        dv2 = self._stay_within_bounds()
        return dv1 + dv2

class Flock:
    def __init__(self, boids: list[Boid]):
        self.boids = np.array(boids)
        self.n_boids = len(boids)

    def avg_pos(self) -> pygame.Vector2:
        p_avg = v2_sum([boid.pos for boid in self.boids]) / self.n_boids
        return p_avg

    def avg_vel(self) -> pygame.Vector2:
        v_avg = v2_sum([boid.vel for boid in self.boids]) / self.n_boids
        return v_avg

if __name__ == "__main__":
    boids_game = Game((800, 600), 64, 2, 3)
    boids_game.play()