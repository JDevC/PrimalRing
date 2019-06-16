#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
from ._Screen import _Screen
from constants import COLORS, SURFACE_MID_ALPHA, ANTIALIASING


class PauseScreen(_Screen):
    def __init__(self, screen, scr_size, sound_manager, player, debug: bool = False):
        """ This class will display our status and let us check, select and use items, save our progress,
        checking our tasks and more things I haven't thought yet. There's a minimal chance of including this
        class on the Level file, so beware of it if you dare to contribute to this project development!

        :param screen: A reference for the main screen
        :param scr_size: The screen size (Default: 600 * 800)
        :param sound_manager:
        :param player: A reference to the player and his statistics
        :param debug: Flag for debugging into the game """
        super().__init__(screen, scr_size, sound_manager, debug)
        self.soundMan.pause_music()
        self.player = player
        # Flags
        self.quit_all = False
        self.resume = False
        # We make our background transparent
        self.background.set_alpha(SURFACE_MID_ALPHA)
        # Cursor elements
        self.cursorSurface = pygame.Surface((170, 25))     # Pause Screen' highlight cursor
        self.cursorSurface.fill(COLORS['GREEN'])
        self.cursorSurface.set_alpha(128)
        self.cursor = self.cursorSurface.get_rect()
        self.cursor.x = self.scrSize[0] * 0.6
        self.cursor.y = self.scrSize[1] * 0.3
        # Setting the text font for the pause menu
        self.font = pygame.font.SysFont('Calibri', 25, True, False)
        # Pause interface text (will include images on next versions)
        self.pauseText = self._init_pause_text()
        self.menuList = self._init_menu_list()
        self.currentMenu = 0

        for x in self.menuList:
            self.pauseText.append(self.font.render(x['Name'], ANTIALIASING, COLORS['WHITE']))

        # Debug
        if self.debug:
            pass

    # --------------- MAIN FLOW ---------------------
    def event_handler(self):
        for event in pygame.event.get():                    # User did something
            if event.type == pygame.QUIT:                   # If user clicked close
                self.quit_all = True
                return True                                 # We are done so we exit this loop

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self._go_up()
                elif event.key == pygame.K_DOWN:
                    self._go_down()
                elif event.key == pygame.K_p:
                    # We resume the music streaming
                    self.soundMan.pause_music(False)
                    self.resume = True
                    return True
                elif event.key == pygame.K_RETURN:
                    self.soundMan.play_fx('Accept')
                    # Incoming functionality on next versions!
                    if self.menuList[self.currentMenu]['Name'] == _("- Inventory"):
                        print("Accessing inventory... soon!")
                    elif self.menuList[self.currentMenu]['Name'] == _("- Skills"):
                        print("Accessing skill board... soon!")
                    elif self.menuList[self.currentMenu]['Name'] == _("- Options"):
                        print("Accessing options... soon!")
                    elif self.menuList[self.currentMenu]['Name'] == _("- Quit"):
                        return True

        return False

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

    # --------------- METHODS ---------------------
    def _init_menu_list(self) -> []:
        return [{'Name': _("- Inventory"), 'Position': [self.scrSize[0] * 0.6, self.scrSize[1] * 0.3]},
                {'Name': _("- Skills"), 'Position': [self.scrSize[0] * 0.6, self.scrSize[1] * 0.4]},
                {'Name': _("- Options"), 'Position': [self.scrSize[0] * 0.6, self.scrSize[1] * 0.5]},
                {'Name': _("- Quit"), 'Position': [self.scrSize[0] * 0.6, self.scrSize[1] * 0.6]}]

    def _init_pause_text(self) -> []:
        return [self.font.render(_("PAUSE"), ANTIALIASING, COLORS['WHITE']),
                self.font.render(_("Life: {0}/{1}").format(self.player.life, self.player.maxLife),
                                 ANTIALIASING, COLORS['WHITE']),
                self.font.render(_("Energy: {0}/{1}").format(self.player.energy, self.player.maxEnergy),
                                 ANTIALIASING, COLORS['WHITE']),
                self.font.render(_("Coins: {0}/{1}").format(self.player.coins, self.player.maxWallet),
                                 ANTIALIASING, COLORS['WHITE'])]

    def _go_down(self) -> None:
        """ Moves the pause screen cursor to the immediate inferior position """
        self.soundMan.play_fx('Select')
        if self.currentMenu == len(self.menuList) - 1:
            self.currentMenu = 0
        else:
            self.currentMenu += 1

    def _go_up(self) -> None:
        """ Moves the pause screen cursor to the immediate superior position """
        self.soundMan.play_fx('Select')
        if self.currentMenu == 0:
            self.currentMenu = len(self.menuList) - 1
        else:
            self.currentMenu -= 1

