import pygame, json

class Pipe_Guides:
    def __init__(self, game):
        self.game = game
        self.pipe_guides = {}
        self.rects = {}
        self.load_pipe_paths()

    def load_pipe_paths(self):
        try:
            # for guide in self.game.tilemap.get_tiles_with_id('pipe_guides'):
            #     print(guide['position'])

            directions = json.load(open('data/configs/pipe_guide_direction.json', 'r'))
            level = json.load(open('data/levels/level_order.json', 'r'))[self.game.level]
            end_positions = json.load(open(f'data/levels/pipe_guides/{level}.json', 'r'))
            positions = []

            for guide in self.game.tilemap.get_tiles_with_id('pipe_guides'):
                position, file_path, direction = end_positions[str(guide['position'])]
                self.pipe_guides[tuple(guide['position'])] = (file_path, tuple(position), tuple(directions[str(guide['index'])]), tuple(directions[str(direction)]))

            for start_position, (file_path, end_position, direction1, direction2) in self.pipe_guides.items():
                rect = pygame.Rect(*start_position, self.game.tilemap.RES*2, self.game.tilemap.RES*2)
                self.rects[(file_path, end_position, direction1, direction2)] = rect
        except:
            pass
