import pygame

class Entity:
    def __init__(self, animations, id, position, current_animation, rect=None):
        self.animations = animations
        self.id = id
        self.current_animation_id = f'{self.id}_{current_animation}'
        self.current_animation = self.animations.get_animation(self.current_animation_id)
        self.velocity = [0,0]
        self.flipped = False
        self.collisions = {i:False for i in ['top', 'right', 'bottom', 'left']}

        if rect:
            self.rect = pygame.Rect(*rect.topleft, rect.width*self.scale, rect.height*self.scale)
            self.offset = [self.rect[0]-position[0], self.rect[1]-position[1]]
        else:
            self.rect = pygame.Rect(*position, *self.current_animation.image.get_size())
            self.offset = [0,0]

    def render(self, surface, scroll=[0,0], colorkey=None, vertical_flip=False):
        self.current_animation.render(surface, (self.position[0]-scroll[0], self.position[1]-scroll[1]), [self.flipped, vertical_flip], colorkey)

        # pygame.draw.rect(surface, (255,0,0), [self.rect[0]-scroll[0], self.rect[1]-scroll[1], self.rect[2], self.rect[3]])

    #Updates the animation
    def update(self, dt):
        self.current_animation.run(dt)

    def move(self, rects, dt, tilemap=None):
        self.collisions = {k:False for k in ('top', 'right', 'bottom', 'left')}

        self.rect[0] += round(self.velocity[0]*dt*80)
        hit_list = self.get_colliding_objects(rects)

        for obj in hit_list:
            if self.velocity[0] > 0:
                self.rect.right = obj.left
                self.collisions['right'] = True
            if self.velocity[0] < 0:
                self.rect.left = obj.right
                self.collisions['left'] = True

        self.rect[1] += round(self.velocity[1]*dt*80)
        hit_list = self.get_colliding_objects(rects)

        for obj in hit_list:
            if self.velocity[1] > 0:
                self.rect.bottom = obj.top
                self.collisions['bottom'] = True
            if self.velocity[1] < 0:
                self.rect.top = obj.bottom
                self.collisions['top'] = True

        if tilemap:
            if self.rect[0] < tilemap.left:
                self.rect[0] = tilemap.left
            if self.rect[0] > tilemap.right-self.get_width():
                self.rect[0] = tilemap.right-self.get_width()

    #Returns the rects the player is colliding with
    def get_colliding_objects(self, objs):
        hit_list = []
        for obj in objs:
            if obj.colliderect(self.rect):
                hit_list.append(obj)

        return hit_list

    #Sets the current animation of the entity
    def set_animation(self, animation):
        animation = f'{self.id}_{animation}'

        if self.current_animation_id == animation:
            return

        if animation in self.animations.animations:
            self.current_animation = self.animations.get_animation(animation)
            self.current_animation_id = animation

    def set_position(self, position):
        self.rect[0] = position[0] + self.offset[0]
        self.rect[1] = position[1] + self.offset[1]

    def reset_rect(self):
        self.rect = pygame.Rect(*self.position, *self.current_animation.image.get_size())
        self.offset = [0,0]

    #FLips the entity horizontally (when rendering only)
    def flip(self, bool):
        self.flipped = bool

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

    def get_size(self):
        return self.rect.size


    @property
    def position(self):
        return [self.rect[0]-self.offset[0], self.rect[1]-self.offset[1]]

    @property
    def scale(self):
        return self.current_animation.animation_data.config['scale']

    #Returns the current animation's current image
    @property
    def image(self):
        return self.current_animation.image

    @property
    def center(self):
        return [self.rect[0]+self.get_width()/2, self.rect[1]+self.get_height()/2]
