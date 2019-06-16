#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ._BodyBase import _BodyBase


class _EnemyBody(_BodyBase):
    def __init__(self, color: [], width: int, height: int):
        """ Evil army! This class is for all enemy objects (It will extend from _AnimatedBlock in a future; Still lacks
        tiles)

        :param color:
        :param width:
        :param height: """
        super().__init__(color, width, height)
        self.life = 0                           # Enemy's life count
        self.isDead = False                     # Enemy's state
        self.firstX = 0
