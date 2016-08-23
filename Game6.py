#!/usr/bin/env python

# ---------------------- IMPORTS ---------------------
# Python libs
import pygame
# import random
# import sys
# from os import path
# Own libs
from Level6 import Level1, Level2
from constants6 import BLACK, WHITE  # ROOT
''' This is the general manager game class. It has the
    main functions and attributes which rule above all
    the rest.'''


class Game(object):
    # ---------- Constructor ----------------------
    def __init__(self, screen, scr_size):
        # Main game attributes
        self.gameOver = False                                       # Endgame (also a truly brutal Megadeth album)
        self.screen = screen
        self.scr_size = scr_size
        self.font = pygame.font.SysFont('Calibri', 25, True, False)
        self.gOverText = self.font.render("GAME OVER", True, WHITE)
        # Levels
        self.levels = []                                            # Contains all levels
        self.levels.append(Level1(screen, scr_size, True))          # We append all levels (True is for debug reasons)
        self.levels.append(Level2(screen, scr_size, True))
        self.level1 = Level1(screen, scr_size, True)                # asdf
        self.currentLevel = 0
        self.level = self.levels[self.currentLevel]                 # This contains the level in which we are at first

    # ---------- Methods ----------------------
    # This function manages all events in game
    def event_handler(self):
        for event in pygame.event.get():                            # User did something
            if event.type == pygame.QUIT:                           # If user clicked close
                return True                                         # Flag that we are done so we exit this loop
            elif event.type == pygame.KEYDOWN:
                # Figure out if it was an arrow key. If it's so, adjust speed.
                if event.key == pygame.K_LEFT:
                    # self.level1.player.go_left()
                    self.level.player.go_left()
                elif event.key == pygame.K_RIGHT:
                    # self.level1.player.go_right()
                    self.level.player.go_right()
                elif event.key == pygame.K_UP:
                    # if self.level1.player.plainLevel:
                    if self.level.player.plainLevel:
                        # self.level1.player.go_up()
                        self.level.player.go_up()
                    else:
                        # self.level1.player.jump()
                        self.level.player.jump()
                elif event.key == pygame.K_DOWN:
                    # if self.level1.player.plainLevel:
                    if self.level.player.plainLevel:
                        # self.level1.player.go_down()
                        self.level.player.go_down()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    # self.level1.player.stop_x()
                    self.level.player.stop_x()
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    # if self.level1.player.plainLevel:
                    if self.level.player.plainLevel:
                        # self.level1.player.stop_y()
                        self.level.player.stop_y()
        return False

    # This function is given to refresh all objects and check collisions
    def run_logic(self):
        # Checks if the player still lives on
        if not self.gameOver:
            # Updates all sprites
            # self.gameOver = self.level1.update()
            reached = self.level.update()
            if reached:
                if self.currentLevel < len(self.levels):
                    self.currentLevel += 1
                    self.level = self.levels[self.currentLevel]
                else:
                    self.gameOver = True

    # This function displays all graphic resources and effects
    def display_frame(self):
        self.screen.fill(BLACK)
        # Checks if the player still lives on
        if self.gameOver:
            # print "Perdiste!"
            self.screen.blit(self.gOverText, [(self.scr_size[0]/2) - 50, self.scr_size[1]/2])
        else:
            # self.level1.display()
            self.level.display()
        # --- This is 'update' for pygame library
        pygame.display.flip()
