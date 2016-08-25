#!/usr/bin/env python

import sys
from os import path
# -------------------- CONSTANTS ---------------------
# --------------- Screen dimensions ------------------
SCR_HEIGHT = 600                                            # 600
SCR_WIDTH = 800                                             # 800
# ----------------- Primary colors -------------------
COLORS = {'BLACK': [0x00, 0x00, 0x00],                      # Hex for black
          'WHITE': [0xFF, 0xFF, 0xFF],                      # Hex for white
          'RED': [0xFF, 0x00, 0x00],                        # Hex for red
          'GREEN': [0x00, 0xFF, 0x00],                      # Hex for green
          'BLUE': [0x00, 0x00, 0xFF],                       # Hex for blue
          'ORANGE': [0xFF, 0xFF, 0x00]}                     # Hex for orange
# ---------------------- Stats -----------------------
# --------------------- Player -----------------------
PLAYER_SIZE = 40                                            # X and Y player's size
MAX_FALL_VELOCITY = 10                                      # Player maximum fall velocity
# ---------------------- Floor -----------------------
FLOOR_SIZE = 50                                             # X and Y floor's size
# ---------------------- Items -----------------------
COIN_SIZE = 30                                              # X and Y coin's size
# --------------------- General ----------------------
GRAVITY = 0.35                                              # Gravity for all bodies
ANTIALIASING = True                                         # Smoothing text fonts
DEBUG = True                                                # Reveals hidden statistics and more
ROOT = path.dirname(path.realpath(sys.argv[0]))             # Root game path
