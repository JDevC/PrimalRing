#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
from views._Screen import _Screen
from views._ScreenHolder import _ScreenHolder
from .OptionsScreen import OptionsScreen
from constants import COLORS, ANTIALIASING, ROOT
from SaveGame import SaveGame


class TitleScreen(_Screen):
    def __init__(self, screen, scr_size, managers, config, debug: bool = False):
        """ This class will display the title screen, showing a background animation and playing the main theme
        while we navigate though the main menu. That's the initial idea, of course.

        :param screen: A reference for the main screen
        :param scr_size: The screen size (Default: 600 * 800)
        :param sound_manager:
        :param lang_manager:
        :param config: General game configuration settings
        :param debug: Flag for debugging into the game
        """
        super().__init__(screen, scr_size, managers, debug)
        self._config = config
        # Setting the text fonts (set your own)
        fonts_dir = f'{ROOT}/resources/fonts/'
        self._font = pygame.font.Font(f'{fonts_dir}AceRecords.ttf', 30)
        self._titleFont = pygame.font.Font(f'{fonts_dir}AceRecords.ttf', 100)
        # Saved games list (or None)
        self._savedFiles = SaveGame.load_files()
        self._musicTheme = 'Main Theme'
        # ---------------------------- Sub-screen elements ---------------------------
        self._newGame = _ScreenHolder()
        self._loadGame = _ScreenHolder()
        self._options = _ScreenHolder()
        # ------------------------------- Flag list --------------------------------
        self.flags = {'NewGame': False, 'LoadGame': [False, False], 'Options': False, 'Quit': False}
        # New Game/Load Game fading surface
        self._cover = pygame.Surface(self.scrSize)
        self._cover.fill(COLORS['BLACK'])
        self._cover.set_alpha(0)
        self._opacity = 0
        # This flag commands the main class to pass from title scene to game scene when it's true
        self.initGame = False
        # Menu
        self.menuList, self.titleText, self.currentMenu = self._init_ui_text(self._font, self._titleFont)
        # Cursor elements
        self.cursorSurface = self._managers.image.load_image(f"Cursor.png")
        self.cursorSurface.set_colorkey(COLORS['WHITE'])
        # Setting initial cursor's position
        self.cursor = self.cursorSurface.get_rect()
        self.cursorDespl = self.cursor.x = self.menuList[0]['Position'][0] - 35
        # Cursor direction and velocity (positive = right; negative = left)
        self.cursorDir = 1
        # If there are saved files, you'll be able to access the 'Load Game' menu
        if self._savedFiles is not None:
            self.flags['LoadGame'][1] = True

        if not self.flags['LoadGame'][1]:
            self.titleText[1] = self._font.render(self.menuList[1]['Name'], ANTIALIASING, COLORS['GREY'])

        if self.debug:
            pass

    # ---------- MAIN FLOW --------------------------
    def event_handler(self):
        # New Game Screen's events
        if self._newGame.flag:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return self._quit_game()
        # Load Game Screen's events
        elif self._loadGame.flag:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return self._quit_game()
        # Options Screen's events
        elif self._options.flag:
            if self._options.screen.event_handler():
                if self._options.screen.quit_all:
                    return self._quit_game()
                else:
                    self._config = SaveGame.load_config()
                    self.menuList, self.titleText, self.currentMenu =\
                        self._init_ui_text(self._font, self._titleFont, True)
                    self._options = _ScreenHolder()
        # Title Screen's events
        else:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return self._quit_game()
                # New Game menu
                if self.flags['NewGame']:               # WIP
                    # Some stuff will happen here, asking for a name and creating a game file for it.
                    self._start_game()
                # Load Game menu
                elif self.flags['LoadGame'][0]:         # WIP
                    # We enable to access the load screen if we have any saved files
                    if self.flags['LoadGame'][1]:
                        # Some stuff will happen here, asking for a name and
                        # loading all stuff in order to continue.
                        self._start_game()
                    else:
                        self.flags['LoadGame'][0] = False
                # Options menu
                elif self.flags['Options']:
                    screen =\
                        OptionsScreen(self.screen, self.scrSize, self._managers, self._config, self._font)
                    self._options = _ScreenHolder(screen, True)
                    self.flags['Options'] = False
                # Title menu
                else:
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_UP:
                            self._cursor_up()
                        elif e.key == pygame.K_DOWN:
                            self._cursor_down()
                        elif e.key == pygame.K_RETURN:
                            self._managers.sound.play_fx('Accept')
                            if self.menuList[self.currentMenu]["ID"] == "NewGame":
                                self.flags['NewGame'] = True
                            elif self.menuList[self.currentMenu]["ID"] == "LoadGame":
                                self.flags['LoadGame'][0] = True
                            elif self.menuList[self.currentMenu]["ID"] == "Options":
                                self.flags['Options'] = True
                            else:
                                return self._quit_game()
        # This is for New Game/Load Game fade out effects
        if self._opacity >= 255:
            return True

        return False

    def run_logic(self):
        # Cursor wiggles
        self.cursor.x = self._wiggle(self.cursor.x)
        self.cursor.y = self.menuList[self.currentMenu]['Position'][1] + 3
        # We init the fade out animation if we start a game, new or loaded
        if self.initGame:
            self._opacity += 2
            self._cover.set_alpha(self._opacity)
        elif self._options.flag:
            self._options.screen.update()

    def display_frame(self):
        if self._newGame.flag:
            self._newGame.screen.display()
        elif self._loadGame.flag:
            self._loadGame.screen.display()
        elif self._options.flag:
            self._options.screen.display()
        else:
            self.screen.blit(self.background, [0, 0])
            self.screen.blit(self.titleText[len(self.titleText) - 1], [150, 100])
            self.screen.blit(self.cursorSurface, [self.cursor.x, self.cursor.y])
            for x in range(len(self.menuList)):
                self.screen.blit(self.titleText[x], self.menuList[x]['Position'])
            self.screen.blit(self._cover, [0, 0])
            if self.debug:
                pass

        pygame.display.flip()

    # ---------- Public Methods --------------------
    def reset_opacity(self):
        self._opacity = 0
        self._cover.set_alpha(self._opacity)

    def set_theme(self):
        if self._musicTheme is not None:
            self._managers.sound.play_music(self._musicTheme, 13)

    # -------------- Internal Methods --------------
    def _init_ui_text(self, font, title_font, refresh: bool = False):
        menu_list = [{
            "ID": "NewGame",
            "Name": _("New Game"),
            "Position": [self.scrSize[0] * 0.6, self.scrSize[1] * 0.5]
        }, {
            "ID": "LoadGame",
            "Name": _("Load Game"),
            "Position": [self.scrSize[0] * 0.6, self.scrSize[1] * 0.57]
        }, {
            "ID": "Options",
            "Name": _("Options"),
            "Position": [self.scrSize[0] * 0.6, self.scrSize[1] * 0.64]
        }, {
            "ID": "Quit",
            "Name": _("Quit"),
            "Position": [self.scrSize[0] * 0.6, self.scrSize[1] * 0.71]
        }]

        # Title interface text
        menu_txt = [font.render(x['Name'], ANTIALIASING, COLORS['WHITE']) for x in menu_list]
        menu_txt.append(title_font.render("Primal Ring", ANTIALIASING, COLORS['WHITE']))
        current_menu = self.currentMenu if refresh else 0

        return menu_list, menu_txt, current_menu

    def _start_game(self):
        if not self.initGame:
            self.initGame = True
            self._managers.sound.music_fadeout(1500)

    def _quit_game(self):
        # We kill the music stream
        self._managers.sound.panic()
        self.flags['Quit'] = True
        return True

    def _cursor_down(self):
        self._managers.sound.play_fx('Select')
        if self.currentMenu == len(self.menuList) - 1:
            self.currentMenu = 0
        else:
            self.currentMenu += 1
            if self.menuList[self.currentMenu]["ID"] == "LoadGame" and not self.flags['LoadGame'][1]:
                self.currentMenu += 1

    def _cursor_up(self):
        self._managers.sound.play_fx('Select')
        if self.currentMenu == 0:
            self.currentMenu = len(self.menuList) - 1
        else:
            self.currentMenu -= 1
            if self.menuList[self.currentMenu]["ID"] == "LoadGame" and not self.flags['LoadGame'][1]:
                self.currentMenu -= 1

    def _wiggle(self, cursor_x):
        # Movement limits
        if abs(cursor_x - self.cursorDespl) >= 6:
            # Inverting direction
            self.cursorDir *= -1

        return cursor_x + self.cursorDir

