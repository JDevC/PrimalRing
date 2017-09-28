#!/usr/bin/env python3

# ---------------------- IMPORTS ---------------------
# Python libs
import pygame
# Own libs
from constants6 import COLORS, SURFACE_MID_ALPHA, ANTIALIASING, ROOT, VOLUME_BAR, SLIDER, TICKER, FULL_SCREEN
from SaveGame import load_files, load_config, save_changes


class _Screen:
    def __init__(self, screen, scr_size, debug=False):
        self.debug = debug
        self.screen = screen
        self.scrSize = scr_size
        # Setting a plane, transparent background
        self.background = pygame.Surface(self.scrSize)
        self.background.fill(COLORS['BLACK'])


class TitleScreen(_Screen):
    def __init__(self, screen, scr_size, config, debug=False):
        """ This class will display the title screen, showing a background animation
                and playing the main theme while we navigate though the main menu. That's
                the initial idea, of course.

        :param screen: A reference for the main screen
        :param scr_size: The screen size (Default: 600 * 800)
        :param config: General game configuration settings
        :param debug: Flag for debugging into the game
        """
        super().__init__(screen, scr_size, debug)
        # -- Source folders -------------------
        sound_dir = f'{ROOT}/resources/sounds/'
        img_dir = f'{ROOT}/resources/images/'
        music_dir = f'{ROOT}/resources/music/'
        fonts_dir = f'{ROOT}/resources/fonts/'
        # -- Attributes -----------------------
        self.savedFiles = load_files()                      # A list of saved games (or None)
        self.soundDict = {'Select': pygame.mixer.Sound(f'{sound_dir}select.ogg'),
                          'Accept': pygame.mixer.Sound(f'{sound_dir}accept.ogg'),
                          'Cancel': pygame.mixer.Sound(f'{sound_dir}cancel.ogg')}
        self.musicTheme = f'{music_dir}strike_the_earth.ogg'
        self.config = config
        # New Game elements
        self.newGame = None                                 # New Game object reference
        self.newGameFlag = False                            # New Game event handling flag
        # Load Game elements
        self.loadGame = None                                # Load Game object reference
        self.loadGameFlag = False                           # Load Game event handling flag
        # Options elements
        self.options = None                                 # Options object reference
        self.optionsFlag = False                            # Options event handling flag
        # New Game/Load Game fading surface
        self.cover = pygame.Surface(self.scrSize)
        self.cover.fill(COLORS['BLACK'])
        self.cover.set_alpha(0)
        self.opacity = 0
        # This flag commands the main class to pass from title scene to game scene when it's true
        self.initGame = False
        # Cursor elements
        self.cursorSurface = pygame.image.load(f'{img_dir}Cursor.png').convert()
        self.cursorSurface.set_colorkey(COLORS['WHITE'])
        self.menuList = [{'Name': 'New Game', 'Position': [self.scrSize[0] * 0.6, self.scrSize[1] * 0.5]},
                         {'Name': 'Load Game', 'Position': [self.scrSize[0] * 0.6, self.scrSize[1] * 0.57]},
                         {'Name': 'Options', 'Position': [self.scrSize[0] * 0.6, self.scrSize[1] * 0.64]},
                         {'Name': 'Quit', 'Position': [self.scrSize[0] * 0.6, self.scrSize[1] * 0.71]}]
        self.currentMenu = 0
        # Setting initial cursor's position
        self.cursor = self.cursorSurface.get_rect()
        self.cursorDespl = self.cursor.x = self.menuList[0]['Position'][0] - 35
        # Cursor direction and velocity (positive = right; negative = left)
        self.cursorDir = 1
        # Flag list
        self.flags = {'NewGame': False, 'LoadGame': [False, False], 'Options': False, 'Quit': False}
        # If there are saved files, you'll be able to access the 'Load Game' menu
        if self.savedFiles is not None:
            self.flags['LoadGame'][1] = True

        # Setting the text font for the pause menu (set your own)
        self.font = pygame.font.Font(f'{fonts_dir}AceRecords.ttf', 30)
        self.titleFont = pygame.font.Font(f'{fonts_dir}AceRecords.ttf', 100)

        # Title interface text
        self.titleText = []
        for x in self.menuList:
            if x['Name'] == 'Load Game' and not self.flags['LoadGame'][1]:
                self.titleText.append(self.font.render(x['Name'], ANTIALIASING, COLORS['GREY']))
            else:
                self.titleText.append(self.font.render(x['Name'], ANTIALIASING, COLORS['WHITE']))

        self.titleText.append(self.titleFont.render("Primal Ring", ANTIALIASING, COLORS['WHITE']))
        # Debug
        if self.debug:
            pass

    # ---------- Methods --------------------------
    def event_handler(self):
        # New Game Screen's events
        if self.newGameFlag:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.flags['Quit'] = True           # This enable the X-window exit button
                    return True
        # Load Game Screen's events
        elif self.loadGameFlag:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.flags['Quit'] = True           # This enable the X-window exit button
                    return True
        # Options Screen's events
        elif self.optionsFlag:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.flags['Quit'] = True           # This enable the X-window exit button
                    return True

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP:
                        self.options.go_up()
                    elif e.key == pygame.K_DOWN:
                        self.options.go_down()
                    if e.key == pygame.K_RIGHT:
                        self.options.sliderFlags[0] = True
                    elif e.key == pygame.K_LEFT:
                        self.options.sliderFlags[1] = True
                    elif e.key == pygame.K_ESCAPE:
                        self.options.soundDict['Cancel'].play()
                        self.optionsFlag = False
                    elif e.key == pygame.K_RETURN:
                        if self.options.optionList[self.options.currentMenu]['Name'] == 'Back to Main Menu':
                            self.options.soundDict['Accept'].play()
                            self.options.save_config()
                            self.config = load_config()
                            self.optionsFlag = False
                        elif self.options.optionList[self.options.currentMenu]['Name'] == 'FullScreen':
                            if self.options.fullScreenFlag:
                                self.options.full_screen_off()
                            else:
                                self.options.full_screen_on()
                elif e.type == pygame.KEYUP:
                    if e.key == pygame.K_RIGHT:
                        self.options.sliderFlags[0] = False
                    elif e.key == pygame.K_LEFT:
                        self.options.sliderFlags[1] = False
        # Title Screen's events
        else:
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
                        # Fading out music (milliseconds)
                        pygame.mixer.music.fadeout(1500)
                # Load Game menu
                elif self.flags['LoadGame'][0]:         # WIP
                    # We enable to access the load screen if we have any saved files
                    if self.flags['LoadGame'][1]:
                        """ Some stuff will happen here, asking for a name and
                            loading all stuff in order to continue."""
                        if not self.initGame:
                            self.initGame = True
                            # Fading out music (milliseconds)
                            pygame.mixer.music.fadeout(1500)
                    else:
                        self.flags['LoadGame'][0] = False
                # Options menu
                elif self.flags['Options']:             # WIP
                    self.options = OptionsScreen(self.screen, self.scrSize, self.font, self.soundDict, self.config)
                    self.optionsFlag = True
                    self.flags['Options'] = False
                # Title menu
                else:
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_UP:
                            self.go_up()
                        elif e.key == pygame.K_DOWN:
                            self.go_down()
                        elif e.key == pygame.K_RETURN:
                            # self.acceptSound.play()
                            self.soundDict['Accept'].play()
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
        # Subscreens
        if self.newGameFlag:
            self.newGame.display()
        elif self.loadGameFlag:
            self.loadGame.display()
        elif self.optionsFlag:
            self.options.display()
        # Debug
        if self.debug:
            pass

        pygame.display.flip()

    def go_down(self):
        # self.selectSound.play()
        self.soundDict['Select'].play()
        if self.currentMenu == len(self.menuList) - 1:
            self.currentMenu = 0
        else:
            self.currentMenu += 1
            if self.menuList[self.currentMenu]['Name'] == 'Load Game' and not self.flags['LoadGame'][1]:
                self.currentMenu += 1

    def go_up(self):
        # self.selectSound.play()
        self.soundDict['Select'].play()
        if self.currentMenu == 0:
            self.currentMenu = len(self.menuList) - 1
        else:
            self.currentMenu -= 1
            if self.menuList[self.currentMenu]['Name'] == 'Load Game' and not self.flags['LoadGame'][1]:
                self.currentMenu -= 1

    def _wiggle(self, cursor_x):
        """
        Cursor simple "live" effect

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

    # Set music theme in this scene
    def set_theme(self):
        pygame.mixer.music.load(self.musicTheme)
        # We start later because we aren't displaying splash screen again
        pygame.mixer.music.play(-1, 13)


class NewGameScreen(_Screen):
    def __init__(self, screen, scr_size, font, debug=False):
        super().__init__(screen, scr_size, debug)
        # Setting the text font for the new game menu
        self.font = font
        # New Game interface text (will include images on next versions)
        self.nGameText = [self.font.render("What's your name, little fella?", ANTIALIASING, COLORS['WHITE'])]


class OptionsScreen(_Screen):
    def __init__(self, screen, scr_size, font, sounds, config, debug=False):
        super().__init__(screen, scr_size, debug)
        # Setting the text font for the new game menu
        self.font = font

        self.soundDict = sounds                        # A sound index for fx effects
        self.config = config                            # A predefined (or previous) configuration set
        # Cursor
        self.cursorSurface = pygame.Surface((170, 25))  # Pause Screen' highlight cursor
        self.cursorSurface.fill(COLORS['GREEN'])
        self.cursorSurface.set_alpha(SURFACE_MID_ALPHA)
        self.optionList = [{'Name': 'FullScreen',
                            'Position': [self.scrSize[0] * 0.2, self.scrSize[1] * 0.2]},
                           {'Name': 'Music Volume',
                            'Position': [self.scrSize[0] * 0.2, self.scrSize[1] * 0.27]},
                           {'Name': 'Effects Volume',
                            'Position': [self.scrSize[0] * 0.2, self.scrSize[1] * 0.34]},
                           {'Name': 'Gallery',
                            'Position': [self.scrSize[0] * 0.2, self.scrSize[1] * 0.41]},
                           {'Name': 'Credits',
                            'Position': [self.scrSize[0] * 0.2, self.scrSize[1] * 0.48]},
                           {'Name': 'Back to Main Menu',
                            'Position': [self.scrSize[0] * 0.2, self.scrSize[1] * 0.55]}]
        self.currentMenu = 0
        # Options interface text (will include images on next versions)
        self.optText = []
        for x in self.optionList:
            self.optText.append(self.font.render(x['Name'], ANTIALIASING, COLORS['WHITE']))

        # Setting initial cursor's position
        self.cursor = self.cursorSurface.get_rect()
        self.cursor.x = self.optionList[0]['Position'][0]
        self.cursor.y = self.optionList[0]['Position'][1] - 0.2
        # Full screen interface
        self.fullScreenTickBox = pygame.Surface((TICKER['Canvas'], TICKER['Canvas']))
        self.fullScreenTickBox.fill(COLORS['WHITE'])
        self.fullScreenTick = pygame.Surface((TICKER['Fill'], TICKER['Fill']))
        self.fullScreenTick.fill(COLORS['GREY'])
        # Volume interface
        self.volumeBar = pygame.Surface((VOLUME_BAR[0], VOLUME_BAR[1]))
        self.volumeBar.fill(COLORS['GREY'])
        self.musicSlider = pygame.Surface((SLIDER[0], SLIDER[1]))
        self.musicSlider.fill(COLORS['GREY'])
        self.fxSlider = pygame.Surface((SLIDER[0], SLIDER[1]))
        self.fxSlider.fill(COLORS['GREY'])
        self.volRatio = 1.0 / (VOLUME_BAR[0] - SLIDER[0])          # Volume map for SLIDER Controls
        self.sliderFlags = [False, False]                          # Flags for continuum slider scrolling
        # Setting GUI controls
        if self.config is not None:
            self.fullScreenFlag = self.config['full_screen']
            pygame.mixer.music.set_volume(self.config['music_volume'])
            self.musicSliderPoint = [self.optionList[1]['Position'][0] + 200
                                     + (self.config['music_volume'] / self.volRatio),
                                     self.optionList[1]['Position'][1]]
            for sound in self.soundDict.values():
                sound.set_volume(self.config['fx_volume'])
            self.fxSliderPoint = [self.optionList[2]['Position'][0] + 200
                                  + (self.config['fx_volume'] / self.volRatio),
                                  self.optionList[2]['Position'][1]]
        else:
            self.fullScreenFlag = FULL_SCREEN
            self.musicSliderPoint = [self.optionList[1]['Position'][0] + 200 + VOLUME_BAR[0] - SLIDER[0],
                                     self.optionList[1]['Position'][1]]
            self.fxSliderPoint = [self.optionList[2]['Position'][0] + 200 + VOLUME_BAR[0] - SLIDER[0],
                                  self.optionList[2]['Position'][1]]
        # Debug text
        if self.debug:
            self.debugText = self.font.render(f'Music slider x = {self.musicSliderPoint[0]}; '
                                              + f'Effects slider x = {self.fxSliderPoint[0]}',
                                              ANTIALIASING, COLORS['WHITE'])

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
            self._slider_to_right()
        elif self.sliderFlags[1]:
            self._slider_to_left()
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
                         [self.optionList[0]['Position'][0] + 200, self.optionList[0]['Position'][1] + 8])
        self.screen.blit(self.fullScreenTick,
                         [self.optionList[0]['Position'][0] + 202, self.optionList[0]['Position'][1] + 10])
        # Volume interface
        self.screen.blit(self.volumeBar,
                         [self.optionList[1]['Position'][0] + 200, self.optionList[1]['Position'][1] + 15])
        self.screen.blit(self.volumeBar,
                         [self.optionList[2]['Position'][0] + 200, self.optionList[2]['Position'][1] + 15])
        self.screen.blit(self.fxSlider, self.fxSliderPoint)
        self.screen.blit(self.musicSlider, self.musicSliderPoint)
        # Option text
        for x in range(len(self.optText)):
            self.screen.blit(self.optText[x], self.optionList[x]['Position'])
        # Debug
        if self.debug:
            self.screen.blit(self.debugText, [100, 50])

    def go_down(self):
        self.soundDict['Select'].play()
        if self.currentMenu == len(self.optionList) - 1:
            self.currentMenu = 0
        else:
            self.currentMenu += 1

    def go_up(self):
        # self.sounds[0].play()
        self.soundDict['Select'].play()
        if self.currentMenu == 0:
            self.currentMenu = len(self.optionList) - 1
        else:
            self.currentMenu -= 1

    def full_screen_on(self):
        if self.optionList[self.currentMenu]['Name'] == 'FullScreen':
            self.soundDict['Accept'].play()
            self.fullScreenFlag = True

    def full_screen_off(self):
        if self.optionList[self.currentMenu]['Name'] == 'FullScreen':
            self.soundDict['Accept'].play()
            self.fullScreenFlag = False

    def save_config(self):
        """
        It takes all config values set into this screen and saves them into a config file
        """
        save_changes(self.fullScreenFlag, pygame.mixer.music.get_volume(), self.soundDict['Select'].get_volume())

    # These two slider functions move the volume controls to left or right, depending on the desired
    # direction. Apparently, they aren't callable if we put the '__' before the name, as if these
    # functions were 'private'.
    def _slider_to_right(self):
        if self.optionList[self.currentMenu]['Name'] == 'Music Volume':
            if self.musicSliderPoint[0] < self.optionList[self.currentMenu]['Position'][0] + 490:
                self.musicSliderPoint[0] += 1
                self._convert_volume(self.musicSliderPoint[0], self.optionList[self.currentMenu]['Name'])
        elif self.optionList[self.currentMenu]['Name'] == 'Effects Volume':
            self.soundDict['Select'].play()
            if self.fxSliderPoint[0] < self.optionList[self.currentMenu]['Position'][0] + 490:
                self.fxSliderPoint[0] += 1
                self._convert_volume(self.fxSliderPoint[0], self.optionList[self.currentMenu]['Name'])

    def _slider_to_left(self):
        if self.optionList[self.currentMenu]['Name'] == 'Music Volume':
            if self.musicSliderPoint[0] > self.optionList[self.currentMenu]['Position'][0] + 200:
                self.musicSliderPoint[0] -= 1
                self._convert_volume(self.musicSliderPoint[0], self.optionList[self.currentMenu]['Name'])
        elif self.optionList[self.currentMenu]['Name'] == 'Effects Volume':
            self.soundDict['Select'].play()
            if self.fxSliderPoint[0] > self.optionList[self.currentMenu]['Position'][0] + 200:
                self.fxSliderPoint[0] -= 1
                self._convert_volume(self.fxSliderPoint[0], self.optionList[self.currentMenu]['Name'])

    def _convert_volume(self, slider_level, option):
        """
        This converts the GUI volume control into real sound values for pygame lib

        :param slider_level:
        :param option:
        :return:
        """
        slider = slider_level - 360
        if option == 'Effects Volume':
            for sound in self.soundDict.values():
                sound.set_volume(slider * self.volRatio)
        elif option == 'Music Volume':
            pygame.mixer.music.set_volume(slider * self.volRatio)
