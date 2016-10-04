# ---------------------- IMPORTS ---------------------
# Python libs
import pygame
# Own libs
from constants6 import ROOT, COLORS, FPS
'''
This class holds the initial splash window, in which I put my fictional game dev studio
and some partners and tools involved into this development.
'''


class Splash(object):
    # Globals
    root = ROOT
    fps = FPS

    # ---------- Constructor ----------------------
    def __init__(self, screen, scr_size, debug=False):
        # -- Attributes -----------------------
        self.debug = debug                                      # Flag for debugging into the game
        self.screen = screen                                    # A reference for the main screen
        self.opacity = 255                                      # Opacity for fade in and fade out effects (254)
        # Animation flags: Each animation has a couple of boolean flags which control the fade effects
        # between displayed images.
        self.endSplash = False
        self.animations = {'First': [True, False], 'Second': [False, False]}
        self.ticker = 0                                         # Delay counter for shown images
        # Setting our studio splash background
        self.background = pygame.image.load(self.root + '/images/Karmical.png').convert()
        # Let's create another surface, which will go on the previous
        self.cover = pygame.Surface(scr_size)
        self.cover.set_alpha(self.opacity)

    def event_handler(self):
        # This could seem nonsense, but the fact is the game goes into a wtf-crash-non-responding
        # state if we don't provide an event-handling process at this point. If you think there's a better
        # way to fix this, please let me know and you'll become my hero
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return True                         # This enable the X-window exit button
            if e.type == pygame.KEYDOWN:
                # This is given to accelerate the splash animations. Still don't know if let it
                # 'as is' for release version, or deleting it
                if e.key == pygame.K_SPACE:
                    if self.animations['First'][0]:
                        self.cover.fill(COLORS['WHITE'])
                        self.animations['First'][0] = False
                        self.animations['First'][1] = True
                    elif self.animations['Second'][0]:
                        self.cover.fill(COLORS['BLACK'])
                        self.animations['Second'][0] = False

        return self.animations['Second'][1]

    # It updates the splash screen at the main control flow
    def run_logic(self):
        # First animation's sequence
        if self.animations['First'][0]:
            if self.opacity >= 0:
                # Fades from black
                self.dec_opacity()
            else:
                # First Fade-in complete
                if self.ticker < self.fps:
                    # It 'delays' a few seconds
                    self.ticker += self.fps / 120
                else:
                    self.ticker = 0                             # Restarts the ticker
                    self.cover.fill(COLORS['WHITE'])            # Sets the next fade-out to white
                    self.animations['First'][0] = False
                    self.animations['First'][1] = True
        elif self.animations['First'][1]:
            if self.opacity <= 255:
                # Fades to white
                self.inc_opacity()
            else:
                # First Fade-out complete: It loads the next image
                self.background = pygame.image.load(self.root + '/images/Partners.png').convert()
                self.animations['First'][1] = False
                self.animations['Second'][0] = True
        # Second animation's sequence
        elif self.animations['Second'][0]:
            if self.opacity >= 0:
                # Fades from white
                self.dec_opacity()
            else:
                # Second Fade-in complete
                if self.ticker < self.fps:
                    # It 'delays' a few seconds
                    self.ticker += self.fps / 120
                else:
                    self.ticker = 0                             # Restarts the ticker
                    self.cover.fill(COLORS['BLACK'])  # Sets the next fade-out to white
                    self.animations['Second'][0] = False
        else:
            if self.opacity <= 255:
                # Fades to white
                self.inc_opacity()
            else:
                # Second Fade-out complete: Time to enter the game!
                self.endSplash = True
                self.animations['Second'][1] = True

    def display_frame(self):
        self.screen.blit(self.background, [0, 0])
        self.screen.blit(self.cover, [0, 0])
        if self.debug:
            pass

        pygame.display.flip()

    def inc_opacity(self):
        self.opacity += 2
        self.cover.set_alpha(self.opacity)

    def dec_opacity(self):
        self.opacity -= 2
        self.cover.set_alpha(self.opacity)
