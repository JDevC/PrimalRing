#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from pygame.surface import Surface
from managers import ManagerDataClass
from models.Bodies.PlayerBody import PlayerBody


@dataclass
class LevelDataClass:
    id: str
    screen: Surface
    screen_size: tuple
    managers: ManagerDataClass
    player: PlayerBody
