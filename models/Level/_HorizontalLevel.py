#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pygame import image
from ._LevelBase import _LevelBase
from constants import ROOT


class _HorizontalLevel(_LevelBase):
    def __init__(self, screen, scr_size, managers, player, debug: bool = False):
        """ 2D Horizontal level's type class

        :param screen:
        :param scr_size:
        :param sound_manager:
        :param player:
        :param debug: """
        super().__init__(screen, scr_size, managers, player, debug)
        self.backgroundImg = image.load(f'{ROOT}/resources/images/astro.jpg').convert()
        self.plainLevel = False

    # ---------- Methods --------------------------
    def update(self) -> bool:
        # Update all elements in level
        self._bodies.update()
        # Checks the condition for going out the level
        if self.player.isDead:
            return True
        elif self.player.coins < 10:
            self.player.update(self._solid_group, self._weak_group)
            self._scroll()
            if self.debug:
                self._update_player_debug()

            return False
        else:
            return True
