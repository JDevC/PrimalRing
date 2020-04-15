#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from managers.LevelManager.LevelManager import LevelManager
from .ImageManager import ImageManager
from .LocalizationManager import LocalizationManager
from .SoundManager import SoundManager
from dataclasses import dataclass


@dataclass
class ManagerDataClass:
    image: ImageManager = None
    sound: SoundManager = None
    localization: LocalizationManager = LocalizationManager()
    levels: LevelManager = LevelManager()
