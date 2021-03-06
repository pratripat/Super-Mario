from ..funcs import *
from .coin_vfx import Coin
import math

class Block:
    def __init__(self, rect, type):
        self.initial_rect = rect
        self.type = type
        self.remove = False
        self.updating_offset = False
        self.offset = 0
        self.offset_counter = 0
        self.hits = 1

    def update_offset(self, function=None):
        if not self.updating_offset:
            return

        self.offset_counter += 0.2
        self.offset = math.sin(self.offset_counter)*10

        enemies = {
            f'{self.game.world_type}_koopa': 'koopa',
            f'{self.game.world_type}_goomba': 'goomba',
            f'{self.game.world_type}_piranha_plant': 'piranha_plant',
            f'red_cheep_cheep': 'red_cheep_cheep',
            f'grey_cheep_cheep': 'grey_cheep_cheep',
            'red_koopa': 'koopa',
            'blooper': 'blooper',
            'bowser': 'bowser'
        }

        for enemy in self.game.entities.get_enemies():
            if rect_rect_collision(enemy.rect, self.rect):
                if not enemy.id == 'podoboo':
                    enemy.falling = True
                    enemy.velocity[1] = -5
                    enemy.stomp_sfx.play()
                    self.game.score_system.add_score('enemy', enemies[enemy.id], enemy)

        for coin in self.game.entities.coins[:]:
            if rect_rect_collision(coin.rect, self.rect):
                coin.coin_sfx.play()
                self.game.entities.coins.remove(coin)
                self.game.entities.coin_animations.append(Coin(self.game, list(coin.rect.center)))
                self.game.ui.coins += 1

        for item in self.game.entities.items:
            if rect_rect_collision(item.rect, self.rect):
                if item.center[0] > self.rect.center[0]:
                    item.velocity[0] = abs(item.velocity[0])
                else:
                    item.velocity[0] = -abs(item.velocity[0])
                item.velocity[1] = -8
                item.rect[1] -= self.offset

        if self.offset <= 0:
            self.updating_offset = False
            self.offset = 0
            self.offset_counter = 0

            if function:
                function()

    def up_collision(self, player, function):
        if player.velocity[1] < 0:
            rect = player.rect.copy()
            rect[1] += player.velocity[1]
            if rect_rect_collision(rect, self.rect):
                function()
                player.velocity[1] = 0
                player.airtimer = player.max_airtimer

                if self.hits > 0:
                    self.hits -= 1
                    self.updating_offset = True
                return

    @property
    def rect(self):
        return pygame.Rect(self.initial_rect[0], self.initial_rect[1]-self.offset, self.initial_rect[2], self.initial_rect[3])
