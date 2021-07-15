#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pytmx import TiledMap

from models.Bodies.PlayerBody import PlayerBody
from models.Level._PlainLevel import _PlainLevel


class TheRingLevel(_PlainLevel):
    def __init__(self, screen, scr_size: tuple, managers, player: PlayerBody, tilemap: TiledMap, debug: bool = False):
        """

        :param screen:
        :param scr_size: The screen size (Default: 600 * 800)
        :param managers:
        :param player:
        :param tilemap:
        :param debug:
        """
        super().__init__(screen, scr_size, managers, player, tilemap, debug)
        # Level data
        self.ID = "TheRing"
        self.levelInit = (150, 850)  # Initial player position's coordinates (50, 500)
        # Populating level
        self._fill_tmx_level(self._tilemap)
        self.musicTheme = 'The RING'
