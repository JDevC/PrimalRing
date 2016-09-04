#!/usr/bin/env python

# ---------------------- IMPORTS ---------------------
# Python libs
import pygame
# Own libs
from constants6 import COLORS, SURFACE_MID_ALPHA, ANTIALIASING, ROOT
from SaveGame import load_files
''' This class will display the title screen, showing a background animation
    and playing the main theme while we navigate though the main menu. That's
    the initial idea, of course. '''


# General class
class TitleScreen(object):
    # Globals
    root = ROOT

    # ---------- Constructor ----------------------
    def __init__(self, screen, scr_size, debug=False):
        # -- Attributes -----------------------
        self.debug = debug                                  # Flag for debugging into the game
        self.screen = screen                                # A reference for the main screen
        self.scrSize = scr_size                             # The screen size (Default: 600 * 800)
        self.savedFiles = load_files()                      # A list of saved games (or None)
        # New Game/Load Game fading surface
        self.cover = pygame.Surface(self.scrSize)
        self.cover.fill(COLORS['BLACK'])
        self.cover.set_alpha(0)
        self.opacity = 0
        self.initGame = False
        # Cursor elements
        self.cursorSurface = pygame.Surface((170, 25))      # Pause Screen' highlight cursor
        self.cursorSurface.fill(COLORS['GREEN'])
        self.cursorSurface.set_alpha(SURFACE_MID_ALPHA)
        self.menuList = [{'Name': 'New Game',
                          'Position': [self.scrSize[0] * 0.6, self.scrSize[1] * 0.5]},
                         {'Name': 'Load Game',
                          'Position': [self.scrSize[0] * 0.6, self.scrSize[1] * 0.57]},
                         {'Name': 'Options',
                          'Position': [self.scrSize[0] * 0.6, self.scrSize[1] * 0.64]},
                         {'Name': 'Quit',
                          'Position': [self.scrSize[0] * 0.6, self.scrSize[1] * 0.71]}]
        self.currentMenu = 0
        # Flag list
        self.flags = {'NewGame': False,
                      'LoadGame': [False, False],
                      'Options': False,
                      'Quit': False}
        # If there are saved files, you'll be able to access the 'Load Game' menu
        if self.savedFiles is not None:
            self.flags['LoadGame'][1] = True

        # Setting a plane, transparent background
        self.background = pygame.Surface(self.scrSize)
        self.background.fill(COLORS['BLACK'])
        # Setting the text font for the pause menu (set your own)
        # self.font = pygame.font.SysFont('Calibri', 25, True, False)
        self.font = pygame.font.Font(self.root + '/fonts/AceRecords.ttf', 30)
        self.titleFont = pygame.font.Font(self.root + '/fonts/AceRecords.ttf', 100)
        # Pause interface text (will include images on next versions)
        self.titleText = []
        for x in self.menuList:
            if x['Name'] == 'Load Game' and not self.flags['LoadGame'][1]:
                self.titleText.append(self.font.render(x['Name'], ANTIALIASING, COLORS['GREY']))
            else:
                self.titleText.append(self.font.render(x['Name'], ANTIALIASING, COLORS['WHITE']))
        self.titleText.append(self.titleFont.render("Primal Ring", ANTIALIASING, COLORS['WHITE']))
        # Setting initial cursor's position
        self.cursor = self.cursorSurface.get_rect()
        self.cursor.x = self.scrSize[0] * 0.6
        self.cursor.y = self.scrSize[1] * 0.3
        # Debug
        if self.debug:
            pass

    # ---------- Methods --------------------------
    def event_handler(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.flags['Quit'] = True           # This enable the X-window exit button
                return True
            # New Game menu
            if self.flags['NewGame']:               # WIP
                # print("Now you are in New Game")
                """ Some stuff will happen here, asking for a name and creating a game file
                    for it."""
                if not self.initGame:
                    self.initGame = True
            # Load Game menu
            elif self.flags['LoadGame'][0]:         # WIP
                # We enable to access the load screen if we have any saved files
                if self.flags['LoadGame'][1]:
                    """ Some stuff will happen here, asking for a name and
                        loading all stuff in order to continue."""
                    if not self.initGame:
                        self.initGame = True
                else:
                    self.flags['LoadGame'][0] = False
            # Options menu
            elif self.flags['Options']:             # WIP
                print("Now you are in Options")
                self.flags['Options'] = False
            # Title menu
            else:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP:
                        self.go_up()
                    elif e.key == pygame.K_DOWN:
                        self.go_down()
                    elif e.key == pygame.K_RETURN:
                        if self.menuList[self.currentMenu]['Name'] == 'New Game':
                            self.flags['NewGame'] = True
                        elif self.menuList[self.currentMenu]['Name'] == 'Load Game':
                            self.flags['LoadGame'][0] = True
                        elif self.menuList[self.currentMenu]['Name'] == 'Options':
                            self.flags['Options'] = True
                        else:
                            self.flags['Quit'] = True
                            return True
        # This is for New Game/Load Game fade out effects
        if self.opacity >= 255:
            return True

        return False

    def run_logic(self):
        self.cursor.x = self.menuList[self.currentMenu]['Position'][0]
        self.cursor.y = self.menuList[self.currentMenu]['Position'][1]
        # We init the fade out animation if we start a game, new or loaded
        if self.initGame:
            self.opacity += 2
            self.cover.set_alpha(self.opacity)

    def display_frame(self):
        # Background attached to all the window surface
        self.screen.blit(self.background, [0, 0])
        # Title
        self.screen.blit(self.titleText[len(self.titleText) - 1], [150, 100])
        # Cursor
        self.screen.blit(self.cursorSurface, [self.cursor.x, self.cursor.y])
        # Title Screen text
        for x in range(len(self.menuList)):
            self.screen.blit(self.titleText[x], self.menuList[x]['Position'])
        # Cover
        self.screen.blit(self.cover, [0, 0])
        # Debug
        if self.debug:
            pass

        pygame.display.flip()

    def go_down(self):
        if self.currentMenu == len(self.menuList) - 1:
            self.currentMenu = 0
        else:
            self.currentMenu += 1
            if self.menuList[self.currentMenu]['Name'] == 'Load Game' and not self.flags['LoadGame'][1]:
                self.currentMenu += 1

    def go_up(self):
        if self.currentMenu == 0:
            self.currentMenu = len(self.menuList) - 1
        else:
            self.currentMenu -= 1
            if self.menuList[self.currentMenu]['Name'] == 'Load Game' and not self.flags['LoadGame'][1]:
                self.currentMenu -= 1

    def __str__(self):
        return "Title"


class NewGame(object):
    # ---------- Constructor ----------------------
    def __init__(self, screen, scr_size, font, debug=False):
        # -- Attributes -----------------------
        self.debug = debug                                  # Flag for debugging into the game
        self.screen = screen                                # A reference for the main screen
        self.scrSize = scr_size
        # Setting a plane, transparent background
        self.background = pygame.Surface(self.scrSize)
        self.background.fill(COLORS['BLACK'])
        # Setting the text font for the new game menu
        self.font = font
        # New Game interface text (will include images on next versions)
        self.nGameText = []
        self.nGameText.append(self.font.render("What's your name, little fella?",
                                               ANTIALIASING, COLORS['WHITE']))

