#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import randrange
from ._HorizontalLevel import _HorizontalLevel
from models.Bodies.SnowBody import SnowBody
from constants import COLORS


class Level1(_HorizontalLevel):
    def __init__(self, screen, scr_size, managers, player, debug: bool = False):
        super().__init__(screen, scr_size, managers, player, debug)
        # Level data
        self.ID = "Doom Valley"
        self.levelInit = (56, 900)                     # Initial player position's coordinates (50, 900)
        # Level map structure
        self.structure = ["ffffffffffffffffffffffffffffffff",
                          "fc                            cf",
                          "ff  fffffffffffffffffff  c  ffff",
                          "f                      flflf   f",
                          "f  f                    fff    f",
                          "f   ff                         f",
                          "f    f        f                f",
                          "f    ffff   fff                f",
                          "f                              f",
                          "f               p          f c f",
                          "f                          fffff",
                          "f              ffff     P      f",
                          "f   f       f  f               f",
                          "f     c    ff  f     fff ffff  f",
                          "f  f ffff fff       f       f  f",
                          "f c          f            f f  f",
                          "f fc                c     f    f",
                          "f  f              fff     f    f",
                          "f               f              f",
                          "f                       c f  v f",
                          "ffffffffllllfffffffffffffffllflf"]
        # Populating level
        self._fill_level(self.structure)

        # Random location for snow flakes
        for i in range(50):     # 50
            # Snow instance
            flake = SnowBody(COLORS['WHITE'], 2, 2, self.scrSize, self._managers)
            # We create a random placement
            flake.rect.x = randrange(len(self.structure[0]) * 50)
            flake.rect.y = randrange(len(self.structure) * 50)
            # Then we add the flake to the block lists
            flake.firstX = flake.rect.x
            self._weak_group.add(flake)
            self._bodies.add(flake)

        self.musicTheme = 'Doom Valley'
