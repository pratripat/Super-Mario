from .entities.mario import Mario
from .entities.question_block import Question_Block
from .entities.brick import Brick
from .entities.super_mushroom import Super_Mushroom

class Entity_Manager:
    def __init__(self, game):
        self.game = game
        self.mario = Mario(game)
        self.blocks = [Question_Block(game, rect) for rect in self.game.tilemap.get_tiles('question')] + [Brick(game, rect) for rect in self.game.tilemap.get_tiles('brick')]
        self.mushrooms = [Super_Mushroom(game, [700, 100])]
        self.brick_pieces = []

    def run(self):
        for question_block in self.blocks[:]:
            question_block.update()

            if question_block.remove:
                self.blocks.remove(question_block)

        for piece in self.brick_pieces[:]:
            piece.update()
            if piece.offscreen:
                self.brick_pieces.remove(piece)

        for mushroom in self.mushrooms[:]:
            mushroom.update()
            if mushroom.offscreen or mushroom.used:
                self.mushrooms.remove(mushroom)

        self.mario.run()

    def render(self):
        for question_block in self.blocks:
            question_block.render()

        for mushroom in self.mushrooms:
            mushroom.render()

        for piece in self.brick_pieces:
            piece.render()

        self.mario.render()

    def get_colliding_entities(self):
        colliding_blocks = []
        for block in self.blocks:
            colliding_blocks.append(block.rect)

        colliding_blocks.extend(self.game.tilemap.get_tiles('tiles'))

        return colliding_blocks
