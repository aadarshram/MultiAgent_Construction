import rulesets
from agent import Agent
from config import BLACK, WHITE, RED, BLUE, GREEN, WIDTH, HEIGHT, BLOCK_SIZE, agent_type
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

'''Implements the simulation model'''

# Import necessary libraries and modules
import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wasp nest building process")

# Initialize grid with intial cell properties
cell_properties = {}
for x in range(0, WIDTH, BLOCK_SIZE):
    for y in range(0, HEIGHT, BLOCK_SIZE):
        rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(SCREEN, WHITE, rect, 1)
        cell_properties[(x, y)] = random.choices([0, 1, 2], [0.97, 0.02, 0.01])[0]

# Set the ruleset
ruleset = rulesets.rulesets[agent_type]

# Initialize agents
agents = [Agent(random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE), BLOCK_SIZE / 2, ruleset, cell_properties) for _ in range(10)]

# Model run
running = True
clock = pygame.time.Clock()
while running:
    # In case of quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # 1. Clear screen
    SCREEN.fill(BLACK)
    # 2. Update grid - cell properties and agents
    for x in range(0, WIDTH, BLOCK_SIZE):
        for y in range(0, HEIGHT, BLOCK_SIZE):
            colors = [WHITE, BLUE, GREEN]
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, colors[cell_properties[(x, y)]], rect, 0)
    for agent in agents:
        agent.step()
        agent.draw(SCREEN)
    # 3. Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
