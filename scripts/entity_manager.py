from .entities.mario import Mario
from .entities.question_block import Question_Block
from .entities.power_up_block import Power_Up_Block
from .entities.star_block import Star_Block
from .entities.brick import Brick
from .entities.goomba import Goomba
from .entities.koopa import Koopa, Red_Koopa
from .entities.piranha_plant import Piranha_Plant
from .entities.flagpole import Flagpole
from .entities.coin import Coin
from .entities.lift import Lift
from .entities.firebar import Firebar
from .entities.fire_breathe import Firebreathe
from .entities.bowser import Bowser
from .entities.axe import Axe
from .funcs import *
import pygame

class Entity_Manager:
    def __init__(self, game, position, transition_velocity):
        self.game = game
        self.load_entities(position, transition_velocity)

    def load_entities(self, position, transition_velocity):
        try:
            mario_rect = self.game.tilemap.get_rects_with_id('mario')[0]
        except:
            mario_rect = pygame.Rect(*position,10,10)

        try:
            self.flagpole = Flagpole(self.game, self.game.tilemap.get_rects_with_id('flagpole')[0])
        except:
            self.flagpole = None

        self.mario = Mario(self.game, mario_rect, self.game.mario_data, transition_velocity)
        self.blocks = [Power_Up_Block(self.game, rect) for rect in self.game.tilemap.get_rects_with_id('power_up_question')] + [Star_Block(self.game, rect) for rect in self.game.tilemap.get_rects_with_id('star_question')] + [Question_Block(self.game, rect) for rect in self.game.tilemap.get_rects_with_id('question')] + [Question_Block(self.game, pygame.Rect(*tiles['position'], tiles['image'].get_width(), tiles['image'].get_height()), 'brick', 6, tiles['index']) for tiles in self.game.tilemap.get_tiles_with_id('brick_coin_6')] + [Brick(self.game, pygame.Rect(*tiles['position'], tiles['image'].get_width(), tiles['image'].get_height()), tiles['index']) for tiles in self.game.tilemap.get_tiles_with_id('brick')]

        self.enemies = [Goomba(self.game, rect) for rect in self.game.tilemap.get_rects_with_id('goomba')]+[Koopa(self.game, rect) for rect in self.game.tilemap.get_rects_with_id('koopa')]+[Koopa(self.game, rect, 'flying') for rect in self.game.tilemap.get_rects_with_id('koopa_flying')]+[Red_Koopa(self.game, rect) for rect in self.game.tilemap.get_rects_with_id('red_koopa')]+[Red_Koopa(self.game, rect, 'flying') for rect in self.game.tilemap.get_rects_with_id('red_koopa_flying')]+[Piranha_Plant(self.game, rect) for rect in self.game.tilemap.get_rects_with_id('piranha_plant')]+[Bowser(self.game, rect) for rect in self.game.tilemap.get_rects_with_id('bowser')]

        self.coins = [Coin(self.game, rect) for rect in self.game.tilemap.get_rects_with_id('coin')]
        self.lifts = [Lift(self.game, rect) for rect in self.game.tilemap.get_rects_with_id('lift')]
        self.firebars = [Firebar(self.game, tile['id'], tile['position'], tile['index']) for tile in self.game.tilemap.get_tiles_with_id('firebar_6')]
        self.firebreathes = [Firebreathe(self.game, rect) for rect in self.game.tilemap.get_rects_with_id('firebreathe')]
        self.axes = [Axe(self.game, rect) for rect in self.game.tilemap.get_rects_with_id('axe')]
        self.items = []
        self.brick_pieces = []
        self.fireballs = []
        self.coin_animations = []
        self.animations = {}
        self.breaking_bridge = False
        self.waiting_timer = 0

    def run(self):
        self.update_pipe_transitions()

        if self.flagpole:
            self.flagpole.run()

        self.mario.run()

        if self.breaking_bridge:
            self.break_bridge()

        if self.game.paused or self.game.flag_animation:
            return

        for enemy in self.enemies[:]:
            enemy.update()

            if enemy.remove or enemy.far_from_mario:
                self.enemies.remove(enemy)

        for question_block in self.blocks[:]:
            question_block.update()

            if question_block.remove:
                self.blocks.remove(question_block)

        for fireball in self.fireballs[:]:
            fireball.update()
            if fireball.remove:
                self.fireballs.remove(fireball)

                animation = self.game.animations.get_animation('blast')
                self.animations[animation] = fireball.center

            elif not fireball.on_screen:
                self.fireballs.remove(fireball)

        for firebar in self.firebars:
            firebar.update()

        for firebreathe in self.firebreathes:
            firebreathe.update()

        for piece in self.brick_pieces[:]:
            piece.update()
            if piece.offscreen:
                self.brick_pieces.remove(piece)

        for item in self.items[:]:
            item.update()
            if item.far_from_mario or item.used:
                self.items.remove(item)

        for lift in self.lifts[:]:
            lift.update()
            if lift.offscreen and lift in self.lifts:
                self.lifts.remove(lift)

        for coin in self.coins[:]:
            coin.update()
            if rect_rect_collision(coin.rect, self.mario.rect):
                coin.coin_sfx.play()
                self.coins.remove(coin)
                self.game.ui.coins += 1

        for axe in self.axes:
            axe.update()

        delete_list = []
        for animation, position in self.animations.items():
            animation.run(self.game.dt)

            if int(animation.frame) == animation.animation_data.duration():
                delete_list.append(animation)

        for animation in delete_list:
            del self.animations[animation]

        for coin_animation in self.coin_animations[:]:
            coin_animation.update()
            if coin_animation.finished:
                self.coin_animations.remove(coin_animation)

    def render(self):
        for item in self.items:
            item.render()

        for question_block in self.blocks:
            question_block.render()

        for lift in self.lifts:
            lift.render()

        for axe in self.axes:
            axe.render()

        for coin in self.coins:
            coin.render()

        for enemy in self.enemies:
            enemy.render()

        for piece in self.brick_pieces:
            piece.render()

        for firebar in self.firebars:
            firebar.render()

        for firebreathe in self.firebreathes:
            firebreathe.render()

        for fireball in self.fireballs:
            fireball.render()

        for animation, position in self.animations.items():
            animation.render(self.game.screen, (position[0]-self.game.camera.scroll[0], position[1]-self.game.camera.scroll[1]))

        for animation in self.coin_animations:
            animation.render()

        if self.flagpole:
            self.flagpole.render()

        self.mario.render()

    def break_bridge(self):
        self.game.paused = True

        if self.waiting_timer > 0:
            self.waiting_timer -= 1
            return

        bridge_positions = sorted([tile['position'] for tile in self.game.tilemap.get_tiles_with_id('ground') if tile['index'] == 14])

        if len(bridge_positions) > 0:
            self.game.tilemap.remove_entity('ground', pos=bridge_positions[-1])
            self.waiting_timer = 5
            self.game.camera.scroll[0] -= 4
        else:
            self.breaking_bridge = False
            self.game.paused = False

            for enemy in self.enemies:
                enemy.dead = enemy.falling = True

            self.firebreathes.clear()

            self.game.load_cutscene('data/configs/cutscenes/castle_clear.json', self.game.load_level, [self.game.level+1])

    def update_pipe_transitions(self):
        for (file_path, position, world_type, direction1, direction2), rect in self.game.pipe_guides.rects.items():
            if rect_rect_collision(self.mario.rect, rect):
                if direction1[1] > 0 and not self.mario.crouching:
                    continue
                if direction1[0] > 0 and not self.mario.directions['right'] and not self.mario.collisions['bottom']:
                    continue
                if direction1[0] < 0 and not self.mario.directions['left'] and not self.mario.collisions['bottom']:
                    continue

                self.mario.play_pipe_transition(file_path, position, world_type, direction1, direction2)
                break

    def get_colliding_entities(self, entity=None, enemies=False, lifts=True):
        colliding_blocks = []
        for block in self.blocks:
            if block.type == 'question':
                if not block.is_invisible:
                    colliding_blocks.append(block.rect)
            else:
                colliding_blocks.append(block.rect)

        if lifts:
            for lift in self.lifts:
                colliding_blocks.append(lift.rect)

        if enemies:
            for enemy in self.enemies:
                if entity == enemy:
                    continue
                colliding_blocks.append(enemy.rect)

        colliding_blocks.extend(self.game.tilemap.get_rects_with_id('ground'))
        colliding_blocks.extend(self.game.tilemap.get_rects_with_id('pipes'))
        colliding_blocks.extend(self.game.tilemap.get_rects_with_id('mushroom'))

        return colliding_blocks

    def get_enemies(self):
        return self.enemies
