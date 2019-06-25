#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ._BodyBase import _BodyBase


class SnowBody(_BodyBase):
    def __init__(self, color: [], width: int, height: int, screen_size: tuple, managers):
        super().__init__(color, width, height, managers)
        self.name = "Snow"
        self.screen_size = screen_size
        self.firstX = 0
        self.acc = 5

    # ---------- Methods --------------------------
    def update(self):
        self.rect.y += 1
        if self.rect.y > self.screen_size[1]:
            self.rect.y = -1

    def react(self, player):
        player.life -= 1

    # Function for falling snow flakes
    def bounce(self):
        if self.rect.x == self.firstX:
            pass
        else:
            pass
