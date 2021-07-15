from .entities.score_text import Score_Text
import pygame

class Score_System:
    def __init__(self, game):
        self.game = game
        self.mario_jumps = 0
        self.score_order = [50, 100, 200, 400, 500, 800, 1000, 2000, 4000, 5000, 8000, 10000]
        self.score_entity = {
            'enemy': {
                'goomba': 1,
                'koopa': 1,
                'blooper': 2,
                'red_cheep_cheep': 2,
                'grey_cheep_cheep': 2,
                'cheep_cheep': 2,
                'piranha_plant': 2,
                'bowser': 9
            },
            'others': {
                'time': 0,
                'brick': 0,
                'coin': 2,
                'power_up': 6,
                'flagpole_100': 1,
                'flagpole_400': 3,
                'flagpole_800': 5,
                'flagpole_2000': 7,
                'flagpole_5000': 9,
            }
        }
        self.one_up_sfx = pygame.mixer.Sound('data/sfx/one_up.wav')

    def add_score(self, type, id, object=None):
        index = self.score_entity[type][id]

        if type == 'enemy':
            index += self.mario_jumps
            self.mario_jumps += 1

        score = self.score_order[min(index, len(self.score_order)-1)]

        if score >= 10000:
            self.game.entities.mario.lives += 1
            score = '1 up'
            self.one_up_sfx.play()
        else:
            self.game.ui.score += score

        if type != 'enemy' and id != 'power_up' and id not in ['flagpole_100', 'flagpole_400', 'flagpole_800', 'flagpole_2000', 'flagpole_5000']:
            return

        self.game.entities.score_texts.append(Score_Text(self.game, str(score), object.position.copy()))
