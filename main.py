import sys
import pygame, pygame.image
import math
import random
from numpy import *
from pygame.surfarray import *
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT, K_SPACE, MOUSEBUTTONDOWN
from settings import *
from map import *
import collections
import string
from PIL import Image

# Game class
class Game:
    def __init__(self):
        # initialize the game
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 8)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.board = ''
        self.edition = ''
        self.click = False

    def new(self):
        # shuffle for every new board
        random.shuffle(PROBS)
        random.shuffle(TILES)
        random.shuffle(HEXCOORDS)
        random.shuffle(EXT_PROBS)
        random.shuffle(EXT_TILES)
        random.shuffle(EXT_HEXCOORDS)

    def run(self):
        # game loop
        self.running = True
        self.make_map()
        while self.running:
            self.events()

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()

    def events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
                if event.key == K_SPACE:
                    self.update()
            elif event.type == QUIT:
                self.quit()
            elif event.type == MOUSEBUTTONDOWN:
                self.click = True

    def update(self):
        # refresh the board
        self.new()
        self.run()

    def make_map(self):
        # background
        pygame.display.set_caption(TITLE)
        self.main_menu_setup()
        pygame.display.flip()
        # subtitle
        if self.board == 'random': sub_text = 'Completely random board generation'
        if self.board == 'fair': sub_text = 'Balanced board generation'
        sub = LARGE_TEXT.render(sub_text, True, BLACK)
        sub_rect = sub.get_rect(center=(WIDTH/2, HEIGHT*0.14))
        self.screen.blit(sub, sub_rect)
        # draw the map
        map = Map(self.board, self.edition, self.screen)
        for key, value in map.hexdict.items():
            print(key + " " + value[2])
        map.render()
        # events
        on_map = True
        pygame.display.flip()
        while on_map:
            click = False
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.quit()
                    if event.key == K_SPACE:
                        self.update()
                elif event.type == QUIT:
                    self.quit()
                elif event.type == MOUSEBUTTONDOWN:
                    click = True
            if self.button('Back', 100, 80, 100, 50, click): on_map = False
            pygame.display.flip()
        self.main_menu()

    def cover(self):
        resize = [512,512]
        time = 250
        self.screen.fill(BLACK)
        img = Image.open(COVER)
        pimg = pygame.image.load(COVER)
        self.screen.blit(pimg, (0,0))
        pygame.display.flip()
        pygame.time.delay(time)
        for i in range(1,32):
            frame = img.resize(tuple(resize))
            frame = frame.resize(img.size,Image.NEAREST)
            frame.save('assets/img/COVER{}.gif'.format(i))
            frame = pygame.image.load('assets/img/COVER{}.gif'.format(i))
            resize = [(x-16) for x in resize]
            time = int(time * 0.975)
            self.screen.blit(frame, (0,0))
            pygame.display.flip()
            pygame.time.delay(time)

        self.main_menu()

    def main_menu_setup(self):
        # setup main menu
        self.screen.fill(BGCOLOR)
        # Title
        tit = TITLE_TEXT.render(TITLE, True, BLACK)
        tit_rect = tit.get_rect(center=(WIDTH/2, HEIGHT/11))
        self.screen.blit(tit, tit_rect)
        # Subtitle
        sub = LARGE_TEXT.render('Created by Alexandra Thursland', True, BLACK)
        sub_rect = sub.get_rect(center=(WIDTH/2, HEIGHT*0.9))
        self.screen.blit(sub, sub_rect)

    def main_menu(self):
        global ticks
        self.main_menu_setup()
        base = False
        ext = False
        while True:
            click = False
            for event in pygame.event.get():
                if event.type == QUIT: self.quit()
                elif event.type == K_ESCAPE: self.quit()
                elif event.type == MOUSEBUTTONDOWN: click = True
            if self.button('Base', WIDTH/2, HEIGHT/2.5, 200, 50, click): base = True
            elif self.button('Extension', WIDTH/2, HEIGHT/2, 200, 50, click): ext = True
            elif self.button('Quit', WIDTH/2, HEIGHT/1.5, 200, 50, click): self.quit()
            if base: self.edition = 'base'
            if ext: self.edition = 'ext'
            if base or ext:
                while base or ext:
                    self.main_menu_2()
            pygame.display.flip()

    def main_menu_2(self):
        global ticks
        self.main_menu_setup()
        random = False
        fair = False
        while True:
            click = False
            for event in pygame.event.get():
                if event.type == QUIT: self.quit()
                elif event.type == K_ESCAPE: self.quit()
                elif event.type == MOUSEBUTTONDOWN: click = True
            if self.button('Random', WIDTH/2, HEIGHT/2.5, 200, 50, click): random = True
            elif self.button('Balanced', WIDTH/2, HEIGHT/2, 200, 50, click): fair = True
            elif self.button('Quit', WIDTH/2, HEIGHT/1.5, 200, 50, click): self.quit()
            if random: self.board = 'random'
            if fair: self.board = 'fair'
            if random or fair:
                while random or fair:
                    self.new()
                    self.run()
            pygame.display.flip()


    def button(self, text, x, y, w, h, click, inactive_color=ORE, active_color=WHITE):
        mouse = pygame.mouse.get_pos()
        return_value = False
        if x < mouse[0] < x + w and y < mouse[1] < y + h:  # if mouse is hovering the button
            pygame.draw.rect(self.screen, active_color, (x-0.5*w, y-0.5*h, w, h))
            pygame.draw.rect(self.screen, BLACK, (x-0.5*w, y-0.5*h, w, h), 2)
            if click and pygame.time.get_ticks() > 100: return_value = True
        else:
            pygame.draw.rect(self.screen, inactive_color, (x-0.5*w, y-0.5*h, w, h))
            pygame.draw.rect(self.screen, BLACK, (x-0.5*w, y-0.5*h, w, h), 2)

        text_surf = LARGE_TEXT.render(text, True, BLACK)
        text_rect = text_surf.get_rect(center=(x,y))
        self.screen.blit(text_surf, text_rect)
        return return_value

# create the game object
if __name__ == '__main__':
    # Initialization
    g = Game()
    g.main_menu()
