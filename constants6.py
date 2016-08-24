#!/usr/bin/env python

import sys
from os import path
# -------------------- CONSTANTS ---------------------
# --------------- Screen dimensions ------------------
SCR_HEIGHT = 600                                            # 600
SCR_WIDTH = 800                                             # 800
# ----------------- Primary colors -------------------
BLACK = [0x00, 0x00, 0x00]                                  # Hex for black
WHITE = [0xFF, 0xFF, 0xFF]                                  # Hex for white
RED = [0xFF, 0x00, 0x00]                                    # Hex for red
GREEN = [0x00, 0xFF, 0x00]                                  # Hex for green
BLUE = [0x00, 0x00, 0xFF]                                   # Hex for blue
# ---------------------- Stats -----------------------
GRAVITY = 0.35                                              # Gravity for all bodies
MAX_FALL_VELOCITY = 10                                      # Player maximum fall velocity
ANTIALIASING = True                                         # Smoothing text fonts
DEBUG = True                                                # Reveals hidden statistics and more
ROOT = path.dirname(path.realpath(sys.argv[0]))             # Root game path
