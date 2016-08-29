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
class PauseScreen(object):
    # Globals
    root = ROOT

    # ---------- Constructor ----------------------
    def __init__(self, screen, scr_size, player, debug=False):
        # -- Attributes -----------------------
        self.debug = debug                          # Flag for debugging into the game
        self.screen = screen                        # A reference for the main screen
        self.scr_size = scr_size                    # The screen size (Default: 600 * 800)
        self.player = player                        # A reference to the player and his statistics
        # Setting a plane, transparent background
        self.background = Surface(scr_size)
        self.background.fill(COLORS['BLACK'])
        self.background.set_alpha(PAUSE_SURFACE_ALPHA)
        # Setting the text font for the pause menu
        self.font = font.SysFont('Calibri', 25, True, False)
        # Pause interface text (will include images on next versions)
        self.pauseText = []
        self.pauseText.append(self.font.render("PAUSE", ANTIALIASING, COLORS['WHITE']))
        self.pauseText.append(self.font.render("Life: " + str(self.player.life) + "/"
                                               + str(self.player.maxLife), ANTIALIASING, COLORS['WHITE']))
        self.pauseText.append(self.font.render("Energy: " + str(self.player.energy) + "/"
                                               + str(self.player.maxEnergy), ANTIALIASING, COLORS['WHITE']))
        self.pauseText.append(self.font.render("Coins: " + str(self.player.coins) + "/"
                                               + str(self.player.maxWallet), ANTIALIASING, COLORS['WHITE']))
        self.pauseText.append(self.font.render("- Inventory", ANTIALIASING, COLORS['WHITE']))
        self.pauseText.append(self.font.render("- Skills", ANTIALIASING, COLORS['WHITE']))
        self.pauseText.append(self.font.render("- Options", ANTIALIASING, COLORS['WHITE']))
        self.pauseText.append(self.font.render("- Quit", ANTIALIASING, COLORS['WHITE']))

        # Debug
        if self.debug:
            pass

    # ---------- Methods --------------------------
    def update(self):
        pass

    def display(self):
        # Background attached to all the window surface
        self.screen.blit(self.background, [0, 0])
        self.screen.blit(self.pauseText[0], [self.scr_size[0] * 0.45, self.scr_size[1] * 0.1])
        self.screen.blit(self.pauseText[1], [self.scr_size[0] * 0.2, self.scr_size[1] * 0.3])
        self.screen.blit(self.pauseText[2], [self.scr_size[0] * 0.2, self.scr_size[1] * 0.4])
        self.screen.blit(self.pauseText[3], [self.scr_size[0] * 0.2, self.scr_size[1] * 0.5])
        self.screen.blit(self.pauseText[4], [self.scr_size[0] * 0.6, self.scr_size[1] * 0.3])
        self.screen.blit(self.pauseText[5], [self.scr_size[0] * 0.6, self.scr_size[1] * 0.4])
        self.screen.blit(self.pauseText[6], [self.scr_size[0] * 0.6, self.scr_size[1] * 0.5])
        self.screen.blit(self.pauseText[7], [self.scr_size[0] * 0.6, self.scr_size[1] * 0.6])
        if self.debug:
            pass
