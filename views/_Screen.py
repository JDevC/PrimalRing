#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
from constants import COLORS


class _Screen:
    def __init__(self, screen, scr_size, sound_manager, debug: bool = False):
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

    def event_handler(self):
        pass

    def update(self):
        pass

    def display(self):
        pass
