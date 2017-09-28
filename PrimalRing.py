#!/usr/bin/env python3

# ---------------------- IMPORTS ---------------------
# Python libs
import pygame
# Game libs
from views.Title import TitleScreen
from views.Splash import Splash
from Game6 import Game
from SaveGame import load_config
from constants6 import SCR_HEIGHT, SCR_WIDTH, COLORS, FPS, ROOT, FULL_SCREEN

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


def screen_set(screen_size, full_screen):
    if full_screen:
        screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
        # This delay helps to start displaying all at proper time
        pygame.time.wait(3000)
    else:
        screen = pygame.display.set_mode(screen_size)

    return screen


def configuration_preset(config, screen_size):
    """
    Defines some initial configuration parameters

    :param config: List with predefined configuration parameters
    :param screen_size: Initial dimensions
    :return: A display instance
    """
    if config is not None:
        screen = screen_set(screen_size, config['full_screen'])
        pygame.mixer.music.set_volume(config['music_volume'])
    else:
        screen = screen_set(screen_size, FULL_SCREEN)

    return screen


# MAIN FUNCTION (Here is where all actions run)
def main():
    # Initializing pygame and pre-initializing sound module
    pygame.init()
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    # -------------------- Variables ---------------------
    # Setting game window's size
    scr_size = (SCR_WIDTH, SCR_HEIGHT)
    ''' Here, we set many configuration properties, depending on our
        config file or a group of defined values in case the config
        file is missing '''
    config = load_config()
    screen = configuration_preset(config, scr_size)
    # Setting the screen's title, game icon and hiding the mouse
    pygame.display.set_caption("Primal Ring")
    icon = pygame.image.load(f'{ROOT}/resources/images/Coin_Frames/coin.png')
    icon.set_colorkey(COLORS['WHITE'])
    pygame.display.set_icon(icon)
    pygame.mouse.set_visible(False)
    # Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # Scene pointer
    current_scene = Splash(screen, scr_size)
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
                current_scene = TitleScreen(screen, scr_size, config)
            elif isinstance(current_scene, TitleScreen):
                if current_scene.flags['NewGame']:
                    reset_flags(current_scene)
                    # We 'switch' to the game scene in a new game
                    current_scene = Game(screen, scr_size)
                elif current_scene.flags['LoadGame'][0]:
                    reset_flags(current_scene)
                    # We 'switch' to the game scene through a loaded game
                    current_scene = Game(screen, scr_size, "Player")
                elif current_scene.flags['Quit']:
                    # We exit the game
                    done = True
            elif isinstance(current_scene, Game) and not current_scene.quit_all:
                current_scene = TitleScreen(screen, scr_size, config)
                current_scene.set_theme()
            else:
                done = True
        # --- Limit to 60 frames per second
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
