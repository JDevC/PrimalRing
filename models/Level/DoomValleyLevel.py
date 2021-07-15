#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import randrange
from pytmx import TiledMap
from ._HorizontalLevel import _HorizontalLevel
from models.Bodies.SnowBody import SnowBody
from constants import COLORS
from ..Bodies.PlayerBody import PlayerBody


class DoomValleyLevel(_HorizontalLevel):
    def __init__(self, screen, scr_size, managers, player: PlayerBody, tilemap: TiledMap, debug: bool = False):
        super().__init__(screen, scr_size, managers, player, tilemap, debug)
        # Level data
        self.ID = "DoomValley"
        self.next_id = "TheRing"
        self.levelInit = (56, 900)                     # Initial player position's coordinates (50, 900)
        # Populating level
        self._fill_tmx_level(self._tilemap)

        # Random location for snow flakes
        for i in range(50):     # 50
            # Snow instance
            flake = SnowBody(COLORS['WHITE'], 2, 2, self.scrSize, self._managers)
            # We create a random placement
            flake.rect.x = randrange(32 * 50)
            flake.rect.y = randrange(21 * 50)
            # Then we add the flake to the block lists
            flake.firstX = flake.rect.x
            self._weak_group.add(flake)
            self._bodies.add(flake)

        self.musicTheme = 'Doom Valley'
