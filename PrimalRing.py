#!/usr/bin/env python

# ---------------------- IMPORTS ---------------------
import pygame                                                       # Python libs
from Game6 import Game                                              # Own libs
from Splash import Splash
from Title import TitleScreen
from constants6 import SCR_HEIGHT, SCR_WIDTH, COLORS, FPS, ROOT
""" This is the main game file, where all classes and functions are
    called from. Now it's a tiny file, but we're on developing, so
    it's more than possible that it will grow from now on. """


# ------------------- FUNCTIONS ----------------------
def reset_flags(scene):
    if scene.flags['NewGame']:
        scene.flags['NewGame'] = False
    elif scene.flags['LoadGame'][0]:
        scene.flags['LoadGame'][0] = False

    scene.initGame = False
    scene.reset_opacity()


# MAIN FUNCTION (Here is where all actions run)
def main():
    # Initializing library
    pygame.init()
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    # -------------------- Variables ---------------------
    # Screen attributes
    scr_size = (SCR_WIDTH, SCR_HEIGHT)		                            # Setting and showing a window
    screen = pygame.display.set_mode(scr_size)                          # Getting the main screen
    # screen = pygame.display.set_mode(scr_size, pygame.FULLSCREEN)     # Getting the main screen
    pygame.display.set_caption("Primal Ring")		                    # Setting the screen's title
    icon = pygame.image.load(ROOT + '/images/Coin_Frames/coin.png')     # Setting the game icon
    icon.set_colorkey(COLORS['WHITE'])
    pygame.display.set_icon(icon)
    pygame.mouse.set_visible(False)			                            # We hide the mouse pointer
    # Misc
    done = False					                                    # Loop until the user clicks the close button.
    clock = pygame.time.Clock()			                                # Used to manage how fast the screen updates
    # Scene array
    scene = [Splash(screen, scr_size),                                  # Splash scene instance
             TitleScreen(screen, scr_size)]                             # Title scene instance
    current_scene = scene[0]
    # ---------------- MAIN PROGRAM LOOP -----------------
    while not done:
        # 1st step: Handling events
        switch = current_scene.event_handler()
        # 2nd step: Running game logic
        current_scene.run_logic()
        # 3rd step: Displaying all
        current_scene.display_frame()
        # 4th step: Evaluating scene switching
        if switch:
            if isinstance(current_scene, Splash) and current_scene.endSplash:
                current_scene = scene[0] = scene[1]                     # We 'switch' to the title scene
                del scene[1]                                            # This is for cleaning memory purpose
            elif isinstance(current_scene, TitleScreen):
                if current_scene.flags['NewGame']:
                    reset_flags(current_scene)
                    # We 'switch' to the game scene in a new game
                    scene.append(Game(screen, scr_size, "Name"))
                    current_scene = scene[1]
                elif current_scene.flags['LoadGame'][0]:
                    reset_flags(current_scene)
                    # We 'switch' to the game scene though a loaded game
                    scene.append(Game(screen, scr_size, "Player"))
                    current_scene = scene[1]
                elif current_scene.flags['Quit']:
                    # We exit the game
                    done = True
            elif isinstance(current_scene, Game) and not current_scene.quit_all:
                current_scene = scene[0]
                del scene[1]                                            # This is for cleaning memory purpose
            else:
                done = True
        # --- Limit to 60 frames per second
        clock.tick(FPS)

    pygame.quit()
    
if __name__ == "__main__":
    main()
