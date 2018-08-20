#!/usr/bin/env python3

# ---------------------- IMPORTS ---------------------
# Python libs
import pygame
# Own libs
from constants import COLORS, SURFACE_MID_ALPHA, ANTIALIASING, ROOT, VOLUME_BAR, SLIDER, TICKER, FULL_SCREEN
from SaveGame import SaveGame


class _Screen:
    def __init__(self, screen, scr_size, sound_manager, debug: bool=False):
        """ Parent class for game screens

        :param screen: A reference for the main screen
        :param scr_size: The screen size (Default: 600 * 800)
        :param sound_manager:
        :param debug: Flag for debugging into the game
        """
        self.screen = screen
        self.scrSize = scr_size
        self.soundMan = sound_manager
        self.debug = debug
        # Setting a plane black background
        self.background = pygame.Surface(self.scrSize)
        self.background.fill(COLORS['BLACK'])


class TitleScreen(_Screen):
    def __init__(self, screen, scr_size, sound_manager, lang_manager, config, debug: bool=False):
        """ This class will display the title screen, showing a background animation and playing the main theme
        while we navigate though the main menu. That's the initial idea, of course.

        :param screen: A reference for the main screen
        :param scr_size: The screen size (Default: 600 * 800)
        :param sound_manager:
        :param lang_manager:
        :param config: General game configuration settings
        :param debug: Flag for debugging into the game
        """
        super().__init__(screen, scr_size, sound_manager, debug)
        self.langMan = lang_manager
        # ----------------------------- Source folders -----------------------------
        img_dir = f'{ROOT}/resources/images/'
        fonts_dir = f'{ROOT}/resources/fonts/'
        # /////////////////////////////// ATTRIBUTES ///////////////////////////////
        self.config = config
        # Setting the text fonts (set your own)
        self.font = pygame.font.Font(f'{fonts_dir}AceRecords.ttf', 30)
        self.titleFont = pygame.font.Font(f'{fonts_dir}AceRecords.ttf', 100)
        # Saved games list (or None)
        self.savedFiles = SaveGame.load_files()
        self.musicTheme = 'Main Theme'
        # ---------------------------- New Game elements ---------------------------
        self.newGame = None                                 # New Game screen reference
        self.newGameFlag = False                            # New Game event handling flag
        # --------------------------- Load Game elements ---------------------------
        self.loadGame = None                                # Load Game screen reference
        self.loadGameFlag = False                           # Load Game event handling flag
        # ---------------------------- Options elements ----------------------------
        self.options = None                                 # Options screen reference
        self.optionsFlag = False                            # Options event handling flag
        # ------------------------------- Flag list --------------------------------
        self.flags = {'NewGame': False, 'LoadGame': [False, False], 'Options': False, 'Quit': False}
        # New Game/Load Game fading surface
        self.cover = pygame.Surface(self.scrSize)
        self.cover.fill(COLORS['BLACK'])
        self.cover.set_alpha(0)
        self.opacity = 0
        # This flag commands the main class to pass from title scene to game scene when it's true
        self.initGame = False
        # Menu
        self.menuList, self.titleText, self.currentMenu = self._init_ui_text(self.font, self.titleFont)
        # Cursor elements
        self.cursorSurface = pygame.image.load(f"{img_dir}Cursor.png").convert()
        self.cursorSurface.set_colorkey(COLORS['WHITE'])
        # Setting initial cursor's position
        self.cursor = self.cursorSurface.get_rect()
        self.cursorDespl = self.cursor.x = self.menuList[0]['Position'][0] - 35
        # Cursor direction and velocity (positive = right; negative = left)
        self.cursorDir = 1
        # If there are saved files, you'll be able to access the 'Load Game' menu
        if self.savedFiles is not None:
            self.flags['LoadGame'][1] = True

        if not self.flags['LoadGame'][1]:
            self.titleText[1] = self.font.render(self.menuList[1]['Name'], ANTIALIASING, COLORS['GREY'])

        if self.debug:
            pass

    # ---------------------------- INITIALIZERS ----------------------------
    def _init_ui_text(self, font, title_font, refresh=False):
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

        if not refresh:
            current_menu = 0
        else:
            current_menu = self.currentMenu

        return menu_list, menu_txt, current_menu

    # ---------- Methods --------------------------
    def event_handler(self):
        # New Game Screen's events
        if self.newGameFlag:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return self.quit_game()
        # Load Game Screen's events
        elif self.loadGameFlag:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return self.quit_game()
        # Options Screen's events
        elif self.optionsFlag:
            if self.options.event_handler():
                if self.options.quit_all:
                    return self.quit_game()
                else:
                    self.config = SaveGame.load_config()
                    self.menuList, self.titleText, self.currentMenu =\
                        self._init_ui_text(self.font, self.titleFont, True)
                    self.options = None
                    self.optionsFlag = False
        # Title Screen's events
        else:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return self.quit_game()
                # New Game menu
                if self.flags['NewGame']:               # WIP
                    # Some stuff will happen here, asking for a name and creating a game file
                    # for it.
                    if not self.initGame:
                        self.initGame = True
                        # Fading out music (milliseconds)
                        pygame.mixer.music.fadeout(1500)
                # Load Game menu
                elif self.flags['LoadGame'][0]:         # WIP
                    # We enable to access the load screen if we have any saved files
                    if self.flags['LoadGame'][1]:
                        # Some stuff will happen here, asking for a name and
                        # loading all stuff in order to continue.
                        if not self.initGame:
                            self.initGame = True
                            # Fading out music (milliseconds)
                            pygame.mixer.music.fadeout(1500)
                    else:
                        self.flags['LoadGame'][0] = False
                # Options menu
                elif self.flags['Options']:
                    self.options = OptionsScreen(self.screen, self.scrSize, self.soundMan, self.langMan, self.config,
                                                 self.font)
                    self.optionsFlag = True
                    self.flags['Options'] = False
                # Title menu
                else:
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_UP:
                            self.cursor_up()
                        elif e.key == pygame.K_DOWN:
                            self.cursor_down()
                        elif e.key == pygame.K_RETURN:
                            self.soundMan.play_fx('Accept')
                            if self.menuList[self.currentMenu]["ID"] == "NewGame":
                                self.flags['NewGame'] = True
                            elif self.menuList[self.currentMenu]["ID"] == "LoadGame":
                                self.flags['LoadGame'][0] = True
                            elif self.menuList[self.currentMenu]["ID"] == "Options":
                                self.flags['Options'] = True
                            else:
                                return self.quit_game()
        # This is for New Game/Load Game fade out effects
        if self.opacity >= 255:
            return True

        return False

    def run_logic(self):
        # Cursor wiggles
        self.cursor.x = self._wiggle(self.cursor.x)
        self.cursor.y = self.menuList[self.currentMenu]['Position'][1] + 3
        # We init the fade out animation if we start a game, new or loaded
        if self.initGame:
            self.opacity += 2
            self.cover.set_alpha(self.opacity)
        elif self.optionsFlag:
            self.options.update()

    def display_frame(self):
        # Subscreens
        if self.newGameFlag:
            self.newGame.display()
        elif self.loadGameFlag:
            self.loadGame.display()
        elif self.optionsFlag:
            self.options.display()
        else:
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

    def cursor_down(self):
        self.soundMan.play_fx('Select')
        if self.currentMenu == len(self.menuList) - 1:
            self.currentMenu = 0
        else:
            self.currentMenu += 1
            if self.menuList[self.currentMenu]["ID"] == "LoadGame" and not self.flags['LoadGame'][1]:
                self.currentMenu += 1

    def cursor_up(self):
        self.soundMan.play_fx('Select')
        if self.currentMenu == 0:
            self.currentMenu = len(self.menuList) - 1
        else:
            self.currentMenu -= 1
            if self.menuList[self.currentMenu]["ID"] == "LoadGame" and not self.flags['LoadGame'][1]:
                self.currentMenu -= 1

    def _wiggle(self, cursor_x):
        """ Cursor simple "live" effect

        :param cursor_x:
        :return: Cursor's new position
        """
        # Movement limits
        if abs(cursor_x - self.cursorDespl) >= 6:
            # Inverting direction
            self.cursorDir *= -1

        return cursor_x + self.cursorDir

    def reset_opacity(self):
        self.opacity = 0
        self.cover.set_alpha(self.opacity)

    def set_theme(self):
        """ Sets music theme in this scene """
        # We start later because we aren't displaying splash screen again
        if self.musicTheme is not None:
            self.soundMan.play_music(self.musicTheme, 13)

    def quit_game(self):
        """ Quick game exit """
        # We kill the music stream
        self.soundMan.panic()
        self.flags['Quit'] = True
        return True


