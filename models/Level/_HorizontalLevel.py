#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pygame import image
from pytmx import TiledMap
from ._LevelBase import _LevelBase
from constants import ROOT
from ..Bodies.PlayerBody import PlayerBody


class _HorizontalLevel(_LevelBase):
    def __init__(self, screen, scr_size: tuple, managers, player: PlayerBody, tilemap: TiledMap, debug: bool = False):
        """ 2D Horizontal level's type class

        :param screen:
        :param scr_size: The screen size (Default: 600 * 800)
        :param managers:
        :param player:
        :param debug: """
        super().__init__(screen, scr_size, managers, player, tilemap, debug)
        self.backgroundImg = image.load(f'{ROOT}/resources/images/astro.jpg').convert()
        self.plainLevel = False

    # ---------- Methods --------------------------
    def update(self) -> bool:
        # Update all elements in level
        self._bodies.update()
        # Checks the condition for going out the level
        if self.player.isDead or self.player.coins == 10:
            return True

        self.player.update(self._solid_group, self._weak_group)
        self._scroll()
        if self.debug:
            self._update_player_debug()

        return False
