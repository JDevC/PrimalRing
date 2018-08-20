#!/usr/bin/env python3

# ---------------------- IMPORTS ---------------------
# Python libs
from pygame import Surface, font
# Own libs
from views.Title import _Screen
from constants import COLORS, SURFACE_MID_ALPHA, ANTIALIASING


class PauseScreen(_Screen):
    def __init__(self, screen, scr_size, sound_manager, player, debug=False):
        """ This class will display our status and let us check, select and use items, save our progress,
        checking our tasks and more things I haven't thought yet. There's a minimal chance of including this
        class on the Level file, so beware of it if you dare to contribute to this project development!

        :param screen: A reference for the main screen
        :param scr_size: The screen size (Default: 600 * 800)
        :param sound_manager:
        :param player: A reference to the player and his statistics
        :param debug: Flag for debugging into the game """
        super().__init__(screen, scr_size, sound_manager, debug)
        self.player = player
        # We make our background transparent
        self.background.set_alpha(SURFACE_MID_ALPHA)
        # Cursor elements
        self.cursorSurface = Surface((170, 25))     # Pause Screen' highlight cursor
        self.cursorSurface.fill(COLORS['GREEN'])
        self.cursorSurface.set_alpha(128)
        # Menu
        self.menuList = [{'Name': _("- Inventory"), 'Position': [self.scrSize[0] * 0.6, self.scrSize[1] * 0.3]},
                         {'Name': _("- Skills"), 'Position': [self.scrSize[0] * 0.6, self.scrSize[1] * 0.4]},
                         {'Name': _("- Options"), 'Position': [self.scrSize[0] * 0.6, self.scrSize[1] * 0.5]},
                         {'Name': _("- Quit"), 'Position': [self.scrSize[0] * 0.6, self.scrSize[1] * 0.6]}]
        self.currentMenu = 0
        # Setting the text font for the pause menu
        self.font = font.SysFont('Calibri', 25, True, False)
        # Pause interface text (will include images on next versions)
        self.pauseText = [
            self.font.render(_("PAUSE"), ANTIALIASING, COLORS['WHITE']),
            self.font.render(_("Life: {0}/{1}").format(self.player.life, self.player.maxLife),
                             ANTIALIASING, COLORS['WHITE']),
            self.font.render(_("Energy: {0}/{1}").format(self.player.energy, self.player.maxEnergy),
                             ANTIALIASING, COLORS['WHITE']),
            self.font.render(_("Coins: {0}/{1}").format(self.player.coins, self.player.maxWallet),
                             ANTIALIASING, COLORS['WHITE'])]

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
        """ Moves the pause screen cursor to the immediate inferior position """
        self.soundMan.play_fx('Select')
        if self.currentMenu == len(self.menuList) - 1:
            self.currentMenu = 0
        else:
            self.currentMenu += 1

    def go_up(self):
        """ Moves the pause screen cursor to the immediate superior position """
        self.soundMan.play_fx('Select')
        if self.currentMenu == 0:
            self.currentMenu = len(self.menuList) - 1
        else:
            self.currentMenu -= 1

