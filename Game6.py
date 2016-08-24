#!/usr/bin/env python

# ---------------------- IMPORTS ---------------------
# Python libs
import pygame
# import random
# import sys
# from os import path
# Own libs
from Level6 import Level1, Level2
from constants6 import BLACK, WHITE, ANTIALIASING, DEBUG  # ROOT
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
        # self.gOverText = self.font.render("GAME OVER", True, WHITE)
        self.gOverText = []
        self.gOverText.append(self.font.render("GAME OVER", ANTIALIASING, WHITE))
        self.gOverText.append(self.font.render("Want to try again?", ANTIALIASING, WHITE))
        self.gOverText.append(self.font.render("Yes / No", ANTIALIASING, WHITE))
        # Levels
        self.levels = []                                            # Contains all levels
        self.levels.append(Level1(screen, scr_size, DEBUG))         # We append all levels
        self.levels.append(Level2(screen, scr_size, DEBUG))
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
                    self.level.player.go_left()
                elif event.key == pygame.K_RIGHT:
                    self.level.player.go_right()
                elif event.key == pygame.K_UP:
                    if self.level.player.plainLevel:
                        self.level.player.go_up()
                    else:
                        self.level.player.jump()
                elif event.key == pygame.K_DOWN:
                    if self.level.player.plainLevel:
                        self.level.player.go_down()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.level.player.stop_x()
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if self.level.player.plainLevel:
                        self.level.player.stop_y()

        return False

    # This function is given to refresh all objects and check collisions
    def run_logic(self):
        # Checks if the player still lives on
        if not self.gameOver:
            # Updates all sprites and checks if the player has made a level change
            reached = self.level.update()
            if reached:
                # It swaps into another level.
                # This point needs a revision: our game map should consist on a central level from where we can
                # travel into the others, but at least it's a beginning
                # self.gameOver = True
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
            self.screen.blit(self.gOverText[0], [(self.scr_size[0]/2) - 45, self.scr_size[1]/2 - 50])
            self.screen.blit(self.gOverText[1], [(self.scr_size[0]/2) - 70, self.scr_size[1]/2 - 25])
            self.screen.blit(self.gOverText[2], [(self.scr_size[0]/2) - 50, self.scr_size[1]/2 + 50])
        else:
            # self.level1.display()
            self.level.display()
        # --- This is 'update' for pygame library
        pygame.display.flip()
