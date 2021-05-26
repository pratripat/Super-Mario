import pygame, json

class Pipe_Guides:
    def __init__(self, game):
        self.game = game
        self.pipe_guides = {}
        self.rects = {}
        self.load_pipe_paths()

    def load_pipe_paths(self):
        for guide in self.game.tilemap.get_tiles_with_id('pipe_guides'):
            print(guide['position'])
            
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


    def get_end_pipe(self, guide, directions):
        current_position = guide['position'].copy()
        direction = directions[str(guide['index'])]

        current_position[0] += direction[0]*self.game.tilemap.RES
        current_position[1] += direction[1]*self.game.tilemap.RES

        new_guide = self.game.tilemap.get_tiles_with_position(guide['id'], current_position)

        if len(new_guide):
            return self.get_end_pipe(new_guide[0], directions)

        return current_position, direction
