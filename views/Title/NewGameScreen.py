#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from views._Screen import _Screen
from constants import ANTIALIASING, COLORS


class NewGameScreen(_Screen):
    def __init__(self, screen, scr_size, sound_manager, font, debug: bool = False):
        super().__init__(screen, scr_size, sound_manager, debug)
        # Setting the text font for the new game menu
        self.font = font
        # New Game interface text (will include images on next versions)
        self.nGameText = [self.font.render("What's your name, little fella?", ANTIALIASING, COLORS['WHITE'])]
