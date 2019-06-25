#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ._AnimatedBody import _AnimatedBody
from constants import COLORS


class LavaBody(_AnimatedBody):
    def __init__(self, color: list, width: int, height: int, managers):
        """ The floor is this block

        :param color:
        :param width:
        :param height: """
        super().__init__(color, width, height, managers)
        self.name = "Lava"
        # Animation image frames
        self._set_frames('Lava_Frames/Lava', 10)
        self.image = self.imageList[self.imageListIndex]
        # We set a transparent color for the image
        self.image.set_colorkey(COLORS['BLACK'])

    def react(self, player):
        player.life -= 1
        player.velY = -5
        player.rect.y -= 0.1
