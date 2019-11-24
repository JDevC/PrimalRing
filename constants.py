#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from os import path
# ///////////////////// CONSTANTS ////////////////////
# --------------- Screen dimensions ------------------
SCR_HEIGHT = 600                                            # 600
SCR_WIDTH = 800                                             # 800
FULL_SCREEN = False                                         # Full Screen flag
# ------------ Title Screen Attributes ---------------
# Option Attributes
VOLUME_BAR = (300, 5)                                       # X and Y Volume bar's dimensions
SLIDER = (10, 30)                                           # X and Y slider control's dimensions
TICKER = {'Canvas': 16, 'Fill': 12}                         # Tick box dimensions
# ------------ Pause Screen Attributes ---------------
SURFACE_MID_ALPHA = 127                                     # Background's alpha value
# --------------------- BODIES -----------------------
# --------------------- Player -----------------------
PLAYER_SIZE = 40                                            # X and Y player's size
MAX_FALL_VELOCITY = 10                                      # Player maximum fall velocity
# ---------------------- Floor -----------------------
FLOOR_SIZE = 50                                             # X and Y floor's size
# ---------------------- ITEMS -----------------------
COIN_SIZE = 30                                              # X and Y coin's size
LIFE_POWER_UP_SIZE = 40                                     # X and Y life power-up's size
# --------------------- GENERAL ----------------------
# ----------------- Primary colors -------------------
COLORS = {'BLACK': [0x00, 0x00, 0x00],                      # Hex for black
          'GREY': [0x77, 0x77, 0x77],                       # Hex for grey
          'WHITE': [0xFF, 0xFF, 0xFF],                      # Hex for white
          'RED': [0xFF, 0x00, 0x00],                        # Hex for red
          'GREEN': [0x00, 0xFF, 0x00],                      # Hex for green
          'BLUE': [0x00, 0x00, 0xFF],                       # Hex for blue
          'ORANGE': [0xFF, 0xFF, 0x00],
          'DEF_ALPHA': [0xAC, 0x00, 0xBE]}                  # Hex for orange
FPS = 60                                                    # General FPS value
GRAVITY = 0.35                                              # Gravity for all bodies
ANTIALIASING = True                                         # Smoothing text fonts
DEBUG = False                                               # Reveals hidden statistics and more
ROOT = path.dirname(path.realpath(sys.argv[0]))             # Root game path
