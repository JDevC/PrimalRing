#!/usr/bin/env python

# ---------------------- IMPORTS ---------------------
# Python libs
import pygame
# Own libs
from constants6 import COLORS, SURFACE_MID_ALPHA, ANTIALIASING, ROOT, VOLUME_BAR, KNOB, TICKER
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
        self.sound_dict = {'Select': pygame.mixer.Sound(ROOT + '/sounds/select.wav'),
                           'Accept': pygame.mixer.Sound(ROOT + '/sounds/accept.ogg'),
                           'Cancel': pygame.mixer.Sound(ROOT + '/sounds/cancel.wav')}
        # self.selectSound = pygame.mixer.Sound(ROOT + '/sounds/select.wav')
        # self.acceptSound = pygame.mixer.Sound(ROOT + '/sounds/accept.ogg')
        # New Game elements
        self.newGame = None
        self.newGameFlag = False
        # Load Game elements
        self.loadGame = None
        self.loadGameFlag = False
        # Options elements
        self.options = None
        self.optionsFlag = False
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
        # Setting initial cursor's position
        self.cursor = self.cursorSurface.get_rect()
        self.cursor.x = self.menuList[0]['Position'][0]
        self.cursor.y = self.menuList[0]['Position'][1] - 0.2
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
        if self.newGameFlag:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.flags['Quit'] = True           # This enable the X-window exit button
                    return True
        elif self.loadGameFlag:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.flags['Quit'] = True           # This enable the X-window exit button
                    return True
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
                        self.options.knob_flags[0] = True
                    elif e.key == pygame.K_LEFT:
                        self.options.knob_flags[1] = True
                    elif e.key == pygame.K_ESCAPE:
                        self.options.sound_dict['Cancel'].play()
                        self.optionsFlag = False
                    elif e.key == pygame.K_RETURN:
                        if self.options.optionList[self.options.currentMenu]['Name'] == 'Back to Main Menu':
                            self.options.sound_dict['Accept'].play()
                            self.optionsFlag = False
                        elif self.options.optionList[self.options.currentMenu]['Name'] == 'FullScreen':
                            if self.options.fullscreen_flag:
                                self.options.full_screen_off()
                            else:
                                self.options.full_screen_on()
                elif e.type == pygame.KEYUP:
                    if e.key == pygame.K_RIGHT:
                        self.options.knob_flags[0] = False
                    elif e.key == pygame.K_LEFT:
                        self.options.knob_flags[1] = False
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
                    self.options = OptionsScreen(self.screen, self.scrSize, self.font, self.sound_dict)
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
                            self.sound_dict['Accept'].play()
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
        self.sound_dict['Select'].play()
        if self.currentMenu == len(self.menuList) - 1:
            self.currentMenu = 0
        else:
            self.currentMenu += 1
            if self.menuList[self.currentMenu]['Name'] == 'Load Game' and not self.flags['LoadGame'][1]:
                self.currentMenu += 1

    def go_up(self):
        # self.selectSound.play()
        self.sound_dict['Select'].play()
        if self.currentMenu == 0:
            self.currentMenu = len(self.menuList) - 1
        else:
            self.currentMenu -= 1
            if self.menuList[self.currentMenu]['Name'] == 'Load Game' and not self.flags['LoadGame'][1]:
                self.currentMenu -= 1

    def reset_opacity(self):
        self.opacity = 0
        self.cover.set_alpha(self.opacity)

    def __str__(self):
        return "Title"


class NewGameScreen(object):
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


