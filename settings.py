import pygame
import random
import numpy

# initialize
pygame.init()

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SAND = (139, 69, 19)
BRICK = (255, 0, 0)
SHEEP = (124, 252, 0)
WOOD = (0, 100, 0)
WHEAT = (255, 215, 0)
ORE = (190, 190, 190)
SEA = (55, 155, 235)
TAN = (247,220,180)

# game settings
WIDTH = 800
HEIGHT = 800
FPS = 16
PALETTE = numpy.zeros((256,3))
FADE_STEP = numpy.zeros((256,3))
TITLE = "Catan Map Generator"
BGCOLOR = SEA

# Useful dicts
COLORS = {'sand' : SAND, 'ore' : ORE, 'brick' : BRICK, 'wood' : WOOD, 'sheep' : SHEEP, 'wheat' : WHEAT}
PDICT = {2 : 1, 3 : 2, 4 : 3, 5 : 4, 6 : 5, 8 : 5, 9 : 4, 10 : 3, 11 : 2, 12 : 1}

# Images
COVER = 'assets/img/cover.gif'

# Fonts
FONT = 'assets/fonts/Minion Pro Regular.ttf'

# Text
SMALL_TEXT = pygame.font.Font(FONT, 12)
MED_TEXT = pygame.font.Font(FONT, 24)
LARGE_TEXT = pygame.font.Font(FONT, 28)
TITLE_TEXT = pygame.font.Font(FONT, 48)

# Types
TYPES = ['sand', 'ore', 'brick', 'wood', 'sheep', 'wheat']

""" 3-4 PLAYER CATAN SETTINGS """
# Probs
PROBS = [0,2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]

# Tiles
TILES = ['sand', 'ore', 'ore', 'ore', 'brick', 'brick', 'brick', 'wood', 'wood', 'wood', 'wood', 'sheep', 'sheep', 'sheep', 'sheep', 'wheat', 'wheat', 'wheat', 'wheat']

# Coords of hexes
HEXCOORDS = [(0,0), (0,-1), (0,-2), (0,1), (0,2), (0.75,0.5), (0.75,1.5), (0.75,-0.5), (0.75,-1.5), (1.5,0), (1.5,-1), (1.5,1), (-0.75,0.5), (-0.75, 1.5), (-0.75, -0.5), (-0.75, -1.5), (-1.5,0), (-1.5,1), (-1.5,-1)]
random.shuffle(HEXCOORDS)

""" 5-6 PLAYER CATAN SETTINGS """
# Probs
EXT_PROBS = [0,0,2,2,3,3,3,4,4,4,5,5,5,6,6,6,8,8,8,9,9,9,10,10,10,11,11,11,12,12]

# Tiles
EXT_TILES = ['sand', 'sand', 'ore', 'ore', 'ore', 'ore', 'ore', 'brick', 'brick', 'brick','brick', 'brick', 'wood', 'wood', 'wood', 'wood', 'wood', 'wood', 'sheep', 'sheep', 'sheep', 'sheep', 'sheep', 'sheep', 'wheat', 'wheat', 'wheat', 'wheat', 'wheat', 'wheat']

# Coords of hexes
EXT_HEXCOORDS = [(0, -0.5), (0, 0.5), (0, -1.5), (0, 1.5), (0, -2.5), (0, 2.5), (0.75, 0), (0.75, -1), (0.75, 1), (0.75, -2), (0.75, 2), (1.5, -0.5), (1.5, 0.5), (1.5, -1.5), (1.5, 1.5), (2.25, 0), (2.25, -1), (2.25, 1), (-0.75, 0), (-0.75, -1), (-0.75, 1), (-0.75, -2), (-0.75, 2), (-1.5, -0.5), (-1.5, 0.5), (-1.5, -1.5), (-1.5, 1.5), (-2.25, 0), (-2.25, -1), (-2.25, 1)]
random.shuffle(EXT_HEXCOORDS)
