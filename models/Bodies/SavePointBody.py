#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ._AnimatedBody import _AnimatedBody
from constants import COLORS


class SavePointBody(_AnimatedBody):
    def __init__(self, color: [], width: int, height: int, image_manager):
        """ Class for saving point tiles

        :param color:
        :param width:
        :param height: """
        super().__init__(color, width, height, image_manager)
        self.name = "SavePoint"
        # Animation image frames
        self._set_frames('SP_Frames/save_point', 12)
        self.image = self.imageList[self.imageListIndex]
        # We set a transparent color for the image
        self.image.set_colorkey(COLORS['BLACK'])

    def react(self, player):
        player.saveFlag = player.distance(self.rect) < self.rect.width / 2
