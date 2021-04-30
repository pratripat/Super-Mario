from .block import Block

class Question_Block(Block):
    def __init__(self, game, rect):
        super().__init__(rect)
        self.game = game
        self.animation = self.game.animations.get_animation('question_block')

    def render(self):
        self.animation.render(self.game.screen, [self.rect[0]-self.game.camera.scroll[0], self.rect[1]-self.game.camera.scroll[1]])

    def update(self):
        self.animation.run(self.game.dt)

        self.up_collision(self.game.entities.mario, self.reveal)

    def reveal(self):
        self.animation = self.game.animations.get_animation('empty_block')
