#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
import logging
from views.Title.TitleScreen import TitleScreen
from views.Splash.SplashScreen import SplashScreen
from managers import managers
from managers.ImageManager import ImageManager
from managers.SoundManager import SoundManager
from Game import Game
from SaveGame import SaveGame
from constants import SCR_HEIGHT, SCR_WIDTH, COLORS, FPS, FULL_SCREEN

""" This is the main game file, where all classes and functions are
    called from. Now it's a tiny file, but we're on developing, so
    it's more than possible that it will grow from now on. """


# ------------------- FUNCTIONS ----------------------
def reset_flags(scene: TitleScreen):
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


def configuration_preset(config, screen_size, managers):
    """ Defines some initial configuration parameters

    :param config: List with predefined configuration parameters
    :param screen_size: Initial dimensions
    :param managers: The game manager container
    :return: A display instance """
    if config is None:
        full_screen_val = FULL_SCREEN
        managers.localization.set_lang("en")
    else:
        full_screen_val = config['full_screen']
        managers.sound.set_music_vol(config['music_volume'])
        managers.sound.set_fx_vol(config['fx_volume'])
        managers.localization.set_lang(config['lang'])

    return screen_set(screen_size, full_screen_val)


def set_game_window(img_manager):
    pygame.display.set_caption("Primal Ring")
    icon = img_manager.load_image('Coin_Frames/coin.png')
    icon.set_colorkey(COLORS['WHITE'])
    pygame.display.set_icon(icon)
    pygame.mouse.set_visible(False)


def main():
    """ Here is where all actions run together """
    pygame.init()
    logging.basicConfig(level=logging.INFO)
    # -------------------- Variables ---------------------
    # Setting game window's size
    screen_measurements = (SCR_WIDTH, SCR_HEIGHT)
    # We get the game sound & image managers
    managers.sound = SoundManager()
    managers.image = ImageManager()
    # Here, we set many configuration properties, depending on our config file or a group of defined values
    # in case the config file is missing
    config = SaveGame.load_config()
    screen = configuration_preset(config, screen_measurements, managers)
    set_game_window(managers.image)
    # Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # Scene pointer
    current_scene = SplashScreen(screen, screen_measurements, managers)
    # ---------------- MAIN LOOP -----------------
    while not done:
        # 1st step: Handling events
        switch = current_scene.event_handler()
        # 2nd step: Running game logic
        current_scene.run_logic()
        # 3rd step: Displaying all
        current_scene.display_frame()
        # 4th step: Evaluating scene switching
        if switch:
            if isinstance(current_scene, SplashScreen) and current_scene.endSplash:
                current_scene = TitleScreen(screen, screen_measurements, managers, config)
            elif isinstance(current_scene, TitleScreen):
                if current_scene.flags['NewGame']:
                    reset_flags(current_scene)
                    # We 'switch' to the game scene in a new game
                    current_scene = Game(screen, screen_measurements, managers)
                elif current_scene.flags['LoadGame'][0]:
                    reset_flags(current_scene)
                    # We 'switch' to the game scene through a loaded game
                    current_scene = Game(screen, screen_measurements, managers, "Player")
                elif current_scene.flags['Quit']:
                    done = True
            elif isinstance(current_scene, Game) and not current_scene.quit_all:
                current_scene = TitleScreen(screen, screen_measurements, managers, config)
                current_scene.set_theme()
            else:
                done = True
        # --- Limit to 60 frames per second
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
