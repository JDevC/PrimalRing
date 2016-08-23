#!/usr/bin/env python

import sys
from os import path
# ---------------- GLOBAL ATTRIBUTES -----------------
# -------------------- Constants ---------------------
SCR_HEIGHT = 600                                    # 600
SCR_WIDTH = 800                                     # 800
BLACK = [0x00, 0x00, 0x00]                          # Hex for black
WHITE = [0xFF, 0xFF, 0xFF]                          # Hex for white
RED = [0xFF, 0x00, 0x00]                            # Hex for red
GREEN = [0x00, 0xFF, 0x00]                          # Hex for green
BLUE = [0x00, 0x00, 0xFF]                           # Hex for blue
ROOT = path.dirname(path.realpath(sys.argv[0]))     # Root game path
