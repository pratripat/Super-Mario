from .mario import Mario
from .question_block import Question_Block
from .brick import Brick

class Entity_Manager:
    def __init__(self, game):
        self.game = game
        self.mario = Mario(game)
        self.blocks = [Question_Block(game, rect) for rect in self.game.tilemap.get_tiles('question')] + [Brick(game, rect) for rect in self.game.tilemap.get_tiles('brick')]

    def run(self):
        for question_block in self.blocks[:]:
            question_block.update()

            if question_block.remove:
                self.blocks.remove(question_block)

        self.mario.run()

    def render(self):
        for question_block in self.blocks:
            question_block.render()

        self.mario.render(self.game.screen, self.game.camera.scroll)

    def get_colliding_entities(self):
        colliding_blocks = []
        for block in self.blocks:
            colliding_blocks.append(block.rect)

        def get_distance(block):
            return (block[0]-self.mario.position[0])**2 + (block[1]-self.mario.position[1])**2

        colliding_blocks.sort(key=get_distance)

        colliding_blocks.extend(self.game.tilemap.get_tiles('tiles'))

        return colliding_blocks
