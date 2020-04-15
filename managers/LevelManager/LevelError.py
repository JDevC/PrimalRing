#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class LevelError(Exception):
    def __init__(self, message):
        super().__init__(message)
