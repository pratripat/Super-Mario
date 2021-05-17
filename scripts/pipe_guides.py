import pygame, json

class Pipe_Guides:
    def __init__(self, game):
        self.game = game
        self.pipe_guides = {}
        self.rects = {}
        self.load_pipe_paths()

    def load_pipe_paths(self):
        directions = json.load(open('data/configs/pipe_guide_direction.json', 'r'))

        for guide in self.game.tilemap.get_tiles_with_id('pipe_guides'):
            end_position, direction2 = self.get_end_pipe(guide, directions)
            direction1 = directions[str(guide['index'])]
            self.pipe_guides[tuple(guide['position'])] = (tuple(end_position), tuple(direction1), tuple(direction2))

        self.pipe_guides = dict(reversed(list(self.pipe_guides.items())))
        duplicate = {v:k for k,v in self.pipe_guides.items()}
        self.pipe_guides = {v:k for k,v in duplicate.items()}

        for start_position, (end_position, direction1, direction2) in self.pipe_guides.items():
            rect = pygame.Rect(*start_position, self.game.tilemap.RES*2, self.game.tilemap.RES*2)
            self.rects[(end_position, direction1, direction2)] = rect

    def get_end_pipe(self, guide, directions):
        current_position = guide['position'].copy()
        direction = directions[str(guide['index'])]

        current_position[0] += direction[0]*self.game.tilemap.RES
        current_position[1] += direction[1]*self.game.tilemap.RES

        new_guide = self.game.tilemap.get_tiles_with_position(guide['id'], current_position)

        if len(new_guide):
            return self.get_end_pipe(new_guide[0], directions)

        return current_position, direction
