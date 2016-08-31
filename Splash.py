# ---------------------- IMPORTS ---------------------
# Python libs
from pygame import Surface, image, display
import time
# Own libs
from constants6 import ROOT, FPS


class Splash(object):
    # Globals
    root = ROOT
    fps = FPS

    # ---------- Constructor ----------------------
    def __init__(self, screen, scr_size, debug=False):
        # -- Attributes -----------------------
        self.debug = debug                                      # Flag for debugging into the game
        self.screen = screen                                    # A reference for the main screen
        self.opacity = 254                                      # Opacity for fade in and fade out effects (255)
        self.refresh = 0                                        # Delay for fading effects
        self.init_animation = True
        # Setting our studio splash background
        self.background = image.load(self.root + '/images/Karmical.png').convert()
        # Let's create another surface, which will go on the previous
        self.cover = Surface(scr_size)
        self.cover.set_alpha(self.opacity)

    def action(self):
        # Checks refresh rate
        while self.opacity != 255:
            if self.init_animation:
                self.opacity -= 1
            else:
                self.opacity += 1

            self.cover.set_alpha(self.opacity)
            if self.opacity == 0:
                self.init_animation = False
                time.sleep(4)
            # We reset the refresh state
            self.refresh = 0
            self.display()

        time.sleep(1)

    def display(self):
        self.screen.blit(self.background, [0, 0])
        self.screen.blit(self.cover, [0, 0])
        if self.debug:
            pass

        display.flip()
