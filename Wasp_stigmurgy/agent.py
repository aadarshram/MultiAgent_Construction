from config import RED, BLACK, BLUE, GREEN, WIDTH, HEIGHT, BLOCK_SIZE
import random
import pygame

class Agent:
    ''' This defines properties and action functions for an agent in the system'''

    def __init__(self, x, y, radius, ruleset, cell_properties):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = RED
        self.ruleset = ruleset
        self.cell_properties = cell_properties

    def hit_boundary(self, x, y): 
        if x < 0 or x > WIDTH - BLOCK_SIZE:
            return True
        elif y < 0 or y > HEIGHT - BLOCK_SIZE:
            return True
        else:
            return False
    def __get_neighborhood_properties(self, pos):
        x, y = pos
        neighborhood = [
            (x, y + BLOCK_SIZE), (x + BLOCK_SIZE, y + BLOCK_SIZE), (x + BLOCK_SIZE, y), (x + BLOCK_SIZE, y - BLOCK_SIZE), (x, y - BLOCK_SIZE), (x - BLOCK_SIZE, y - BLOCK_SIZE), (x - BLOCK_SIZE, y), (x - BLOCK_SIZE, y + BLOCK_SIZE) # clockwise from top
        ]
        neighborhood_properties = []
        for cell in neighborhood:
            x, y = cell
            # Enforce boundary condition
            if self.hit_boundary(x, y):
                neighborhood_properties.append(0)
            else:
                neighborhood_properties.append(self.cell_properties[(x, y)])
        return neighborhood_properties
    
    def _make_symmetric(self, neighborhood_properties):
        neighborhood_properties_list = []
        extended_list = neighborhood_properties + neighborhood_properties
        for i in range(len(neighborhood_properties)):
            permut = extended_list[i:i + len(neighborhood_properties)]
            neighborhood_properties_list.append(permut)
        return neighborhood_properties_list
    
    def build(self):
        # Fetch neighborhood properties
        neighborhood_properties = self.__get_neighborhood_properties((self.x, self.y))
        # Get all possible permutations enforcing symmetry
        neighborhood_properties_list = self._make_symmetric(neighborhood_properties)
        # get current cell property
        cell_property = self.cell_properties[(self.x, self.y)]

        # Compare with ruleset and set property
        for rule in self.ruleset:
            if cell_property == 0 and list(rule[0]) in neighborhood_properties_list:
                self.cell_properties[(self.x, self.y)] = rule[1]
                break # Only accept the first applicable rule when multiple satisfies

    def move(self):
        direction = random.choice([(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)])
        self.x += direction[0] * BLOCK_SIZE
        self.y += direction[1] * BLOCK_SIZE

        # Enforce boundary
        if self.x < 0 :
            self.x = 0
        elif self.x > WIDTH - BLOCK_SIZE: 
            self.x = WIDTH - BLOCK_SIZE

        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT - BLOCK_SIZE:
            self.y = HEIGHT - BLOCK_SIZE


    def step(self):
        self.build()
        self.move()

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        # Insert wasp icon for clarity
        # img = pygame.image.load('wasp_icon.jpg')
        # img = pygame.transform.scale(img, (self.radius * 2, self.radius * 2))
        # Blit image onto circle
        # img_rect = img.get_rect(center = (self.x, self.y))
        # surface.blit(img, img_rect)