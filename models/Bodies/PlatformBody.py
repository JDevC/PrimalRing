#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ._BodyBase import _BodyBase


class PlatformBody(_BodyBase):
    def __init__(self, color: [], width: int, height: int, image_manager, init_point, axis: str = 'X'):
        """ This block is so bored about being on the same point that he's going to move

        :param color:
        :param width:
        :param height:
        :param init_point:
        :param axis: """
        super().__init__(color, width, height, image_manager)
        self.name = "Platform"
        self.initPoint = init_point
        self.velX = self.velY = 1
        # Movement limit
        self.maxRun = 50
        self.axis = axis

    # ------------ Methods ------------------------
    def update(self):
        # The current position it's still into the limits
        if self.maxRun >= abs(self.rect.x - self.initPoint[0]) \
                and self.maxRun >= abs(self.rect.y - self.initPoint[1]):
            # It's moving in the X or Y axis?
            if self.axis == 'X':
                self.rect.x += self.velX
            elif self.axis == 'Y':
                self.rect.y += self.velY
        elif self.maxRun < abs(self.rect.x - self.initPoint[0]):
            # We convert the velocity value to its opposite
            self.velX *= -1
            self.rect.x += self.velX
        elif self.maxRun < abs(self.rect.y - self.initPoint[1]):
            # We convert the velocity value to its opposite
            self.velY *= -1
            self.rect.y += self.velY

        # We reset the refresh rating
        # self.refresh = 0

    def react(self, player):
        if player.velY > 0:
            player.stop_fall()
            player.rect.bottom = self.rect.top - 2
        elif player.velY < 0:
            player.stop_y()
            player.rect.top = self.rect.bottom + 2
