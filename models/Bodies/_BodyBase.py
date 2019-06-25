#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from pygame import Surface
from pygame.sprite import Sprite
from managers import ManagerDataClass


class _BodyBase(Sprite):
    def __init__(self, color: [], width: int, height: int, managers: ManagerDataClass):
        """
        A parent class for all sprites in the game screen, such as the main player, all kind of platforms, enemies
        and so on.

        :param color:
        :param width:
        :param height:
        """
        super().__init__()
        self.name = "Block"
        self._managers = managers
        self.velX = self.velY = 0
        # We create the block's surface
        self.image = Surface([width, height])
        # We fill this 'surface' with a color
        self.image.fill(color)
        # We get the 'collider' box
        self.rect = self.image.get_rect()

        # We get the logger
        self.logger = logging.getLogger(__class__.__name__)

    # ---------- Methods --------------------------
    def react(self, player):
        """ Generates a reaction against the player when he collides this block

        :param player: The player's block
        :return: None """
        pass
