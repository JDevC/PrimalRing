#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from models.Level._PlainLevel import _PlainLevel


# All levels must inherit from 'HorizontalLevel' or 'Plain Level'
class Level2(_PlainLevel):
    def __init__(self, screen, src_size, managers, player, debug: bool = False):
        super().__init__(screen, src_size, managers, player, debug)
        # Level data
        self.ID = "The RING"
        self.levelInit = (150, 850)  # Initial player position's coordinates (50, 500)
        # -- Attributes -----------------------
        self.structure = ["ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                          "fffffff  ffff ff               ffhhchhchhchhchhff c        cffff",
                          "ff  fff  fff  ff               ffhhchhchhchhchhffcfff       cfff",
                          "ff c cf  fc   ff                               ff fhh        cff",
                          "ff  hhf  fhh                                                  cf",
                          "ff  fff  fff            hhhhhhhffhhhhhh                        f",
                          "ff  fff  fff  ff        hhhhhhhffhhhhhh  hhhhhhff fhh      hhf f",
                          "f             ff        hhhhhhffffhhhhh  hhhhhhffcfff      fffcf",
                          "fffffff  fffffff        hhhhhffffffhhhh  hhhhhhff c          c f",
                          "f       fc    ffffffff  fffffffffffffff  ffffffffffffff  fffffff",
                          "f fffff fc    ffffffff  fffffffffffffff  ffffffffffffff  fffffff",
                          "fcfhf h     f ff        hhhhhffffffhhhh  hhhhhhff              f",
                          "fcf        ff ff        hhhhhhffffhhhhh  hhhhhhff fff      fff f",
                          "fcff    f fff ff        hhhhhhhffhhhhhh  hhhhhhff fhh  s   hhf f",
                          "fcf   h  c              hhhhhhhffhhhhhh                        f",
                          "fcff  h                                                    hhhhf",
                          "ff    h    s  ff                               ff fhh      hhhff",
                          "fff   f       ff               ffhhchhchhchhchhff fff      hhfff",
                          "ffff  f       ff               ffhhchhchhchhchhff          hffff",
                          "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"]
        # 64 x 20
        # Populating level
        self._fill_level(self.structure)
        self.structure.clear()
        self.musicTheme = 'The RING'
