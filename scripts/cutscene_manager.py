class Cutscene:
    def __init__(self, entity_list, sequential_commands=[], independent_commands=[], function=None, args=[]):
        self.entity_list = entity_list
        self.sequential_commands = []
        self.independent_commands = []
        self.finished = False
        self.function = function
        self.args = args

        self.load_commands(sequential_commands, independent_commands)

    def load_commands(self, sequential_commands, independent_commands):
        for command in sequential_commands:
            object = Command(self.entity_list[command['entity']], command['entity_speed'], command['target_position'])
            self.sequential_commands.append(object)

        for command in independent_commands:
            object = Command(self.entity_list[command['entity']], command['entity_speed'], command['target_position'])
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
            print('finished cutscene')

class Command:
    def __init__(self, entity, entity_speed, target_position):
        self.entity = entity
        self.entity_speed = entity_speed
        self.target_position = target_position
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

        self.movement_timer += 1

        if self.movement_timer >= self.total_time:
            self.finished = True
