class Score_Text:
    def __init__(self, game, text, position):
        self.game = game
        self.text = text
        self.position = position
        self.timer = 1

    def render(self):
        self.game.font.render(self.game.screen, self.text, (self.position[0]-self.game.camera.scroll[0], self.position[1]-self.game.camera.scroll[1]), center=[True, False], scale=3)

    def update(self):
        self.position[1] -= 1
        self.timer -= self.game.dt

    @property
    def remove(self):
        return self.timer <= 0
