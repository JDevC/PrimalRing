#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ._LevelBase import _LevelBase


class _PlainLevel(_LevelBase):
    def __init__(self, screen, scr_size, managers, player, debug: bool = False):
        """ 2D Plain level's type class

        :param screen:
        :param scr_size:
        :param sound_manager:
        :param player:
        :param debug: """
        super().__init__(screen, scr_size, managers, player, debug)
        self.plainLevel = True

    # ---------- Methods --------------------------
    def update(self):
        # Update all elements in level
        self._bodies.update()
        self.player.update(self._solid_group, self._weak_group)
        self._scroll()
        if self.debug:
            self._update_player_debug()

        return False
