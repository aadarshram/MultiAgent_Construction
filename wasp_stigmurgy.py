'''
Overview: 
This code attempts to reproduce interesting 2D patterns created by social wasp species 
by simulating a set of random agents that follow a certain rule-based mechanism.

Context:
One theory behind how wasps collaborate and build interesting architectures is that
they use environmental cues to communicate with each other and also decide on their actions. One model dictates the
existence of a property called 'stigmurgy' either qualitative or quantitative which are some kind of messages left by wasps in their environment
for others to see and act accordingly.

After extensive studies on intricate details of nest architectures of various species a set of rules can be derived for each neighbourhood configuration
that dictates the corresponding natural patterns to emerge.

For example, the Vespa genus build their architecture with a local neighborhood ruleset like this:

  [1 0 0 0 0 0 0 0] -> [2]
  [1 2 0 0 0 0 0 0] -> [2]
  [1 0 0 0 0 0 0 2] -> [2]
  [2 0 0 0 0 0 2 1] -> [2]
  [0 0 0 0 2 1 2 0] -> [2]
  [2 0 0 0 0 0 1 2] -> [2]
  [0 0 0 0 2 2 1 0] -> [2]
  [2 0 0 0 0 0 2 1] -> [2]
  [1 2 0 0 0 0 0 2] -> [2]
  [2 2 0 0 0 0 0 2] -> [2]
  [2 2 0 0 0 2 2 2] -> [2]
  [2 0 0 0 0 0 2 2] -> [2]
  [2 2 2 0 0 0 2 2] -> [2]
  [1 2 2 0 0 0 2 2] -> [2]
  [2 2 2 2 0 2 2 2] -> [2]
  [2 0 0 0 0 2 2 1] -> [2]
  [2 2 0 0 0 0 2 1] -> [2]
  [2 2 0 0 0 2 2 1] -> [2]

Where the first  with eight elements corresponds to neighborhood of a certain cell, and the next  gives the material type to place if the neighborhood matches

Initially, random patches of the different materials are set up with certain corresponding probabilities.
'''

# I use a python library called 'mesa' which is useful for modelling multi-agent systems

# Import libraries
import mesa
import mesa.visualization.ModularVisualization
import mesa.visualization.modules

import random

# class SingleGridWithProperties(mesa.space.SingleGrid):
#     def __init__(self, width, height, torus):
#         super().__init__(width, height, torus)
#         self.cell_properties = {(x, y): 0 for x in range(width) for y in range(height)}
    
#     def set_cell_property(self, pos, value):
#         self.cell_properties[pos] = value
    
#     def get_cell_property(self, pos):
#         return self.cell_properties[pos]
#     def get_neighborhoodcells_property(self, neighborhood):
#         return [self.get_cell_property(pos) for pos in neighborhood]
    
    # Modify according to PS
ruleset = ( # Ichneumon-ruleset # global
      (( 1, 1, 0, 0, 0, 0, 0, 1), 2),
      (( 1, 0, 0, 0, 0, 0, 0, 0), 1),
      (( 2, 0, 0, 0, 1, 0, 0, 0), 1),
      (( 1, 1, 0, 0, 1, 0, 0, 1), 1),
      (( 0, 2, 0, 0, 1, 0, 0, 2), 1),
      (( 1, 1, 2, 0, 0, 0, 2, 1), 1),
      (( 0, 2, 0, 0, 1, 0, 0, 0), 1),
      (( 0, 0, 0, 0, 1, 0, 0, 2), 1),
      (( 1, 1, 2, 0, 0, 0, 0, 1), 1),
      (( 1, 1, 0, 0, 0, 0, 0, 1), 1),
      (( 0, 1, 0, 0, 0, 0, 0, 1), 1),
      (( 2, 0, 0, 0, 0, 0, 0, 0), 2),
      (( 2, 2, 0, 0, 0, 0, 0, 2), 2))

