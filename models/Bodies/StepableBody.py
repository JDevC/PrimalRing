#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ._BodyBase import _BodyBase
from managers import ImageManager


class StepableBody(_BodyBase):
    def __init__(self, color: [], width: int, height: int, image_manager: ImageManager):
        """ Class for ground floor tiles

        :param color:
        :param width:
        :param height: """
        super().__init__(color, width, height, image_manager)
        self.name = "Stepable"
        self.toggle = True
