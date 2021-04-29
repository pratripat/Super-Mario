from .mario import Mario

class Entity_Manager:
    def __init__(self, game):
        self.game = game
        self.mario = Mario(game)

    def run(self):
        self.mario.run()

    def render(self):
        self.mario.render(self.game.screen, self.game.camera.scroll)
