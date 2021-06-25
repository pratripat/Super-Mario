import random

class Camera:
    def __init__(self):
        self.target = None
        self.scroll = [0,0]
        self.movement = 1
        self.screen_shake = 0
        self.time = 0
        self.stuck_bottom = True

    def update(self, surface, tilemap=None):
        axe = tilemap.get_tiles_with_id('axe')

        if self.time == 0:
            self.screen_shake = 0

        if self.target and len(axe):
            self.scroll[0] += int((self.target.center[0]-self.scroll[0]-surface.get_width()/2) * self.movement + random.uniform(-self.screen_shake, self.screen_shake+1))
        else:
            self.scroll[0] += self.target.speed

        if self.time > 0:
            self.time -= 1

        if tilemap:
            right = tilemap.right

            if len(axe):
                right = axe[0]['position'][0]+axe[0]['dimensions'][0]+tilemap.RES//2

            if self.scroll[0] > right-surface.get_width():
                self.scroll[0] = right-surface.get_width()
            if self.scroll[0] < tilemap.left:
                self.scroll[0] = tilemap.left
            if self.scroll[1] < tilemap.top:
                self.scroll[1] = tilemap.top
            if self.scroll[1] > tilemap.bottom-surface.get_height():
                self.scroll[1] = tilemap.bottom-surface.get_height()

            self.scroll[1] = tilemap.bottom-surface.get_height()

        tilemap.left = self.scroll[0]

    def set_target(self, target):
        self.target = target

    def set_movement(self, movement):
        self.movement = movement

    def set_screen_shake(self, screen_shake, time):
        self.screen_shake = screen_shake
        self.time = time
