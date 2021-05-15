import json

class Pipe_Guides:
    def __init__(self, game):
        self.game = game
        self.pipe_guides = {}
        self.load_pipe_paths()

    def load_pipe_paths(self):
        directions = json.load(open('data/configs/pipe_guide_direction.json', 'r'))

        for guide in self.game.tilemap.get_tiles_with_id('pipe_guides'):
            end_position = self.get_end_pipe(guide, directions)
            self.pipe_guides[tuple(guide['position'])] = tuple(end_position)

        duplicate = {v:k for k,v in self.pipe_guides.items()}
        self.pipe_guides = {v:k for k,v in duplicate.items()}

    def get_end_pipe(self, guide, directions):
        current_position = guide['position'].copy()
        direction = directions[str(guide['index'])]

        current_position[0] += direction[0]*self.game.tilemap.RES
        current_position[1] += direction[1]*self.game.tilemap.RES

        new_guide = self.game.tilemap.get_tiles_with_position(guide['id'], current_position, guide['layer'])

        if len(new_guide):
            return self.get_end_pipe(new_guide[0], directions)

        return current_position
