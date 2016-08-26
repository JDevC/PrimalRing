#!/usr/bin/env python

# ---------------------- IMPORTS ---------------------
# Python libs
import pygame
# import random
# import sys
# from os import path
# Own libs
from Level6 import Level1, Level2
import PauseScreen
from constants6 import COLORS, ANTIALIASING, DEBUG
''' This is the general manager game class. It has the
    main functions and attributes which rule above all
    the rest.'''


class Game(object):
    # ---------- Constructor ----------------------
    def __init__(self, screen, scr_size):
        # Main game attributes
        self.gameOver = False                                           # Endgame (also a truly brutal Megadeth album)
        self.screen = screen
        self.scr_size = scr_size
        self.font = pygame.font.SysFont('Calibri', 25, True, False)
        # GAME OVER text
        self.gOverText = []
        self.gOverText.append(self.font.render("GAME OVER", ANTIALIASING, COLORS['WHITE']))
        self.gOverText.append(self.font.render("Want to try again?", ANTIALIASING, COLORS['WHITE']))
        self.gOverText.append(self.font.render("Yes / No", ANTIALIASING, COLORS['WHITE']))
        # PAUSE elements
        self.pause = ""
        self.pauseFlag = False                                          # Well, this is obvious
        # Levels
        self.levels = []                                                # Contains all levels
        self.levels.append(Level1(screen, scr_size, DEBUG))             # We append all levels
        self.levels.append(Level2(screen, scr_size, DEBUG))
        self.currentLevel = 0
        self.level = self.levels[self.currentLevel]                     # This holds the level in which we are at first

    # ---------- Methods ----------------------
    # This function manages all events in game
    def event_handler(self):
        if not self.pauseFlag:
            for event in pygame.event.get():                            # User did something
                if event.type == pygame.QUIT:                           # If user clicked close
                    return True                                         # We are done so we exit this loop

                if event.type == pygame.KEYDOWN:
                    # Figure out if it was an arrow key. If it's so, adjust speed.
                    if event.key == pygame.K_LEFT:                      # <-
                        self.level.player.go_left()
                    if event.key == pygame.K_RIGHT:                     # ->
                        self.level.player.go_right()
                    if event.key == pygame.K_UP:
                        if self.level.player.plainLevel:
                            self.level.player.go_up()
                        else:
                            self.level.player.jump()
                    if event.key == pygame.K_DOWN:
                        if self.level.player.plainLevel:
                            self.level.player.go_down()
                    if event.key == pygame.K_p:                         # 'p' key
                        self.pauseFlag = True
                        self.pause = PauseScreen.PauseScreen(self.screen, self.scr_size, self.level.player)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.level.player.stop_x()
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        if self.level.player.plainLevel:
                            self.level.player.stop_y()

        else:
            for event in pygame.event.get():                            # User did something
                if event.type == pygame.QUIT:                           # If user clicked close
                    return True                                         # We are done so we exit this loop

                # Incoming functionality on next versions!
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pass
                    elif event.key == pygame.K_RIGHT:
                        pass
                    elif event.key == pygame.K_UP:
                        pass
                    elif event.key == pygame.K_DOWN:
                        pass
                    elif event.key == pygame.K_p:
                        self.pauseFlag = False                          # Exits the pause screen

        return False

    # This function is given to refresh all objects and check collisions
    def run_logic(self):
        # Checks if the player still lives on
        if not self.gameOver:
            if not self.pauseFlag:
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
            else:
                pass

    # This function displays all graphic resources and effects
    def display_frame(self):
        self.screen.fill(COLORS['BLACK'])
        # Checks if the player still lives on
        if self.gameOver:
            self.screen.blit(self.gOverText[0], [(self.scr_size[0]/2) - 45, self.scr_size[1]/2 - 50])
            self.screen.blit(self.gOverText[1], [(self.scr_size[0]/2) - 70, self.scr_size[1]/2 - 25])
            self.screen.blit(self.gOverText[2], [(self.scr_size[0]/2) - 50, self.scr_size[1]/2 + 50])
        else:
            self.level.display()
            # This implementation allows us to cover our game screen with the pause screen,
            # stopping all mechanics and events in game except those who are involved in the
            # pause screen logic flow, but also letting us to see a static impression of the
            # game behind the pause screen.
            if self.pauseFlag:
                self.pause.display()
        # --- This is 'update' for pygame library
        pygame.display.flip()
