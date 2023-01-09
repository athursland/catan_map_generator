import sys
import pygame, pygame.image
import math
import random
from pygame.surfarray import *
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT, K_SPACE, MOUSEBUTTONDOWN
from settings import *
from main import *
import collections
import string

""" Hex class """
# Hexagon class
class Hex:
    def __init__(self, screen, hexcoords, type, prob):
        self.screen = screen
        self.type = type
        self.prob = prob
        self.row = hexcoords[0]
        self.col = hexcoords[1]
        self.coords = self.vertices()

    def vertices(self):
        x = (WIDTH)/2
        y = (HEIGHT)/2
        p1 = (x-50+100*self.col, y-25+100*self.row)
        p2 = (x+100*self.col, y-50+100*self.row)
        p3 = (x+50+100*self.col, y-25+100*self.row)
        p4 = (x+50+100*self.col, y+25+100*self.row)
        p5 = (x+100*self.col, y+50+100*self.row)
        p6 = (x-50+100*self.col, y+25+100*self.row)
        return (p1, p2, p3, p4, p5, p6)

    def draw(self):
        x = (WIDTH)/2+100*self.col
        y = (HEIGHT)/2+100*self.row
        pygame.draw.polygon(self.screen, COLORS.get(self.type), self.coords)
        pygame.draw.lines(self.screen, BLACK, True, self.coords, 2)
        pygame.draw.circle(self.screen, TAN, (x,y), 25)
        pygame.draw.circle(self.screen, BLACK, (x,y), 25, 2)
        font = MED_TEXT
        if self.prob in [6,8]:
            label = font.render(str(self.prob), True, BRICK)
        else:
            label = font.render(str(self.prob), True, BLACK)
        label_rect = label.get_rect(center=(x,y))
        self.screen.blit(label, label_rect)
        font = SMALL_TEXT
        if self.prob != 0:
            chits = ["*" for i in range(PDICT.get(self.prob))]
            chit = font.render(''.join(chits), True, BLACK)
            chit_rect = chit.get_rect(center=(x,y+16))
            self.screen.blit(chit, chit_rect)


