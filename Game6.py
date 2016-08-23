#!/usr/bin/env python

# ---------------------- IMPORTS ---------------------
# Python libs
import pygame
# import random
# import sys
# from os import path
# Own libs
from Level6 import Level1
from constants6 import BLACK, WHITE  # ROOT

''' This is the general manager game class. It has the
    main functions and attributes which rule above all
    the rest.'''


class Game(object):
    # ---------- Constructor ----------------------
    def __init__(self, screen, scr_size):
        # Endgame (also a truly brutal Megadeth album)
        self.gameOver = False
        self.screen = screen
        self.scr_size = scr_size
        self.font = pygame.font.SysFont('Calibri', 25, True, False)
        self.gOverText = self.font.render("GAME OVER", True, WHITE)
        # self.level1 = Level1(screen, scr_size, ROOT, True)  # debug = True
        self.level1 = Level1(screen, scr_size, True)  # debug = True

    # ---------- Methods ----------------------
    # This function manages all events in game
    def event_handler(self):
        for event in pygame.event.get():                # User did something
            if event.type == pygame.QUIT:               # If user clicked close
                return True                             # Flag that we are done so we exit this loop
            elif event.type == pygame.KEYDOWN:
                # Figure out if it was an arrow key. If it's so, adjust speed.
                if event.key == pygame.K_LEFT:
                    self.level1.hero.go_left()
                elif event.key == pygame.K_RIGHT:
                    self.level1.hero.go_right()
                elif event.key == pygame.K_UP:
                    self.level1.hero.jump()
                # elif event.key == pygame.K_DOWN:
                # self.level1.hero.velY = 3
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.level1.hero.stop_x()
                # elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                # self.hero.stopY()
        return False

    # This function is given to refresh all objects and check collisions
    def run_logic(self):
        # Checks if the player still lives on
        if not self.gameOver:
            # Updates all sprites
            self.level1.update()

            if len(self.level1.temporary) == 0:
                self.gameOver = True

    # This function displays all graphic resources and effects
    def display_frame(self):
        self.screen.fill(BLACK)
        # Checks if the player still lives on
        if self.gameOver:
            # print "Perdiste!"
            self.screen.blit(self.gOverText, [(self.scr_size[0]/2) - 50, self.scr_size[1]/2])
        else:
            self.level1.display()
        # --- This is 'update' for pygame library
        pygame.display.flip()
