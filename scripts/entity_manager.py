from .entities.mario import Mario
from .entities.question_block import Question_Block
from .entities.power_up_block import Power_Up_Block
from .entities.brick import Brick
from .entities.goomba import Goomba
from .entities.koopa import Koopa
from .entities.flagpole import Flagpole
from .funcs import *
import pygame

class Entity_Manager:
    def __init__(self, game, position):
        self.game = game
        self.load_entities(position)

    def load_entities(self, position):
        try:
            mario_rect = self.game.tilemap.get_rects_with_id('mario')[0]
        except:
            mario_rect = pygame.Rect(*position, 10, 10)

        try:
            self.flagpole = Flagpole(self.game, self.game.tilemap.get_rects_with_id('flagpole')[0])
        except:
            self.flagpole = None

        self.mario = Mario(self.game, mario_rect)
        self.blocks = [Power_Up_Block(self.game, rect) for rect in self.game.tilemap.get_rects_with_id('power_up_question')] + [Question_Block(self.game, rect) for rect in self.game.tilemap.get_rects_with_id('question')] + [Brick(self.game, pygame.Rect(*tiles['position'], tiles['image'].get_width(), tiles['image'].get_height()), tiles['index']) for tiles in self.game.tilemap.get_tiles_with_id('brick')]
        self.enemies = [Goomba(self.game, rect) for rect in self.game.tilemap.get_rects_with_id('goomba')]+[Koopa(self.game, rect) for rect in self.game.tilemap.get_rects_with_id('koopa')]
        self.items = []
        self.brick_pieces = []
        self.fireballs = []

    def run(self):
        self.update_pipe_transitions()

        if self.flagpole:
            self.flagpole.run()

        self.mario.run()

        if self.game.paused or self.game.level_finished:
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

        for piece in self.brick_pieces[:]:
            piece.update()
            if piece.offscreen:
                self.brick_pieces.remove(piece)

        for item in self.items[:]:
            item.update()
            if item.far_from_mario or item.used:
                self.items.remove(item)

    def render(self):
        for item in self.items:
            item.render()

        for question_block in self.blocks:
            question_block.render()

        for piece in self.brick_pieces:
            piece.render()

        for enemy in self.enemies:
            enemy.render()

        for fireball in self.fireballs:
            fireball.render()

        if self.flagpole:
            self.flagpole.render()

        self.mario.render()

    def update_pipe_transitions(self):
        for (file_path, position, direction1, direction2), rect in self.game.pipe_guides.rects.items():
            if rect_rect_collision(self.mario.rect, rect):
                if direction1[1] > 0 and not self.mario.crouching:
                    continue
                if direction1[0] > 0 and not self.mario.directions['right'] and not self.mario.collisions['bottom']:
                    continue
                if direction1[0] < 0 and not self.mario.directions['left'] and not self.mario.collisions['bottom']:
                    continue

                self.mario.play_pipe_transition(file_path, position, direction1, direction2)
                break

    def get_colliding_entities(self, entity=None, enemies=False):
        colliding_blocks = []
        for block in self.blocks:
            colliding_blocks.append(block.rect)

        if enemies:
            for enemy in self.enemies:
                if entity == enemy:
                    continue
                colliding_blocks.append(enemy.rect)

        colliding_blocks.extend(self.game.tilemap.get_rects_with_id('ground'))
        colliding_blocks.extend(self.game.tilemap.get_rects_with_id('pipes'))

        return colliding_blocks

    def get_enemies(self):
        return self.enemies
