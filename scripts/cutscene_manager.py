class Cutscene:
    def __init__(self, entity_list, font, sequential_commands=[], independent_commands=[], function=None, args=[]):
        self.entity_list = entity_list
        self.font = font
        self.sequential_commands = []
        self.independent_commands = []
        self.finished = False
        self.function = function
        self.args = args

        self.load_commands(sequential_commands, independent_commands)

    def load_commands(self, sequential_commands, independent_commands):
        for command in sequential_commands:
            object = Command(self.font, self.entity_list[command['entity']], command['entity_speed'], command['target_position'], command['waiting_timer'], command['text'], command['position'])
            self.sequential_commands.append(object)

        for command in independent_commands:
            object = Command(self.font, self.entity_list[command['entity']], command['entity_speed'], command['target_position'], command['waiting_timer'], command['text'], command['position'])
            self.independent_commands.append(object)

    def update(self):
        self.sequential_commands[0].update()
        if self.sequential_commands[0].finished:
            self.sequential_commands.pop(0)

        for command in self.independent_commands[:]:
            command.update()

            if command.finished:
                self.independent_commands.remove(command)

        if len(self.sequential_commands) == 0 and len(self.independent_commands) == 0:
            self.finished = True

class Command:
    def __init__(self, font, entity, entity_speed, target_position, waiting_timer, text, position):
        self.font = font
        self.entity = entity
        self.entity_speed = entity_speed
        self.target_position = target_position
        self.waiting_timer = waiting_timer
        self.text = text
        self.position = position
        self.movement_timer = 0
        self.finished = False

        self.calculate_velocity()

    def calculate_velocity(self):
        vector = [self.target_position[0]-self.entity.position[0], 0]
        magnitude = vector[0]

        if magnitude > 0:
            vector[0] /= magnitude

        self.velocity = [vector[0]*self.entity_speed, vector[1]*self.entity_speed]

        self.total_time = magnitude/self.entity_speed

    def update(self):
        if self.velocity[0] > 0:
            self.entity.directions['right'] = True
        if self.velocity[0] < 0:
            self.entity.directions['left'] = True
        if self.velocity[0] == 0:
            self.entity.directions['left'] = False
            self.entity.directions['right'] = False
            self.entity.velocity[0] = 0

        self.movement_timer += 1

        if self.movement_timer >= self.total_time:
            if self.waiting_timer <= 0:
                self.finished = True
            else:
                self.waiting_timer -= 1
                game = self.entity.game
                game.renderer.texts.append({'text': self.text, 'position': [self.position[0]-game.camera.scroll[0], self.position[1]-game.camera.scroll[1]]})
                self.text = ''
