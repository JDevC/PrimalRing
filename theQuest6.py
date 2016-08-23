#!/usr/bin/env python

# ---------------------- IMPORTS ---------------------
import pygame                                   # Python libs
import Game6                                    # Own libs
from constants6 import SCR_HEIGHT, SCR_WIDTH
""" This is the main game file, where all classes and functions are
    called from. Now it's a tiny file, but we're on developing, so
    it's more than possible that it will grow from now on. """


# ------------------- FUNCTIONS ----------------------
# MAIN FUNCTION (Here is where all actions run)
def main():
    # Initializing library
    pygame.init()
    # -------------------- Variables ---------------------
    # Screen attributes
    scr_size = (SCR_WIDTH, SCR_HEIGHT)		    # Setting and showing a window
    screen = pygame.display.set_mode(scr_size)  # We get the main screen
    pygame.display.set_caption("The Quest")		# We set the screen's title
    pygame.mouse.set_visible(False)			    # We hide the mouse pointer
    # Game attributes
    # collidersList = pygame.sprite.Group()		# Every collider sprite
    # spritesList = pygame.sprite.Group() 		# This is a list of every sprite. All blocks and the player block as well
    # Misc
    done = False					            # Loop until the user clicks the close button.
    clock = pygame.time.Clock()			        # Used to manage how fast the screen updates
    # We create a Game instance
    game = Game6.Game(screen, scr_size)
    # ---------------- MAIN PROGRAM LOOP -----------------
    while not done:
        # 1st step: Handling events
        done = game.event_handler()
        # 2nd step: Running game logic
        game.run_logic()
        # 3rd step: Displaying all
        game.display_frame()
        # --- Limit to 60 frames per second
        clock.tick(60)
    
    pygame.quit()
    
if __name__ == "__main__":
    main()