class WaspAgent(mesa.Agent):
    '''Represents a worker wasp agent in simulation.'''

    def __init__(self, agent_id, model):
        '''
        Create an agent in the given state and position.
        '''
        super().__init__(agent_id, model)
        self.model = model
        self.ruleset = ruleset

    def get_neighborhood(self):
        return self.model.grid.get_neighborhood(self.pos, moore = True, include_center = True)
    def get_cell_value(self, pos):
        cell_contents = self.model.grid.get_cell_list_contents([pos])
        for agent in cell_contents:
            if type(agent) is Block:
                return agent.value
    def get_neighborhood_values(self):
        neighborhood = self.get_neighborhood()
        neighborhood_cell_values = []
        for pos in neighborhood:
            cell_value = self.get_cell_value(pos)
            neighborhood_cell_values.append(cell_value)
        return neighborhood_cell_values
            
    def build(self):
        neighborhood_cell_values = self.get_neighborhood_values()

        # rules on neighborhood
        #------------------------------------------
        # if then and set cell property of pos
        for rule in ruleset:
            if neighborhood_cell_values[1] == 0 and neighborhood_cell_values[1:] == list(rule[0]): # If no block in current position and surrounding values match pattern
                # set_cell_property(pos, rule[1])
                # spawn a block agent 
                block_agent = Block(random.random(), self.model, rule[1])
                self.model.grid.place_agent(block_agent, self.pos)
                self.model.schedule.add(block_agent)

        
    def move(self):
        next_pos = self.random.choice(self.get_neighborhood())
        self.model.grid.move_agent(self, next_pos)
        self.pos = next_pos

    def step(self):
        '''Define agent's action on step'''
        # Set material acc to rules
        self.build()
        # move agent
        self.move()

class Block(mesa.Agent): # property of cell; defined to be agent in mesa
    ''' Agent for materials'''
    def __init__(self, agent_id, model, value):
        super().__init__(agent_id, model)
        self.value = value
    
    def step(self):
        pass

class WaspStigmurgyModel(mesa.Model):
    '''A model with some number of random agents and properties'''
    
    def __init__(self, N, width, height):
        super().__init__()
        self.num_agents = N
        self.width = width
        self.height = height

        self.grid = mesa.space.MultiGrid(self.width, self.height, torus = False)

        # # Set initial material patches as cell properties
        # for x in range(width):
        #     for y in range(height):
        #         patch = random.choices([0, 1, 2], [0.9, 0.075, 0.025]) # 0 -no material, 1 and 2 are material types
        #         self.grid.set_cell_property((x,y), patch)

        self.schedule = mesa.time.RandomActivationByType(self)
        

        # Create agents
        occupied = []
        for i in range(self.num_agents):
            # Set initial pos of agents
            x = 0
            y = 0
            while True:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                if (x, y) not in occupied:
                    break
            wasp_agent = WaspAgent(random.random(), self)
            self.grid.place_agent(wasp_agent, (x, y))
            occupied.append((x, y))
            self.schedule.add(wasp_agent)

        # Set initial material patches as agents
        for x in range(width):
            for y in range(height):
                block_value = random.choices([0, 1, 2], [0.9, 0.075, 0.025]) # 0 -no material, 1 and 2 are material types
                block_agent = Block(random.random(), self, block_value)
                self.grid.place_agent(block_agent, (x, y))
                self.schedule.add(block_agent)

        # self.datacollector = mesa.DataCollector()

        self.running = True

    def step(self):
        '''Advance the model by one step'''
        # self.datacollector.collect(self)
        self.schedule.step()

def agents_portrayal(agent):
    ''' Agent characteristics'''
    if agent is None:
        return
    if type(agent) is WaspAgent:
        portrayal = {'Shape': 'circle',
                    'Color': 'red',
                    'Filled': 'true',
                    "w": 1,
                    "h": 1,
                    "Layer": 0,
                    'r': 0.5}
    elif type(agent) is Block:
        portrayal = {'Shape': 'circle',
                    'Color': 'blue',
                    'Filled': 'true',
                    "w": 1,
                    "h": 1,
                    "Layer": 0,
                    'r': 0.5}

    return portrayal

# model = WaspStigmurgyModel(100, 10, 10)
# for i in range(10):
#     model.step()

# config
width = 50
height = 50
num_agents = 50

# {
#         "type": "SliderInt",
#         "value": 50,
#         "label": "Number of agents:",
#         "min": 10,
#         "max": 100,
#         "step": 1,
#         "description": "Number of agents:"
#     },
model_params = {
    "N": num_agents,
    "width": width,
    "height": height,
}

# Server
canvas_element  = mesa.visualization.modules.CanvasGrid(agents_portrayal, model_params["width"], model_params["height"], 500, 500)

# model = WaspStigmurgyModel(num_agents, width, height, ruleset)
# results = mesa.batch_run(
#     WaspStigmurgyModel,
#     parameters = {"width": 10, "height": 10, "N": 100},
#     iterations = 50,
#     display_progress = True
# )


server = mesa.visualization.ModularVisualization.ModularServer(WaspStigmurgyModel, [canvas_element], 'WaspStigmurgyModel', model_params)

server.port = 8521
server.launch()