""" Map class """
class Map:
    """ Initialize the map """
    def __init__(self, board, edition, screen):
        # base vars
        self.board = board
        self.edition = edition
        self.screen = screen
        self.hexlist = []
        self.hexdict = {}
        self.chitdict = {'ore' : 0, 'brick' : 0, 'wood' : 0, 'sheep' : 0, 'wheat' : 0}
        if self.edition == 'base':
            self.tiles = TILES.copy()
            self.probs = PROBS.copy()
            self.coords = HEXCOORDS.copy()
        elif self.edition == 'ext':
            self.tiles = EXT_TILES.copy()
            self.probs = EXT_PROBS.copy()
            self.coords = EXT_HEXCOORDS.copy()

    """ Random generator """
    def random(self):
        # a completely random board
        num = len(self.tiles)
        letlist = list(map(chr, range(97,97+num)))
        for let in letlist:
            hc = self.coords.pop()
            t = None
            p = None
            self.hexdict[let] = (hc, t, p, [])
        for key, value in self.hexdict.items():
            if self.edition == 'ext' and (key == 'a' or key == 'b'):
                self.probs.remove(0)
                self.tiles.remove('sand')
                self.hexdict[key] = (value[0], 'sand', 0, value[3])
                hex = Hex(self.screen, value[0], 'sand', 0)
            elif self.edition == 'base' and key == 'a':
                self.probs.remove(0)
                self.tiles.remove('sand')
                self.hexdict[key] = (value[0], 'sand', 0, value[3])
                hex = Hex(self.screen, value[0], 'sand', 0)
            else:
                tile = self.tiles.pop()
                prob = self.probs.pop()
                hex = Hex(self.screen, value[0], tile, prob)
                self.hexdict[key] = (value[0], tile, 0, value[3])
            hex.draw()

    """ Fair generator """
    def fair(self):
        # fair board
        self.gen_fair_tup()
        for hex in self.hexdict.keys():
            vals = self.hexdict.get(hex)
            print(hex + " " + str(vals))
            self.draw_hex(self.screen, vals[0], vals[1], vals[2])

    """  Fair generator methods """
    def gen_fair_tup(self):
        # generate the random hex tuple list
        num = len(self.tiles)
        letlist = list(map(chr, range(97,97+num)))
        # for each letter initialize dictionary
        for let in letlist:
            hc = self.coords.pop()
            t = None
            p = None
            self.hexdict[let] = (hc, t, p, [])
        # gen neighbors
        self.gen_neighbors()
        self.gen_desert()
        self.gen_types()
        self.gen_nums()

    def gen_neighbors(self):
        # generate neighbors - originally in gen_hex_tup() method, might switch back
        for key, value in self.hexdict.items():
            # ref coord
            ref = value[0]
            # vt neighbors (let)
            vtnc = [x for x in self.hexdict.keys() if (self.hexdict.get(x)[0][0] == ref[0] - 0.75 or self.hexdict.get(x)[0][0] == ref[0] + 0.75)]
            vtnc = [x for x in vtnc if (self.hexdict.get(x)[0][1] == ref[1] - 0.5 or self.hexdict.get(x)[0][1] == ref[1] + 0.5)]
            # hz neighbors (let)
            hznc = [x for x in self.hexdict.keys() if (self.hexdict.get(x)[0][1] == ref[1] - 1 or self.hexdict.get(x)[0][1] == ref[1] + 1)]
            hznc = [x for x in hznc if (self.hexdict.get(x)[0][0] == ref[0])]
            # add neighbors to dict
            self.hexdict[key] = (ref, value[1], value[2], vtnc + hznc)

    def gen_desert(self):
        for key, value in self.hexdict.items():
            if self.edition == 'base':
                if key == 'a':
                    self.probs.remove(0)
                    self.tiles.remove('sand')
                    self.hexdict[key] = (value[0], 'sand', 0, value[3])
            if self.edition == 'ext':
                if key == 'a' or key == 'b':
                    self.probs.remove(0)
                    self.tiles.remove('sand')
                    self.hexdict[key] = (value[0], 'sand', 0, value[3])

    def gen_types(self):
        # generate types based on neighbors
        for key, value in self.hexdict.items():
            if self.edition == 'base':
                if key != 'a':
                    ntypes = [x[1][1] for x in self.hexdict.items() if x[0] in value[3]]
                    # list of available probs
                    ptypes = [x for x in self.tiles if x not in ntypes]
                    random.shuffle(ptypes)
                    # select random prob
                    if len(ptypes) == 0:
                        tile = self.tiles[0]
                    else:
                        tile = ptypes.pop()
                    self.tiles.remove(tile)
                    self.hexdict[key] = (value[0], tile, value[2], value[3])
            if self.edition == 'ext':
                if key != 'a' and key != 'b':
                    ntypes = [x[1][1] for x in self.hexdict.items() if x[0] in value[3]]
                    # list of available probs
                    ptypes = [x for x in self.tiles if x not in ntypes]
                    random.shuffle(ptypes)
                    # select random prob
                    if len(ptypes) == 0:
                        tile = self.cluster_buster(key, ntypes)
                    else:
                        tile = ptypes.pop()
                    self.tiles.remove(tile)
                    self.hexdict[key] = (value[0], tile, value[2], value[3])

    def cluster_buster(self, hex, ntypes):
        # check for neighbor type clusters and return non-cluster type
        pcs = [x for x in list(set(ntypes)) if (ntypes.count(x) > 1) and x != None]
        pts = [x for x in ntypes if x not in pcs and x in self.tiles and x != 'sand']
        if len(pts) == 0:
            return self.tiles[0]
        else:
            random.shuffle(pts)
            return pts[0]

    def gen_nums(self):
        # assign probs to tiles
        for key, value in self.hexdict.items():
            if self.edition == 'base':
                if key != 'a':
                    # set up neighbor red check
                    nprobs = [x[1][2] for x in self.hexdict.items() if x[0] in value[3]]
                    if 6 in nprobs: nprobs.append(8)
                    if 8 in nprobs: nprobs.append(6)
                    # check chit dist
                    chits = self.chit_dist(value[1])
                    pprobs = [x for x in self.probs if x not in nprobs and PDICT.get(x) < chits]
                    random.shuffle(pprobs)
                    if len(pprobs) == 0:
                        prob = self.probs[0]
                    else:
                        prob = pprobs.pop()
                    self.probs.remove(prob)
                    self.hexdict[key] = (value[0], value[1], prob, value[3])
                    self.chitdict[value[1]] += PDICT.get(prob)
            if self.edition == 'ext':
                if key != 'a' and key != 'b':
                    # set up neighbor red check
                    nprobs = [x[1][2] for x in self.hexdict.items() if x[0] in value[3]]
                    if 6 in nprobs: nprobs.append(8)
                    if 8 in nprobs: nprobs.append(6)
                    pprobs = [x for x in self.probs if x not in nprobs]
                    random.shuffle(pprobs)
                    if len(pprobs) == 0:
                        prob = self.probs[0]
                    else:
                        prob = pprobs.pop()
                    self.probs.remove(prob)
                    self.hexdict[key] = (value[0], value[1], prob, value[3])

    def chit_dist(self, type):
        # ensure evenly distributed chits
        if self.edition == 'base':
            if type == 'ore' or type == 'brick': return 10 - self.chitdict[type]
            else: return 13 - self.chitdict[type]
        if self.edition == 'ext':
            if type == 'ore' or type == 'brick': return 10 - self.chitdict[type]
            else: return 13 - self.chitdict[type]

    def draw_hex(self, screen, coord, tile, prob):
        hex = Hex(screen, coord, tile, prob)
        hex.draw()

    """ Render method """
    def render(self):
        if self.board == 'random':
            board = self.random()
        if self.board == 'fair':
            board = self.fair()
        pygame.display.flip()
