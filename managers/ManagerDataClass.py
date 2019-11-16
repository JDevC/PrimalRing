#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .ImageManager import ImageManager
from .LocalizationManager import LocalizationManager
from .SoundManager import SoundManager
from dataclasses import dataclass


@dataclass
class ManagerDataClass:
    image: ImageManager = None
    localization: LocalizationManager = None
    sound: SoundManager = None
