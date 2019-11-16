#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ._BodyBase import _BodyBase
from constants import COLORS, FPS
from managers import ManagerDataClass


class _AnimatedBody(_BodyBase):
    def __init__(self, color: [], width: int, height: int, managers: ManagerDataClass):
        """ It's alive! Class for animated blocks, with some additions (Animated is for textures, not for changing its
        position (at least for now...))

        :param color:
        :param width:
        :param height:
        :param managers:
        """
        super().__init__(color, width, height, managers)
        self.name = "AnimatedBlock"
        # Tile container and pointer on animation
        self.imageList = []
        self.imageListIndex = 0
        # Frame Rate
        self.fps = FPS
        # Delay for frame animations
        self.refresh = 0

    # ---------- Public Methods --------------------------
    def update(self) -> None:
        # We configure the refresh rating here
        if self.refresh < self.fps:
            self.refresh += self.fps / 2
        else:
            # We switch the current tile to next in a concrete sequence
            if self.imageListIndex < len(self.imageList) - 1:
                self.imageListIndex += 1
            else:
                self.imageListIndex = 0
            self.image = self.imageList[self.imageListIndex]
            self.image.set_colorkey(COLORS['BLACK'])
            # We reset the refresh state
            self.refresh = 0

    # ---------- Internal Methods --------------------------
    def _set_frames(self, origin: str, quantity: int = 1):
        """ Loads all tiles incoming from a specified folder

        :param origin: The tile folder and image name in the format '{folder}/{image}'
        :param quantity: Count of tiles for the animation
        :return: None """
        self.imageList = [self._managers.image.load_image(f'{origin}{i + 1}.png') for i in range(quantity)]
