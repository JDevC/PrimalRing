#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pytmx import TiledMap
from models.Level._PlainLevel import _PlainLevel


class Level2(_PlainLevel):
    def __init__(self, screen, src_size, managers, player, tilemap: TiledMap, debug: bool = False):
        super().__init__(screen, src_size, managers, player, tilemap, debug)
        # Level data
        self.ID = "TheRing"
        self.levelInit = (150, 850)  # Initial player position's coordinates (50, 500)
        # Populating level
        self._fill_tmx_level(self._tilemap)
        self.musicTheme = 'The RING'
