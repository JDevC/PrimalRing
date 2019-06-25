#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ._BodyBase import _BodyBase


class HoleBody(_BodyBase):
    def __init__(self, color: [], width: int, height: int, managers, img_tag: str = None):
        """ Class for hole tiles

        :param color:
        :param width:
        :param height:
        :param managers: """
        super().__init__(color, width, height, managers)
        self.name = "Hole"
        if img_tag is not None:
            self.image = self._managers.image.load_image(f'plain_hole/{img_tag}.png').convert()

    def react(self, player):
        if player.distance(self.rect) < self.rect.width * 0.75:
            if player.rect.y > self.rect.y:
                player.rect.y -= 2
            elif player.rect.y < self.rect.y:
                player.rect.y += 2
