#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from pygame import image
from constants import ROOT


class ImageManager:
    LOGGER = logging.getLogger(__name__)

    def __init__(self):
        self._imageDir = f'{ROOT}/resources/images/'

    def load_image(self, image_name):
        return image.load(f'{self._imageDir}/{image_name}').convert()
