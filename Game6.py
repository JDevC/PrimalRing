#!/usr/bin/env python

# ---------------------- IMPORTS ---------------------
# Python libs
import pygame
# Own libs
from Level6 import Level1, Level2
import PauseScreen
import SaveGame
from SaveGame import load_file
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
        self.pause = None
        self.pauseFlag = False                                          # Well, this is obvious
        # SAVE GAME elements
        self.save = None
        self.saveFlag = False                                           # Well, this is obvious
        # Levels
        saved_state = load_file()                                       # We try to load a game file
        print(saved_state)
        # This holds the level in which we are at first
        if saved_state is not None:
            self.levels = {"Doom Valley": Level1(screen, scr_size, DEBUG, saved_state),
                           "The RING": Level2(screen, scr_size, DEBUG, saved_state)}
            self.level = self.levels[saved_state['Level']]
        else:
            self.levels = {"Doom Valley": Level1(screen, scr_size, DEBUG),
                           "The RING": Level2(screen, scr_size, DEBUG)}
            self.level = self.levels["Doom Valley"]

    # ---------- Methods ----------------------
    # This function manages all events in game
    def event_handler(self):
        # Pause screen
        if self.pauseFlag:
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
                    elif event.key == pygame.K_ESCAPE:
                        return True

        # Save screen
        elif self.saveFlag:
            for event in pygame.event.get():                            # User did something
                if event.type == pygame.QUIT:                           # If user clicked close
                    return True                                         # We are done so we exit this loop
                # Incoming functionality on next versions!
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:                         # 'TAB' key
                        # We clean all flags and the save screen object
                        self.saveFlag = False
                        self.level.player.saveFlag = False
                        self.save = ""
                    elif event.key == pygame.K_UP:
                        pass
                    elif event.key == pygame.K_DOWN:
                        pass
                    elif event.key == pygame.K_s:                       # 's' key
                        # This saves your game!
                        # (Pfffiuuuu... what a relief)
                        self.save.save_file()
                        # Game saved
                        # self.save.load_file()
                        self.saveFlag = False
                        self.level.player.saveFlag = False
                        self.save = ""
                        pass
                    elif event.key == pygame.K_n:                       # 'n' key
                        # This avoids your game for being saved!
                        # You have a confident will, don't you?
                        self.saveFlag = False
                        self.level.player.saveFlag = False
                        self.save = ""

        else:
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
                    if event.key == pygame.K_TAB:                         # 'TAB' key
                        if self.level.player.saveFlag:
                            self.saveFlag = True
                            self.save = SaveGame.SaveGame(self.screen, self.scr_size, self.level)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.level.player.stop_x()
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        if self.level.player.plainLevel:
                            self.level.player.stop_y()

        return False

    # This function is given to refresh all objects and check collisions
    def run_logic(self):
        # Checks if the player still lives on
        if not self.gameOver:
            if self.pauseFlag:
                pass
            elif self.saveFlag:
                pass
            else:
                # Updates all sprites and checks if the player has made a level change
                reached = self.level.update()
                if reached:
                    # It swaps into another level.
                    # This point needs a revision: our game map should consist on a central level from where we can
                    # travel into the others, but at least it's a beginning
                    # self.gameOver = True
                    self.level = self.levels["The RING"]

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
            elif self.saveFlag:
                self.save.display()
        # --- This is 'update' for pygame library
        pygame.display.flip()
