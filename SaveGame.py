#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
from pygame import Surface, font
import pickle
import json
import logging
from os import walk
from constants import COLORS, SURFACE_MID_ALPHA, ANTIALIASING, ROOT


class SaveGame:
    LOGGER = logging.getLogger(__name__)

    def __init__(self, screen, scr_size, level, debug=False):
        """ This class will display the save game dialog and provide a set of load/save game tools

        :param screen: A reference for the main screen
        :param scr_size: The screen size (Default: 600 * 800)
        :param level: A reference to the level and its statistics
        :param debug: Flag for debugging into the game
        """
        # ------ Attributes -----------------------
        self.quit_all = self.resume = False
        self.screen = screen
        self.level = level
        self.debug = debug
        # Setting a plane, transparent background
        self.background = Surface([scr_size[0], scr_size[1] / 4])
        self.bounds = [0, self.background.get_height() * 3]
        self.background.set_alpha(SURFACE_MID_ALPHA)
        # Setting the text font for the save menu
        self.font = font.SysFont('Calibri', 25, True, False)
        # Save interface text (will include images on next versions)
        self.game_saved = False
        self.saveText = [
            self.font.render(_("Looking at this glittering spot fills you with det... "),
                             ANTIALIASING, COLORS['WHITE']),
            self.font.render(_("oh, wait, we don't want to be accused of plagiarism!"),
                             ANTIALIASING, COLORS['WHITE']),
            self.font.render(_("Do you want to save your game? Y: Yes; N: No"), ANTIALIASING, COLORS['WHITE']),
            self.font.render(_("Game saved!"), ANTIALIASING, COLORS['WHITE'])]

        if self.debug:
            pass

    # --------------- MAIN FLOW ---------------------
    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_all = True
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB or event.key == pygame.K_n:
                    self.resume = True
                    return True
                elif event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_y:  # 's' key
                    self.save_file()
                    # Game saved (Pfffiuuuu... what a relief)
                    self.resume = True
                    return True

        return False

    def update(self):
        # WIP
        pass

    def display(self):
        self.screen.blit(self.background, self.bounds)
        self.screen.blit(self.saveText[0], [self.bounds[0] + 10, self.bounds[1] + 10])
        self.screen.blit(self.saveText[1], [self.bounds[0] + 10, self.bounds[1] + 35])
        self.screen.blit(self.saveText[2], [self.bounds[0] + 10, self.bounds[1] + 60])
        if self.debug:
            pass

    def save_file(self):
        """ It gathers all game statistics we need to save and pushes them into a game file. Phew, that was close... """
        player_status = {"Name": self.level.player.name,
                         "Life": [self.level.player.life, self.level.player.maxLife],
                         "Energy": [self.level.player.energy, self.level.player.maxEnergy],
                         "Coins": [self.level.player.coins, self.level.player.maxWallet],
                         "Level": {'ID': self.level.ID,
                                   'PositionX': self.level.player.rect.x + abs(self.level.reference[0].rect.x),
                                   'PositionY': self.level.player.rect.y + abs(self.level.reference[0].rect.y)}}

        try:
            with open(f'{ROOT}/saves/{self.level.player.name}.sv', "wb") as game_file:
                pickle.dump(player_status, game_file)
                self.LOGGER.info("Game saved successfully!")
        except FileNotFoundError as fnf:
            self.LOGGER.error(f"It seems there's a conflict with the saving directory: {fnf}")
        except OSError as ose:
            # We reach this if it's been some kind of issue while opening the file (maybe it has some restrictions,
            # or a wild byte has broken into the filesystem and it's plundering). In any case, you can't open the
            # file.
            self.LOGGER.error(f"It seems there's a conflict with the saving directory: {ose}")
        except pickle.PicklingError as pe:
            self.LOGGER.error(f"The game couldn't be saved: {pe}")

    @classmethod
    def load_file(cls, name: str):
        """ Function for loading a game file. This needs a revision, I'm not sure about this implementation.
        It works, by the way.

        :param name: The game file's name
        :return: Your requested game data if succeed; None otherwise
        """
        try:
            with open(f'{ROOT}/saves/{name}.sv', "rb") as game_file:
                game_data = pickle.load(game_file)
                cls.LOGGER.info(f"Game loaded successfully!")
                return game_data
        except FileNotFoundError as fnf:
            # This exception can be reached if the user is playing a new game, or if anyone has messed up
            # with the save file and it's missing from its expected place.
            cls.LOGGER.warning(f"Game couldn't be loaded: {fnf}")
        except OSError as ose:
            # We reach this if it's been some kind of issue while opening the file (maybe it has some restrictions,
            # or a wild byte has broken into the filesystem and it's plundering). In any case, you can't open the
            # file.
            cls.LOGGER.warning(f"Game couldn't be loaded: {ose}")
        except pickle.UnpicklingError as pickle_err:
            cls.LOGGER.error(f"Bad format file: {pickle_err.args}")

    @classmethod
    def load_files(cls):
        """ Function for loading a game file list """
        try:
            files = []
            for save in walk(f'{ROOT}/saves'):
                for s in save[2]:
                    files.append(s)

            if len(files) > 0:
                cls.LOGGER.info(f"Game files loaded successfully!")
                return files
        except FileNotFoundError as fnf:
            # This exception can be reached if anyone has messed up with the save folder and it's
            # lost in cyberspace. And you can't do NOTHING for saving it, you monster
            cls.LOGGER.warning(f"Game files couldn't be loaded: {fnf}")

    @classmethod
    def load_config(cls):
        """ This function loads a group of game configuration parameters

        :return: Game configuration parameters' list if succeeds; otherwise, None
        """
        try:
            with open(f'{ROOT}/config.json') as data_file:
                file = json.load(data_file)
                cls.LOGGER.info(f"Game configuration loaded successfully!")
                return file  # file["options"]
        except FileNotFoundError as fnf:
            # This exception can be reached if the user is playing a new game, or if anyone has messed up
            # with the save file and it's missing from its expected place.
            cls.LOGGER.warning(f"Game configuration couldn't be loaded: {fnf}")
        except OSError as ose:
            # We reach this if it's been some kind of issue while opening the file (maybe it has some restrictions,
            # or a wild byte has broken into the filesystem and it's plundering). In any case, you can't open the
            # file.
            cls.LOGGER.warning(f"Game configuration couldn't be loaded: {ose}")

    @classmethod
    def save_config(cls, full_screen: bool, music_vol: float, fx_vol: float, lang: str):
        try:
            with open(f'{ROOT}/config.json', "w") as file:
                json.dump({"full_screen": full_screen, "music_volume": music_vol, "fx_volume": fx_vol, "lang": lang},
                          file)
                cls.LOGGER.info("Game configuration saved successfully!")
        except FileNotFoundError as fnf:
            # This exception can be reached if the user is playing a new game, or if anyone has messed up
            # with the save file and it's missing from its expected place.
            cls.LOGGER.warning(f"File not found: {fnf}")
        except OSError as ose:
            # We reach this if it's been some kind of issue while opening the file (maybe it has some restrictions,
            # or a wild byte has broken into the filesystem and it's plundering). In any case, you can't open the
            # file.
            cls.LOGGER.warning(f"SO error: {ose}")
