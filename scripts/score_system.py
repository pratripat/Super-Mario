class Score_System:
    def __init__(self, game):
        self.game = game
        self.mario_jumps = 0
        self.score_order = [50, 100, 200, 400, 500, 800, 1000, 2000, 4000, 5000, 8000]
        self.score_entity = {
            'enemy': {
                'goomba': 1,
                'koopa': 1,
                'blooper': 2,
                'cheep_cheep': 2,
                'piranha_plant': 2,
                'bowser': 9
            },
            'others': {
                'time': 0,
                'brick': 0,
                'coin': 2,
                'power_up': 6
            }
        }

    def add_score(self, type, id):
        index = self.score_entity[type][id]

        if type == 'enemy':
            index += self.mario_jumps
            self.mario_jumps += 1

        self.game.ui.score += self.score_order[min(index, len(self.score_order))]
