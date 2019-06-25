#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
from views._Screen import _Screen
from SaveGame import SaveGame
from constants import COLORS, SURFACE_MID_ALPHA, ANTIALIASING, VOLUME_BAR, SLIDER, TICKER, FULL_SCREEN


class OptionsScreen(_Screen):
    def __init__(self, screen, scr_size, managers, config, font, debug: bool = False):
        super().__init__(screen, scr_size, managers, debug)
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
            self._managers.sound.set_music_vol(config['music_volume'])
            self.musicSliderPoint = [self.optionList[1]['Position'][0] + 220 + (config['music_volume'] / self.volRatio),
                                     self.optionList[1]['Position'][1]]
            self._managers.sound.set_fx_vol(config['fx_volume'])
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
    def _init_ui_text(self, font, refresh: bool = False):
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

    @staticmethod
    def _init_cursor(def_option: []):
        cursor_surface = pygame.Surface((170, 25))
        cursor_surface.fill(COLORS['GREEN'])
        cursor_surface.set_alpha(SURFACE_MID_ALPHA)
        # Setting initial cursor's position
        cursor = cursor_surface.get_rect()
        cursor.x = def_option['Position'][0]
        cursor.y = def_option['Position'][1] - 0.2

        return cursor_surface, cursor

    # ---------------------------- MAIN FLOW ----------------------------
    def event_handler(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.quit_all = True
                return True

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    self._go_up()
                elif e.key == pygame.K_DOWN:
                    self._go_down()

                if e.key == pygame.K_RIGHT:
                    self._change_language(self.langUtils.next_index, self.currentLang, 0)
                elif e.key == pygame.K_LEFT:
                    self._change_language(self.langUtils.prev_index, self.currentLang, 1)
                elif e.key == pygame.K_ESCAPE:
                    self._managers.sound.play_fx('Cancel')
                    return True
                elif e.key == pygame.K_RETURN:
                    if self.optionList[self.currentMenu]["ID"] == "Back":
                        self._managers.sound.play_fx('Accept')
                        self._save_config()
                        return True
                    elif self.optionList[self.currentMenu]["ID"] == "FullScreen":
                        self._switch_full_screen(not self.fullScreenFlag)

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
            self._managers.localization.set_lang(self.langUtils.get_id(self.currentLang))

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

    # ----------------------------- METHODS -----------------------------
    def _go_down(self):
        self._managers.sound.play_fx('Select')
        self.currentMenu = 0 if self.currentMenu == len(self.optionList) - 1 else self.currentMenu + 1

    def _go_up(self):
        self._managers.sound.play_fx('Select')
        self.currentMenu = len(self.optionList) - 1 if self.currentMenu == 0 else self.currentMenu - 1

    def _switch_full_screen(self, full_screen: bool = False):
        if self.optionList[self.currentMenu]["ID"] == "FullScreen":
            self._managers.sound.play_fx('Accept')
            self.fullScreenFlag = full_screen

    def _save_config(self):
        """ It takes all config values set into this screen and saves them into a config file """
        SaveGame.save_config(self.fullScreenFlag, self._managers.sound.get_music_vol(),
                             self._managers.sound.get_fx_vol(), self.langUtils.get_id(self.currentLang))

    # These two slider functions move the volume controls to left or right, depending on the desired
    # direction.
    def _slider_to_right(self, slider_opt: {}) -> None:
        if slider_opt["ID"] == "MusicVol":
            if self.musicSliderPoint[0] < slider_opt['Position'][0] + 510:
                self.musicSliderPoint[0] += 1
                self._convert_volume(self.musicSliderPoint[0], slider_opt["ID"])
        elif slider_opt["ID"] == "EffectsVol":
            self._managers.sound.play_fx('Select')
            if self.fxSliderPoint[0] < slider_opt['Position'][0] + 510:
                self.fxSliderPoint[0] += 1
                self._convert_volume(self.fxSliderPoint[0], slider_opt["ID"])

    def _slider_to_left(self, slider_opt: {}) -> None:
        if slider_opt["ID"] == "MusicVol":
            if self.musicSliderPoint[0] > slider_opt['Position'][0] + 220:
                self.musicSliderPoint[0] -= 1
                self._convert_volume(self.musicSliderPoint[0], slider_opt["ID"])
        elif slider_opt["ID"] == "EffectsVol":
            self._managers.sound.play_fx('Select')
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
            self._managers.sound.set_fx_vol(slider * self.volRatio)
        elif option == "MusicVol":
            self._managers.sound.set_music_vol(slider * self.volRatio)

    def _change_language(self, callback, current_lang, flag_index: int):
        if self.optionList[self.currentMenu]["ID"] == "Language":
            self.currentLang = callback(current_lang)
        else:
            self.sliderFlags[flag_index] = True

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
