#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
from pygame.surface import Surface

from ._StageEnum import _StageEnum
from constants import COLORS, FPS


class SplashScreen:
    def __init__(self, screen: Surface, scr_size: tuple, managers, debug: bool = False):
        """ This class holds the initial splash window, in which I put my fictional game dev studio
        and some partners and tools involved into this development.

        :param screen: A reference for the main screen
        :param scr_size: Initial dimensions
        :param managers:
        :param debug: Flag for debugging into the game
        """
        self.screen = screen
        self.debug = debug
        self.fps = FPS
        self._managers = managers
        # Opacity for fade in and fade out effects (254)
        self.opacity = 255
        # Animation flags
        self.endSplash = False
        self._currentStage = _StageEnum.FIRST
        # Delay counter for shown images
        self.ticker = 0
        # Setting our studio splash background
        self.background = managers.image.load_image(f'Karmical.png')
        self.partners_bg = f'Partners.png'
        # Let's create another surface, which will go on the previous
        self.cover = pygame.Surface(scr_size)
        self.cover.set_alpha(self.opacity)
        # We set and play the main theme
        self._managers.sound.play_music('Main Theme')

    def event_handler(self) -> bool:
        """ It handles all events thrown while the splash sequence is running

        :return: True if the player hits the X-window exit button OR the splash sequence is finished; False otherwise
        """
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return True                         # This enable the X-window exit button
            if e.type == pygame.KEYDOWN:
                # This is given to accelerate the splash animations. Still don't know if let it
                # 'as is' for release version, or deleting it
                if e.key == pygame.K_SPACE:
                    if self._currentStage == _StageEnum.FIRST:
                        self._start_fade_out('WHITE', _StageEnum.SECOND)
                    elif self._currentStage == _StageEnum.THIRD:
                        self._start_fade_out('BLACK', _StageEnum.NONE)

        return self._currentStage == _StageEnum.FOURTH

    def run_logic(self):
        """ It updates the splash screen at the main control flow """
        if self._currentStage == _StageEnum.FIRST:
            self._fade_in(self._start_fade_out, 'WHITE', _StageEnum.SECOND)
        elif self._currentStage == _StageEnum.SECOND:
            self._fade_out(self._first_fade_out_complete)
        elif self._currentStage == _StageEnum.THIRD:
            self._fade_in(self._start_fade_out, 'BLACK', _StageEnum.NONE)
        else:
            self._fade_out(self._second_fade_out_complete)

    def display_frame(self):
        self.screen.blit(self.background, [0, 0])
        self.screen.blit(self.cover, [0, 0])
        if self.debug:
            pass

        pygame.display.flip()

    # -------- Internal Methods --------
    def _fade_in(self, callback, color_tag: str, stage_value):
        if self.opacity >= 0:
            self._change_opacity(-2)
        else:
            self._hold(callback, color_tag, stage_value)

    def _hold(self, callback, color_tag: str, stage_value):
        if self.ticker < self.fps:
            self.ticker += self.fps / 120
        else:
            self.ticker = 0
            callback(color_tag, stage_value)

    def _fade_out(self, callback):
        if self.opacity <= 255:
            self._change_opacity(2)
        else:
            callback()

    def _start_fade_out(self, color_tag, stage_value):
        self.cover.fill(COLORS[color_tag])
        self._currentStage = stage_value

    def _first_fade_out_complete(self):
        self.background = self._managers.image.load_image(self.partners_bg)
        self._currentStage = _StageEnum.THIRD

    def _second_fade_out_complete(self):
        self.endSplash = True
        self._currentStage = _StageEnum.FOURTH

    def _change_opacity(self, value):
        self.opacity += value
        self.cover.set_alpha(self.opacity)
