#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ._BodyBase import _BodyBase
from constants import COLORS


class LifePowerUpBody(_BodyBase):
    def __init__(self, color: [], width: int, height: int, managers):
        """ Class for life power-ups

        :param color:
        :param width:
        :param height: """
        super().__init__(color, width, height, managers)
        self.name = "LifePowerUp"
        self.image = self._managers.image.load_image('LifePowerUp.png')
        # We set a transparent color for the image
        self.image.set_colorkey(COLORS['WHITE'])

    def react(self, player):
        player.maxLife += 50
        player.life = player.maxLife
