import pygame, sys, json
from .funcs import *

graphics_file_path = 'data/graphics/spritesheet/'
res = 48

class TileMap:
    def __init__(self, filename):
        self.tiles = []
        self.filename = filename
        self.load_map()

    #Loads the json file (map) and stores all the images
    def load_map(self):
        data = json.load(open(self.filename, 'r'))

        for entity in data.values():
            id = entity['id']
            position = entity['position']
            position = [position[0]*res, position[1]*res]
            index = entity['index']
            layer = entity['layer']
            dimensions = entity['dimensions']
            spritesheet_path = graphics_file_path+id+'.png'

            try:
                image = load_images_from_spritesheet(spritesheet_path)[index]

                offset = self.load_image_offset(image, dimensions, id, index)
                image = pygame.transform.scale(image, dimensions)
                self.tiles.append({'image':image, 'position':position, 'offset': offset, 'layer':layer, 'id': id})
            except Exception as er:
                try:
                    image = pygame.image.load(spritesheet_path).convert()
                    image.set_colorkey((0,0,0))
                    offset = self.load_image_offset(image, dimensions, 'hound', index)
                    image = pygame.transform.scale(image, dimensions)
                    self.tiles.append({'image':image, 'position':position, 'offset': offset, 'layer':layer, 'id': id})
                except Exception as e:
                    print(f'could not load {spritesheet_path}')

        #Sorting the tiles according to the layer
        def get_layer(dict):
            return dict['layer']

        self.tiles.sort(key=get_layer)

        record_left = float('inf')
        record_right = -float('inf')
        record_top = float('inf')
        record_bottom = -float('inf')

        for tile in self.tiles:
            if tile['layer'] == 0:
                if tile['position'][0] < record_left:
                    record_left = tile['position'][0]
                if tile['position'][0]+tile['image'].get_width() > record_right:
                    record_right = tile['position'][0]+tile['image'].get_width()
                if tile['position'][1] < record_top:
                    record_top = tile['position'][1]
                if tile['position'][1]+tile['image'].get_height() > record_bottom:
                    record_bottom = tile['position'][1]+tile['image'].get_height()

        self.left = record_left
        self.right = record_right
        self.top = record_top
        self.bottom = record_bottom

    def load_image_offset(self, image, dimensions, id, index):
        try:
            offset_data = json.load(open(f'data/configs/offsets/{id}_offset.json', 'r'))
            offset = offset_data[str(index)]
            offset[0] *= dimensions[0]/image.get_width()
            offset[1] *= dimensions[1]/image.get_height()
        except:
            offset = [0,0]

        return offset

    #Returns tiles with same id and layer(not necessary)
    def get_tiles(self, id, layer=None):
        tiles = []

        for tile in self.tiles:
            if tile['id'] == id:
                if layer != None:
                    if tile['layer'] != layer:
                        continue

                rect = pygame.Rect(*tile['position'], *tile['image'].get_size())
                tiles.append(rect)

        return tiles
