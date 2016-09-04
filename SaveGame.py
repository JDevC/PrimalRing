#!/usr/bin/env python

# ---------------------- IMPORTS ---------------------
# Python libs
from pygame import Surface, font
import pickle
from os import walk
# Own libs
from constants6 import COLORS, SURFACE_MID_ALPHA, ANTIALIASING, ROOT


# General class
class SaveGame(object):
    # Globals
    root = ROOT

    # ---------- Constructor ----------------------
    def __init__(self, screen, scr_size, level, debug=False):
        # -- Attributes -----------------------
        self.debug = debug                                      # Flag for debugging into the game
        self.screen = screen                                    # A reference for the main screen
        # self.scr_size = scr_size                              # The screen size (not needed 'as is' for now)
        self.level = level                                      # A reference to the level and his statistics
        # Setting a plane, transparent background
        self.background = Surface([scr_size[0], scr_size[1]/4])
        self.bounds = [0, self.background.get_height() * 3]
        # self.background.fill(COLORS['WHITE'])
        self.background.set_alpha(SURFACE_MID_ALPHA)
        # Setting the text font for the save menu
        self.font = font.SysFont('Calibri', 25, True, False)
        # Save interface text (will include images on next versions)
        self.game_saved = False
        self.saveText = []
        self.saveText.append(self.font.render("Looking at this glittering spot fills you with det... ",
                                              ANTIALIASING, COLORS['WHITE']))
        self.saveText.append(self.font.render("oh, wait, we don't want to be accused of plagiarism!",
                                              ANTIALIASING, COLORS['WHITE']))
        self.saveText.append(self.font.render("Do you want to save your game? Y: Yes; N: No",
                                              ANTIALIASING, COLORS['WHITE']))
        self.saveText.append(self.font.render("Game saved!", ANTIALIASING, COLORS['WHITE']))
        # Debug
        if self.debug:
            pass

    # ---------- Methods --------------------------
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

    # Function for saving a game file
    def save_file(self):
        player_status = {"Name": self.level.player.name,
                         "Life": [self.level.player.life, self.level.player.maxLife],
                         "Energy": [self.level.player.energy, self.level.player.maxEnergy],
                         "Coins": [self.level.player.coins, self.level.player.maxWallet],
                         "Level": {'ID': self.level.ID,
                                   'PositionX': self.level.player.rect.x,
                                   'PositionY': self.level.player.rect.y}
                         }
        # file = open(ROOT + '/saves/save_trial.sv', "wb")
        file = open(ROOT + '/saves/' + self.level.player.name + '.sv', "wb")
        pickle.dump(player_status, file)
        file.close()


# Function for loading a game file. This needs a revision, I'm not sure about this
# implementation. It works, by the way.
def load_file(name):
    try:
        # file = open(ROOT + '/saves/save_trial.sv', "rb")
        file = open(ROOT + '/saves/' + name + '.sv', "rb")
        obj = pickle.load(file)
        file.close()
        # print(obj)
        return obj
    except FileNotFoundError:
        # This exception can be reached if the user is playing a new game, or if anyone has messed up
        # with the save file and it's missing from its expected place.
        return None
    except pickle.UnpicklingError:
        print("Bad format file!")
        return None


# This returns a list of saved games
def load_files():
    try:
        files = []
        for save in walk(ROOT + '/saves'):
            for s in save[2]:
                files.append(s)

        if len(files) > 0:
            return files
        else:
            return None
    except FileNotFoundError:
        # This exception can be reached if anyone has messed up with the save folder and it's
        # lost in cyberspace. And you can't do NOTHING for saving it, you monster
        return None