class NewGameScreen(_Screen):
    def __init__(self, screen, scr_size, sound_manager, font, debug=False):
        super().__init__(screen, scr_size, sound_manager, debug)
        # Setting the text font for the new game menu
        self.font = font
        # New Game interface text (will include images on next versions)
        self.nGameText = [self.font.render("What's your name, little fella?", ANTIALIASING, COLORS['WHITE'])]


class OptionsScreen(_Screen):
    def __init__(self, screen, scr_size, sound_manager, lang_manager, config, font, debug: bool=False):
        super().__init__(screen, scr_size, sound_manager, debug)

        self.langMan = lang_manager
        # Setting the text font for the new game menu
        self.font = font
        # Options interface text (will include images on next versions)
        self.optionList, self.optText, self.currentMenu = self._init_ui_text(self.font)
        # Cursor
        self.cursorSurface, self.cursor = self._init_cursor(self.optionList[0])
        # Full screen interface
        self._init_fscreen_ui(TICKER['Canvas'], TICKER['Fill'], COLORS['WHITE'], COLORS['GREY'])
        # Volume interface
        self._init_volume_ui(VOLUME_BAR, SLIDER, COLORS["GREY"], COLORS["GREY"])
        # Language interface
        self.langUtils = OptionsScreen._LangUIUtils(self.font)
        # Flag for complete game exit
        self.quit_all = False
        # Setting GUI controls
        if config is not None:
            self.fullScreenFlag = config['full_screen']
            self.soundMan.set_music_vol(config['music_volume'])
            self.musicSliderPoint = [self.optionList[1]['Position'][0] + 220 + (config['music_volume'] / self.volRatio),
                                     self.optionList[1]['Position'][1]]
            self.soundMan.set_fx_vol(config['fx_volume'])
            self.fxSliderPoint = [self.optionList[2]['Position'][0] + 220 + (config['fx_volume'] / self.volRatio),
                                  self.optionList[2]['Position'][1]]
            self.currentLang = self.langUtils.set_index(config["lang"])
        else:
            self.fullScreenFlag = FULL_SCREEN
            self.musicSliderPoint = [self.optionList[1]['Position'][0] + 200 + VOLUME_BAR[0] - SLIDER[0],
                                     self.optionList[1]['Position'][1]]
            self.fxSliderPoint = [self.optionList[2]['Position'][0] + 200 + VOLUME_BAR[0] - SLIDER[0],
                                  self.optionList[2]['Position'][1]]
            self.currentLang = self.langUtils.set_index("en")

        if self.debug:
            self.debugText = self.font.render(f'Music slider x = {self.musicSliderPoint[0]}; '
                                              f'Effects slider x = {self.fxSliderPoint[0]}',
                                              ANTIALIASING, COLORS['WHITE'])

    # ---------------------------- INITIALIZERS ----------------------------
    def _init_ui_text(self, font, refresh=False):
        options = [
            {
                "ID": "FullScreen",
                'Name': _("FullScreen"),
                'Position': [self.scrSize[0] * 0.2, self.scrSize[1] * 0.2]
            }, {
                "ID": "MusicVol",
                'Name': _("Music Volume"),
                'Position': [self.scrSize[0] * 0.2, self.scrSize[1] * 0.27]
            }, {
                "ID": "EffectsVol",
                'Name': _("Effects Volume"),
                'Position': [self.scrSize[0] * 0.2, self.scrSize[1] * 0.34]
            }, {
                "ID": "Language",
                'Name': _("Language"),
                'Position': [self.scrSize[0] * 0.2, self.scrSize[1] * 0.41]
            }, {
                "ID": "Gallery",
                'Name': _("Gallery"),
                'Position': [self.scrSize[0] * 0.2, self.scrSize[1] * 0.48]
            }, {
                "ID": "Credits",
                'Name': _("Credits"),
                'Position': [self.scrSize[0] * 0.2, self.scrSize[1] * 0.55]
            }, {
                "ID": "Back",
                'Name': _('Back to Main Menu'),
                'Position': [self.scrSize[0] * 0.2, self.scrSize[1] * 0.62]
            }]

        options_txt = [font.render(option['Name'], ANTIALIASING, COLORS['WHITE']) for option in options]

        if not refresh:
            current_menu = 0
        else:
            current_menu = self.currentMenu

        return options, options_txt, current_menu

    def _init_cursor(self, def_option: []):
        cursor_surface = pygame.Surface((170, 25))
        cursor_surface.fill(COLORS['GREEN'])
        cursor_surface.set_alpha(SURFACE_MID_ALPHA)
        # Setting initial cursor's position
        cursor = cursor_surface.get_rect()
        cursor.x = def_option['Position'][0]
        cursor.y = def_option['Position'][1] - 0.2

        return cursor_surface, cursor

    def _init_fscreen_ui(self, canvas_dim: int, fill_dim: int, canvas_color: [], fill_color: []):
        self.fullScreenTickBox = pygame.Surface((canvas_dim, canvas_dim))
        self.fullScreenTickBox.fill(canvas_color)
        self.fullScreenTick = pygame.Surface((fill_dim, fill_dim))
        self.fullScreenTick.fill(fill_color)

    def _init_volume_ui(self, vol_bar_dim: tuple, slider_dim: tuple, vol_bar_color: [], slider_color: []):
        # Volume interface
        self.volBar = pygame.Surface(vol_bar_dim)
        self.volBar.fill(vol_bar_color)
        self.musicSlider = pygame.Surface(slider_dim)
        self.musicSlider.fill(slider_color)
        self.fxSlider = pygame.Surface(slider_dim)
        self.fxSlider.fill(slider_color)
        # Volume map for SLIDER Controls
        self.volRatio = 1.0 / (VOLUME_BAR[0] - SLIDER[0])
        # Flags for continuum slider scrolling
        self.sliderFlags = [False, False]

    # ---------------------------- MAIN LOOP FUNCTIONS ----------------------------
    def event_handler(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.quit_all = True
                return True

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    self.go_up()
                elif e.key == pygame.K_DOWN:
                    self.go_down()

                if e.key == pygame.K_RIGHT:
                    if self.optionList[self.currentMenu]["ID"] == "Language":
                        self.currentLang = self.langUtils.next_index(self.currentLang)
                    else:
                        self.sliderFlags[0] = True
                elif e.key == pygame.K_LEFT:
                    if self.optionList[self.currentMenu]["ID"] == "Language":
                        self.currentLang = self.langUtils.prev_index(self.currentLang)
                    else:
                        self.sliderFlags[1] = True
                elif e.key == pygame.K_ESCAPE:
                    self.soundMan.play_fx('Cancel')
                    return True
                elif e.key == pygame.K_RETURN:
                    if self.optionList[self.currentMenu]["ID"] == "Back":
                        self.soundMan.play_fx('Accept')
                        self.save_config()
                        return True
                    elif self.optionList[self.currentMenu]["ID"] == "FullScreen":
                        self.switch_full_screen(not self.fullScreenFlag)

            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    self.sliderFlags[0] = False
                elif e.key == pygame.K_LEFT:
                    self.sliderFlags[1] = False

        return False

    def update(self):
        # Cursor
        self.cursor.x = self.optionList[self.currentMenu]['Position'][0]
        self.cursor.y = self.optionList[self.currentMenu]['Position'][1]
        if self.fullScreenFlag:
            self.fullScreenTick.set_alpha(255)
        else:
            self.fullScreenTick.set_alpha(0)
        # Volume sliders
        if self.sliderFlags[0]:
            self._slider_to_right(self.optionList[self.currentMenu])
        elif self.sliderFlags[1]:
            self._slider_to_left(self.optionList[self.currentMenu])
        # Language change
        if self.langUtils.has_changed(self.currentLang):
            self.langMan.set_lang(self.langUtils.get_id(self.currentLang))

            self.optionList, self.optText, self.currentMenu = self._init_ui_text(self.font, True)
            self.langUtils.refresh(self.font)
        # Debug text
        if self.debug:
            self.debugText = self.font.render(f'Music slider x = {self.musicSliderPoint[0]}; '
                                              + f'Effects slider x = {self.fxSliderPoint[0]}',
                                              ANTIALIASING, COLORS['WHITE'])

    def display(self):
        # Background attached to all the window surface
        self.screen.blit(self.background, [0, 0])
        # Cursor
        self.screen.blit(self.cursorSurface, [self.cursor.x, self.cursor.y])
        # Full screen interface
        self.screen.blit(self.fullScreenTickBox,
                         [self.optionList[0]['Position'][0] + 220, self.optionList[0]['Position'][1] + 8])
        self.screen.blit(self.fullScreenTick,
                         [self.optionList[0]['Position'][0] + 222, self.optionList[0]['Position'][1] + 10])
        # Volume interface
        self.screen.blit(self.volBar,
                         [self.optionList[1]['Position'][0] + 220, self.optionList[1]['Position'][1] + 15])
        self.screen.blit(self.volBar,
                         [self.optionList[2]['Position'][0] + 220, self.optionList[2]['Position'][1] + 15])
        self.screen.blit(self.fxSlider, self.fxSliderPoint)
        self.screen.blit(self.musicSlider, self.musicSliderPoint)
        # Language interface
        self.screen.blit(self.langUtils.get_text(self.currentLang),
                         [self.optionList[3]["Position"][0] + 220, self.optionList[3]["Position"][1]])
        # Option text
        for x in range(len(self.optText)):
            self.screen.blit(self.optText[x], self.optionList[x]['Position'])
        # Debug
        if self.debug:
            self.screen.blit(self.debugText, [100, 50])

    def go_down(self):
        self.soundMan.play_fx('Select')
        self.currentMenu = 0 if self.currentMenu == len(self.optionList) - 1 else self.currentMenu + 1

    def go_up(self):
        self.soundMan.play_fx('Select')
        self.currentMenu = len(self.optionList) - 1 if self.currentMenu == 0 else self.currentMenu - 1

    def switch_full_screen(self, full_screen=False):
        if self.optionList[self.currentMenu]["ID"] == "FullScreen":
            self.soundMan.play_fx('Accept')
            self.fullScreenFlag = full_screen

    def save_config(self):
        """ It takes all config values set into this screen and saves them into a config file """
        SaveGame.save_changes(self.fullScreenFlag, self.soundMan.get_music_vol(), self.soundMan.get_fx_vol(),
                              self.langUtils.get_id(self.currentLang))

    # These two slider functions move the volume controls to left or right, depending on the desired
    # direction.
    def _slider_to_right(self, slider_opt: {}) -> None:
        if slider_opt["ID"] == "MusicVol":
            if self.musicSliderPoint[0] < slider_opt['Position'][0] + 510:
                self.musicSliderPoint[0] += 1
                self._convert_volume(self.musicSliderPoint[0], slider_opt["ID"])
        elif slider_opt["ID"] == "EffectsVol":
            self.soundMan.play_fx('Select')
            if self.fxSliderPoint[0] < slider_opt['Position'][0] + 510:
                self.fxSliderPoint[0] += 1
                self._convert_volume(self.fxSliderPoint[0], slider_opt["ID"])

    def _slider_to_left(self, slider_opt: {}) -> None:
        if slider_opt["ID"] == "MusicVol":
            if self.musicSliderPoint[0] > slider_opt['Position'][0] + 220:
                self.musicSliderPoint[0] -= 1
                self._convert_volume(self.musicSliderPoint[0], slider_opt["ID"])
        elif slider_opt["ID"] == "EffectsVol":
            self.soundMan.play_fx('Select')
            if self.fxSliderPoint[0] > slider_opt['Position'][0] + 220:
                self.fxSliderPoint[0] -= 1
                self._convert_volume(self.fxSliderPoint[0], slider_opt["ID"])

    def _convert_volume(self, slider_level, option):
        """ This converts the GUI volume control into real sound values for pygame lib

        :param slider_level:
        :param option:
        :return:
        """
        slider = slider_level - 380
        if option == "EffectsVol":
            self.soundMan.set_fx_vol(slider * self.volRatio)
        elif option == "MusicVol":
            self.soundMan.set_music_vol(slider * self.volRatio)

    # ---------------------------- HELPERS ----------------------------
    class _LangUIUtils:
        def __init__(self, font):
            self.current = 0
            self.langTexts = {
                0: {"ID": "en", "Text": font.render(_("English"), ANTIALIASING, COLORS["WHITE"])},
                1: {"ID": "es", "Text": font.render(_("Spanish"), ANTIALIASING, COLORS["WHITE"])}
            }

        def refresh(self, font):
            self.langTexts = {
                0: {"ID": "en", "Text": font.render(_("English"), ANTIALIASING, COLORS["WHITE"])},
                1: {"ID": "es", "Text": font.render(_("Spanish"), ANTIALIASING, COLORS["WHITE"])}
            }

        def get_id(self, index: int):
            return self.langTexts[index]["ID"]

        def get_text(self, index: int):
            return self.langTexts[index]["Text"]

        def set_index(self, lang_id: str):
            for index, val in self.langTexts.items():
                if val["ID"] == lang_id:
                    self.current = index
                    return index

        def next_index(self, index):
            next_index = index + 1

            if next_index >= len(self.langTexts):
                next_index = 0

            return next_index

        def prev_index(self, index):
            prev_index = index - 1

            if prev_index < 0:
                prev_index = len(self.langTexts) - 1

            return prev_index

        def has_changed(self, index: int):
            changed = self.current != index
            self.current = index
            return changed
