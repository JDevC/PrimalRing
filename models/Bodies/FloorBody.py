#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ._BodyBase import _BodyBase
from managers import ImageManager


class FloorBody(_BodyBase):
    def __init__(self, color: [], width: int, height: int, image_manager: ImageManager):
        """ Class for ground floor tiles

        :param color:
        :param width:
        :param height: """
        super().__init__(color, width, height, image_manager)
        self.name = "Floor"
        self.toggle = True

    def react(self, player):
        # X checking
        if self.toggle:
            dist = player.rect.centerx - self.rect.centerx
            if 45 > dist > 0:
                # Moving to the left
                player.rect.left = self.rect.right
            elif -45 < dist < 0:
                # Moving to the right
                player.rect.right = self.rect.left
        # Y checking
        else:
            dist = player.rect.centery - self.rect.centery
            if -45 < dist < 0:
                # Wall under the player
                player.stop_fall()
                player.rect.bottom = self.rect.top
            elif 45 > dist > 0:
                # Wall upon the player
                player.stop_y()
                player.rect.top = self.rect.bottom

        self.toggle = not self.toggle