class OptionsScreen(object):
    # ---------- Constructor ----------------------
    def __init__(self, screen, scr_size, font, sounds, debug=False):
        # -- Attributes -----------------------
        self.debug = debug                              # Flag for debugging into the game
        self.screen = screen                            # A reference for the main screen
        self.scrSize = scr_size
        self.sound_dict = sounds
        # Setting a plane, transparent background
        self.background = pygame.Surface(self.scrSize)
        self.background.fill(COLORS['BLACK'])
        # Setting the text font for the new game menu
        self.font = font
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
        # Fullscreen interface
        self.fullscreen_tickbox = pygame.Surface((TICKER['Canvas'], TICKER['Canvas']))
        self.fullscreen_tickbox.fill(COLORS['WHITE'])
        self.fullscreen_tick = pygame.Surface((TICKER['Fill'], TICKER['Fill']))
        self.fullscreen_tick.fill(COLORS['GREY'])
        self.fullscreen_flag = False
        # Volume interface
        self.volumeBar = pygame.Surface((VOLUME_BAR[0], VOLUME_BAR[1]))
        self.volumeBar.fill(COLORS['GREY'])
        self.musicKnob = pygame.Surface((KNOB[0], KNOB[1]))
        self.musicKnob.fill(COLORS['GREY'])
        self.musicKnob_coords = [self.optionList[1]['Position'][0] + 200, self.optionList[1]['Position'][1]]
        self.fxKnob = pygame.Surface((KNOB[0], KNOB[1]))
        self.fxKnob.fill(COLORS['GREY'])
        self.fxKnob_coords = [self.optionList[2]['Position'][0] + 200, self.optionList[2]['Position'][1]]
        self.vol_ratio = 1.0/(VOLUME_BAR[0] - KNOB[0])      # Volume map for GUI Controls
        self.knob_flags = [False, False]                    # Flags for continuum knob scrolling
        # Debug text
        if self.debug:
            self.debugText = self.font.render("Music knob x = " + str(self.musicKnob_coords[0])
                                              + "\nEffects knob x = " + str(self.fxKnob_coords[0]),
                                              ANTIALIASING, COLORS['WHITE'])

    def update(self):
        # Cursor
        self.cursor.x = self.optionList[self.currentMenu]['Position'][0]
        self.cursor.y = self.optionList[self.currentMenu]['Position'][1]
        if self.fullscreen_flag:
            self.fullscreen_tick.set_alpha(255)
        else:
            self.fullscreen_tick.set_alpha(0)
        # Volume knobs
        if self.knob_flags[0]:
            self.__knob_to_right()
        elif self.knob_flags[1]:
            self.__knob_to_left()
        # Debug text
        if self.debug:
            self.debugText = self.font.render("Music knob x = " + str(self.musicKnob_coords[0])
                                              + "\nEffects knob x = " + str(self.fxKnob_coords[0]),
                                              ANTIALIASING, COLORS['WHITE'])

    def display(self):
        # Background attached to all the window surface
        self.screen.blit(self.background, [0, 0])
        # Cursor
        self.screen.blit(self.cursorSurface, [self.cursor.x, self.cursor.y])
        # Fullscreen interface
        self.screen.blit(self.fullscreen_tickbox,
                         [self.optionList[0]['Position'][0] + 200, self.optionList[0]['Position'][1] + 8])
        self.screen.blit(self.fullscreen_tick,
                         [self.optionList[0]['Position'][0] + 201, self.optionList[0]['Position'][1] + 9])
        # Volume interface
        self.screen.blit(self.volumeBar,
                         [self.optionList[1]['Position'][0] + 200, self.optionList[1]['Position'][1] + 15])
        self.screen.blit(self.volumeBar,
                         [self.optionList[2]['Position'][0] + 200, self.optionList[2]['Position'][1] + 15])
        self.screen.blit(self.fxKnob, self.fxKnob_coords)
        self.screen.blit(self.musicKnob, self.musicKnob_coords)
        # Option text
        for x in range(len(self.optText)):
            self.screen.blit(self.optText[x], self.optionList[x]['Position'])
        # Debug
        if self.debug:
            self.screen.blit(self.debugText, [100, 50])

    def go_down(self):
        # self.sounds[0].play()
        self.sound_dict['Select'].play()
        if self.currentMenu == len(self.optionList) - 1:
            self.currentMenu = 0
        else:
            self.currentMenu += 1

    def go_up(self):
        # self.sounds[0].play()
        self.sound_dict['Select'].play()
        if self.currentMenu == 0:
            self.currentMenu = len(self.optionList) - 1
        else:
            self.currentMenu -= 1

    def full_screen_on(self):
        if self.optionList[self.currentMenu]['Name'] == 'FullScreen':
            # self.sounds[1].play()
            self.sound_dict['Accept'].play()
            self.fullscreen_flag = True

    def full_screen_off(self):
        if self.optionList[self.currentMenu]['Name'] == 'FullScreen':
            # self.sounds[1].play()
            self.sound_dict['Accept'].play()
            self.fullscreen_flag = False

    # These two knob functions move the volume controls to left or right, depending on the desired
    # direction. Apparently, they aren't callable if we put the '__' before the name, as if these
    # functions were 'private'.
    def __knob_to_right(self):
        self.sound_dict['Select'].play()
        if self.optionList[self.currentMenu]['Name'] == 'Music Volume':
            if self.musicKnob_coords[0] < self.optionList[self.currentMenu]['Position'][0] + 490:
                self.musicKnob_coords[0] += 1
                self.__convert_volume(self.musicKnob_coords[0])
        elif self.optionList[self.currentMenu]['Name'] == 'Effects Volume':
            if self.fxKnob_coords[0] < self.optionList[self.currentMenu]['Position'][0] + 490:
                self.fxKnob_coords[0] += 1
                self.__convert_volume(self.fxKnob_coords[0])

    def __knob_to_left(self):
        self.sound_dict['Select'].play()
        if self.optionList[self.currentMenu]['Name'] == 'Music Volume':
            if self.musicKnob_coords[0] > self.optionList[self.currentMenu]['Position'][0] + 200:
                self.musicKnob_coords[0] -= 1
                self.__convert_volume(self.musicKnob_coords[0])
        elif self.optionList[self.currentMenu]['Name'] == 'Effects Volume':
            if self.fxKnob_coords[0] > self.optionList[self.currentMenu]['Position'][0] + 200:
                self.fxKnob_coords[0] -= 1
                self.__convert_volume(self.fxKnob_coords[0])

    # This function converts the GUI volume control into real sound values for pygame lib
    def __convert_volume(self, knob_level):

        knob = knob_level - 360
        for sound in self.sound_dict.values():
            sound.set_volume(knob * self.vol_ratio)
        # print("Knob level -> " + str(knob) + "; Sound -> " + str(self.sounds[0].get_volume()))
