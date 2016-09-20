#!/usr/bin/env python

# ---------------------- IMPORTS ---------------------
# Python libs
from pygame import Surface, font, mixer
# Own libs
from constants6 import COLORS, SURFACE_MID_ALPHA, ANTIALIASING, ROOT
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
        self.scrSize = scr_size                     # The screen size (Default: 600 * 800)
        # Cursor elements
        self.cursorSurface = Surface((170, 25))     # Pause Screen' highlight cursor
        self.cursorSurface.fill(COLORS['GREEN'])
        self.cursorSurface.set_alpha(128)
        self.menuList = [{'Name': '- Inventory',
                          'Position': [self.scrSize[0] * 0.6, self.scrSize[1] * 0.3]},
                         {'Name': '- Skills',
                          'Position': [self.scrSize[0] * 0.6, self.scrSize[1] * 0.4]},
                         {'Name': '- Options',
                          'Position': [self.scrSize[0] * 0.6, self.scrSize[1] * 0.5]},
                         {'Name': '- Quit',
                          'Position': [self.scrSize[0] * 0.6, self.scrSize[1] * 0.6]}]
        # Sounds
        self.selectSound = mixer.Sound(ROOT + '/sounds/select.wav')
        self.currentMenu = 0
        # Player
        self.player = player                        # A reference to the player and his statistics
        # Setting a plane, transparent background
        self.background = Surface(self.scrSize)
        self.background.fill(COLORS['BLACK'])
        self.background.set_alpha(SURFACE_MID_ALPHA)
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
        for x in self.menuList:
            self.pauseText.append(self.font.render(x['Name'], ANTIALIASING, COLORS['WHITE']))

        # Setting initial cursor's position
        self.cursor = self.cursorSurface.get_rect()
        self.cursor.x = self.scrSize[0] * 0.6
        self.cursor.y = self.scrSize[1] * 0.3

        # Debug
        if self.debug:
            pass

    # ---------- Methods --------------------------
    def update(self):
        self.cursor.x = self.menuList[self.currentMenu]['Position'][0]
        self.cursor.y = self.menuList[self.currentMenu]['Position'][1]

    def display(self):
        # Background attached to all the window surface
        self.screen.blit(self.background, [0, 0])
        # Cursor
        self.screen.blit(self.cursorSurface, [self.cursor.x, self.cursor.y])
        # Pause text
        self.screen.blit(self.pauseText[0], [self.scrSize[0] * 0.45, self.scrSize[1] * 0.1])
        self.screen.blit(self.pauseText[1], [self.scrSize[0] * 0.2, self.scrSize[1] * 0.3])
        self.screen.blit(self.pauseText[2], [self.scrSize[0] * 0.2, self.scrSize[1] * 0.4])
        self.screen.blit(self.pauseText[3], [self.scrSize[0] * 0.2, self.scrSize[1] * 0.5])
        for x in range(len(self.menuList)):
            self.screen.blit(self.pauseText[x+4], self.menuList[x]['Position'])
        # Debug
        if self.debug:
            pass

    def go_down(self):
        self.selectSound.play()
        if self.currentMenu == len(self.menuList) - 1:
            self.currentMenu = 0
        else:
            self.currentMenu += 1

    def go_up(self):
        self.selectSound.play()
        if self.currentMenu == 0:
            self.currentMenu = len(self.menuList) - 1
        else:
            self.currentMenu -= 1

