#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ._BodyBase import _BodyBase
from managers import ManagerDataClass
from constants import COLORS


class CoinBody(_BodyBase):
    def __init__(self, color: [], width: int, height: int, managers: ManagerDataClass):
        """ Class for coins

        :param color:
        :param width:
        :param height: """
        super().__init__(color, width, height, managers)
        self.name = "Coin"
        self.image = self._managers.image.load_image("Coin_Frames/coin.png").convert()
        # We set a transparent color for the image
        self.image.set_colorkey(COLORS['WHITE'])

    def react(self, player):
        if player.coins < player.maxWallet:
            player.coins += 1

        self._managers.sound.play_fx('Coin')
