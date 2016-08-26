#!/usr/bin/env python

# ---------------------- IMPORTS ---------------------
# Python libs
from pygame import Surface, font
# Own libs
from constants6 import COLORS, PAUSE_SURFACE_ALPHA, ANTIALIASING, ROOT
''' This class will display our status and let us check, select and
    use items, save our progress, checking our tasks and more things
    I haven't thought yet. It exist a minimal chance of including this
    class on the Level file, so beware of it if you dare to contribute
    to this proyect development!'''


# General class
class SaveGame(object):
    # Globals
    root = ROOT

    # ---------- Constructor ----------------------
    def __init__(self, screen, scr_size, player, debug=False):
        # -- Attributes -----------------------
        self.debug = debug                          # Flag for debugging into the game
        self.screen = screen                        # A reference for the main screen
        self.scr_size = scr_size                    # The screen size
        self.player = player                        # A reference to the player and his statistics
        # Setting a plane, transparent background
        self.background = Surface([self.scr_size[0], self.scr_size[1]/4])
        self.background.fill(COLORS['BLACK'])
        # self.background.set_alpha(PAUSE_SURFACE_ALPHA)
        # Setting the text font for the save menu
        self.font = font.SysFont('Calibri', 25, True, False)
        # Save interface text (will include images on next versions)
        self.saveText = []
        self.saveText.append(self.font.render("Looking at this glittering spot fills you with det... "
                                              , ANTIALIASING, COLORS['WHITE']))
        self.saveText.append(self.font.render("oh, wait, we don't want being accused of plagiarism!"
                                              , ANTIALIASING, COLORS['WHITE']))
        self.saveText.append(self.font.render("In next versions, you'll be able to save your "
                                              + "game. Sorry! ", ANTIALIASING, COLORS['WHITE']))
        # Debug
        if self.debug:
            pass

    # ---------- Methods --------------------------
    def update(self):
        pass

    def display(self):
        self.screen.blit(self.background, [0, 0])
        self.screen.blit(self.saveText[0], [10, 10])
        self.screen.blit(self.saveText[1], [10, 35])
        self.screen.blit(self.saveText[2], [10, 60])
        if self.debug:
            pass
