#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pygame import image
from ._BodyBase import _BodyBase
from managers import SoundManager, ImageManager
from constants import COLORS, ROOT


class CoinBody(_BodyBase):
    def __init__(self, color: [], width: int, height: int, sound_manager: SoundManager, image_manager: ImageManager):
        """ Class for coins

        :param color:
        :param width:
        :param height: """
        super().__init__(color, width, height, image_manager)
        self.name = "Coin"
        self.image = image.load(f'{ROOT}/resources/images/Coin_Frames/coin.png').convert()
        # We set a transparent color for the image
        self.image.set_colorkey(COLORS['WHITE'])
        # We get the sound manager reference
        self.soundMan = sound_manager

    def react(self, player):
        if player.coins < player.maxWallet:
            player.coins += 1

        self.soundMan.play_fx('Coin')
