import pygame, json

class UI:
    def __init__(self, game):
        self.game = game
        self.score = 0
        self.coins = 0
        self.time = 40
        self.animation = self.game.animations.get_animation('coin_ui')

    def render(self):
        #FIRST ROW
        position1 = self.game.font.render(self.game.screen, 'mario', [self.game.screen.get_width()/5,20], scale=3, center=[True, False])
        position2 = self.game.font.render(self.game.screen, 'world', [self.game.screen.get_width()/5*3,20], scale=3, center=[True, False])
        position3 = self.game.font.render(self.game.screen, 'time', [self.game.screen.get_width()/5*4,20], scale=3, center=[True, False])

        #SECOND ROW
        self.game.font.render(self.game.screen, f'{self.score:06d}', [position1[0], 50], scale=3)

        position = self.game.font.render(self.game.screen, f'*{self.coins:02d}', [self.game.screen.get_width()/5*2, 50], scale=3)
        self.animation.render(self.game.screen, [position[0]-self.animation.image.get_width(), position[1]])

        world_surface = self.game.font.get_surface('WORLD')
        world_surface = pygame.transform.scale(world_surface, (world_surface.get_width()*3, world_surface.get_height()*3))
        level, world_type, cutscene_path = json.load(open('data/levels/level_order.json', 'r'))[self.game.level]
        world = level.split('.')[0].split('/')
        self.game.font.render(self.game.screen, f'{world[-2][-1]}-{world[-1]}', [position2[0]+world_surface.get_width()/2, 50], scale=3, center=[True, False])

        time_surface = self.game.font.get_surface('TIME')
        time_surface = pygame.transform.scale(time_surface, (time_surface.get_width()*3, time_surface.get_height()*3))
        time_counter_surface = self.game.font.get_surface(f'{int(self.time):03d}')
        time_counter_surface = pygame.transform.scale(time_counter_surface, (time_counter_surface.get_width()*3, time_counter_surface.get_height()*3))
        self.game.font.render(self.game.screen, f'{int(self.time):03d}', [position3[0]+time_surface.get_width()-time_counter_surface.get_width(), 50], scale=3)

    def update(self):
        self.animation.run(self.game.dt)

        if self.coins >= 100:
            self.coins = 0

        if not self.game.entities.mario.dead:
            self.time -= self.game.dt

            if self.time <= 0:
                self.game.entities.mario.die()

    def refresh(self, level):
        level = int(level.split('/')[-1])
        self.time = 400
        if level == 3 or level == 4:
            self.time = 300
