#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Any


@dataclass
class _ScreenHolder:
    screen: Any = None
    flag: bool = False
