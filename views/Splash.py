# ---------------------- IMPORTS ---------------------
# Python libs
import pygame
# Own libs
from constants import ROOT, COLORS, FPS


class Splash:
    def __init__(self, screen, scr_size, sound_manager, debug=False):
        """ This class holds the initial splash window, in which I put my fictional game dev studio
        and some partners and tools involved into this development.

        :param screen: A reference for the main screen
        :param scr_size:
        :param sound_manager:
        :param debug: Flag for debugging into the game
        """
        # -- Source folders -------------------
        img_dir = f'{ROOT}/resources/images/'
        # -- Attributes -----------------------
        self.screen = screen
        self.debug = debug
        self.fps = FPS
        # Opacity for fade in and fade out effects (254)
        self.opacity = 255
        # Animation flags: Each animation has a couple of boolean flags which control the fade effects
        # between displayed images.
        self.endSplash = False
        self.animations = {'First': [True, False], 'Second': [False, False]}
        # Delay counter for shown images
        self.ticker = 0
        # Setting our studio splash background
        self.background = pygame.image.load(f'{img_dir}Karmical.png').convert()
        self.partners_bg = f'{img_dir}Partners.png'
        # Let's create another surface, which will go on the previous
        self.cover = pygame.Surface(scr_size)
        self.cover.set_alpha(self.opacity)
        # We set and play the main theme
        sound_manager.play_music('Main Theme')

    def event_handler(self):
        """ It handles all events thrown while the splash sequence is running

        :return: True if the player hits the X-window exit button OR the splash sequence is finished; False otherwise
        """
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

    def run_logic(self):
        """ It updates the splash screen at the main control flow """
        # First animation's sequence
        if self.animations['First'][0]:
            if self.opacity >= 0:
                # Fades from black
                self._dec_opacity()
            else:
                # First Fade-in complete
                if self.ticker < self.fps:
                    # It 'delays' a few seconds
                    self.ticker += self.fps / 120
                else:
                    self.ticker = 0                             # Ticker restarts
                    self.cover.fill(COLORS['WHITE'])            # Sets the next fade-out to white
                    self.animations['First'][0] = False
                    self.animations['First'][1] = True
        elif self.animations['First'][1]:
            if self.opacity <= 255:
                # Fades to white
                self._inc_opacity()
            else:
                # First Fade-out complete: It loads the next image
                self.background = pygame.image.load(self.partners_bg).convert()
                self.animations['First'][1] = False
                self.animations['Second'][0] = True
        # Second animation's sequence
        elif self.animations['Second'][0]:
            if self.opacity >= 0:
                # Fades from white
                self._dec_opacity()
            else:
                # Second Fade-in complete
                if self.ticker < self.fps:
                    # It 'delays' a few seconds
                    self.ticker += self.fps / 120
                else:
                    self.ticker = 0                             # Ticker restarts
                    self.cover.fill(COLORS['BLACK'])            # Sets the next fade-out to white
                    self.animations['Second'][0] = False
        else:
            if self.opacity <= 255:
                # Fades to white
                self._inc_opacity()
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

    def _inc_opacity(self):
        self.opacity += 2
        self.cover.set_alpha(self.opacity)

    def _dec_opacity(self):
        self.opacity -= 2
        self.cover.set_alpha(self.opacity)
