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
    def __init__(self, game):
        self.game = game
        self.flagpole = Flagpole(game, self.game.tilemap.get_rects_with_id('flagpole')[0])
        self.mario = Mario(game, self.game.tilemap.get_rects_with_id('mario')[0])
        self.blocks = [Power_Up_Block(game, rect) for rect in self.game.tilemap.get_rects_with_id('power_up_question')] + [Question_Block(game, rect) for rect in self.game.tilemap.get_rects_with_id('question')] + [Brick(game, rect) for rect in self.game.tilemap.get_rects_with_id('brick')]
        self.enemies = [Goomba(game, rect) for rect in self.game.tilemap.get_rects_with_id('goomba')]+[Koopa(game, rect) for rect in self.game.tilemap.get_rects_with_id('koopa')]
        self.items = []
        self.brick_pieces = []

    def run(self):
        self.flagpole.run()

        self.mario.run()

        if self.game.paused or self.game.level_finished:
            return

        for enemy in self.enemies[:]:
            enemy.update()

            if enemy.remove:
                self.enemies.remove(enemy)

        for question_block in self.blocks[:]:
            question_block.update()

            if question_block.remove:
                self.blocks.remove(question_block)

        for piece in self.brick_pieces[:]:
            piece.update()
            if piece.offscreen:
                self.brick_pieces.remove(piece)

        for item in self.items[:]:
            item.update()
            if item.far_from_mario or item.used:
                self.items.remove(item)

        for (position, direction1, direction2), rect in self.game.pipe_guides.rects.items():
            if rect_rect_collision(self.mario.rect, rect):
                if direction1[1] > 0 and not self.mario.crouching:
                    continue
                if direction1[0] > 0 and not self.mario.velocity[0] > 0:
                    continue
                if direction1[0] < 0 and not self.mario.velocity[0] < 0:
                    continue

                self.mario.play_pipe_transition(position, direction1, direction2)
                break

    def render(self):
        for item in self.items:
            item.render()

        for question_block in self.blocks:
            question_block.render()

        for piece in self.brick_pieces:
            piece.render()

        for enemy in self.enemies:
            enemy.render()

        self.mario.render()

    def get_colliding_entities(self):
        colliding_blocks = []
        for block in self.blocks:
            colliding_blocks.append(block.rect)

        colliding_blocks.extend(self.game.tilemap.get_rects_with_id('ground'))
        colliding_blocks.extend(self.game.tilemap.get_rects_with_id('pipes'))

        return colliding_blocks

    def get_enemies(self):
        return self.enemies
