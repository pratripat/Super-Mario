from .entities.lift import Lift
import pygame

class Lift_Spawner:
    def __init__(self, game, position):
        self.game = game
        self.position = position
        self.spawn_timer = 0
        self.max_spawn_timer = 3

    def spawn_lift(self):
        if int(self.spawn_timer) > 0:
            self.spawn_timer -= self.game.dt

        if int(self.spawn_timer) == 0:
            lift = Lift(self.game, pygame.Rect(*self.position, 10, 10), self.velocity, top_position=[0,-float('inf')], bottom_position=[0,float('inf')])
            self.game.entities.lifts.append(lift)
            self.spawn_timer = self.max_spawn_timer

    @property
    def velocity(self):
        if self.position[1] <= self.game.tilemap.top:
            print(self.position, self.game.tilemap.top)
            return [0, 2]
        else:
            return [0,-2]

class Lift_Spawner_Manager:
    def __init__(self, game):
        self.game = game
        self.lift_spawners = [Lift_Spawner(game, list(rect.topleft)) for rect in self.game.tilemap.get_rects_with_id('lift_spawner')]
        print(self.lift_spawners)

    def update(self):
        for lift_spawner in self.lift_spawners:
            lift_spawner.spawn_lift()
