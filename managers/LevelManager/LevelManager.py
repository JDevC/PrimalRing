#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
from pytmx.util_pygame import load_pygame

from managers.LevelManager.LevelDataClass import LevelDataClass
from managers.LevelManager.LevelError import LevelError
from models.Level.DoomValleyLevel import DoomValleyLevel
from models.Level.TheRingLevel import TheRingLevel
from constants import DEBUG, ROOT


class LevelManager:
    def __init__(self):
        self._levels_path = f'{ROOT}/resources/images/LevelMaps'

    def load_level(self, level_data: LevelDataClass):
        try:
            tile_map = load_pygame(f"{self._levels_path}/{level_data.id}/{level_data.id}Level.tmx")
            screen = level_data.screen
            scr_size = level_data.screen_size
            managers = level_data.managers
            player = level_data.player

            if "DoomValley" == level_data.id:
                return DoomValleyLevel(screen, scr_size, managers, player, tile_map, DEBUG)
            elif "TheRing" == level_data.id:
                return TheRingLevel(screen, scr_size, managers, player, tile_map, DEBUG)
        except FileNotFoundError:
            raise LevelError(f"Level was not found -> ID = {level_data.id}")
