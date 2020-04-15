#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
from SaveGame import SaveGame
from managers.LevelManager.LevelDataClass import LevelDataClass
from managers.LevelManager.LevelManager import LevelManager
from models.Bodies.PlayerBody import PlayerBody
from views._ScreenHolder import _ScreenHolder
from views.PauseScreen import PauseScreen
from constants import COLORS, PLAYER_SIZE, ANTIALIASING


class Game:
    def __init__(self, screen, scr_size, managers, saved_state_name: str = None):
        """ This is the general manager game class. It has the main functions and attributes which rule above
        all the rest.

        :param screen:
        :param scr_size:
        :param saved_state_name: """
        # Main game attributes
        self._screen = screen
        self._scrSize = scr_size
        self._managers = managers
        self._font = pygame.font.SysFont('Calibri', 25, True, False)
        # Endgame (also a truly brutal Megadeth album)
        self.gameOver = False
        self.quit_all = False
        # GAME OVER text
        g_over_str = [_("GAME OVER"), _("Want to try again?"), _("Yes / No")]
        self.gOverText = [self._font.render(x, ANTIALIASING, COLORS['WHITE']) for x in g_over_str]
        self._pause = _ScreenHolder()
        self._save = _ScreenHolder()
        # Game loading
        saved_state = saved_state_name if saved_state_name is None else SaveGame.load_file(saved_state_name)
        # Player
        self.player = PlayerBody(COLORS['RED'], PLAYER_SIZE, PLAYER_SIZE, managers, saved_state)
        self._init_player_location(saved_state, self.player, self._managers.levels)
        # We activate the music in the current level
        self._level.set_theme()

    # ---------- Public Methods ----------------------
    def event_handler(self):
        if self._pause.flag:
            return self._handle_screen_events(self._pause, self._pause_screen_cleaning)
        elif self._save.flag:
            return self._handle_screen_events(self._save, self._save_screen_cleaning)
        else:
            return self._handle_game_screen_events()

    def run_logic(self):
        if not self.gameOver:
            if self._pause.flag:
                self._pause.screen.update()
            elif self._save.flag:
                self._save.screen.update()
            else:
                # Updates all sprites and checks if the player has made a level change
                if self._level.update():
                    # It swaps into another level.
                    # This point needs a revision: our game map should consist on a central level from where
                    # we can travel into the others, but at least it's a beginning
                    if self.player.isDead:
                        self.gameOver = True
                    else:
                        self._managers.sound.stop_music()
                        next_id = self._level.next_id
                        level_data = LevelDataClass(next_id, self._screen, self._scrSize, self._managers, self.player)
                        self._level = self._managers.levels.load_level(level_data)
                        self.player.rect.x = self._level.levelInit[0]
                        self.player.rect.y = self._level.levelInit[1]
                        self.player.plainLevel = self._level.plainLevel
                        # We activate the music in the current level
                        self._level.set_theme()

    def display_frame(self):
        """ This function displays all graphic resources and effects """
        self._screen.fill(COLORS['GREY'])
        # Checks if the player still lives on
        if self.gameOver:
            self._screen.blit(self.gOverText[0], [(self._scrSize[0] / 2) - 45, self._scrSize[1] / 2 - 50])
            self._screen.blit(self.gOverText[1], [(self._scrSize[0] / 2) - 70, self._scrSize[1] / 2 - 25])
            self._screen.blit(self.gOverText[2], [(self._scrSize[0] / 2) - 50, self._scrSize[1] / 2 + 50])
        else:
            self._level.display()
            # This logic allows us to cover our game screen with the pause screen,
            # stopping all mechanics and events in game except those who are involved in the
            # pause screen logic flow, but also letting us to see a static impression of the
            # game behind the pause screen.
            if self._pause.flag:
                self._pause.screen.display()
            elif self._save.flag:
                self._save.screen.display()
        # --- This is 'update' for pygame library
        pygame.display.flip()

    def quit_game(self):
        self._managers.sound.panic()
        self.quit_all = True
        return True

    # ---------- Internal Methods ----------------------
    def _init_player_location(self, saved_state: dict, player, level_manager: LevelManager):
        if saved_state is not None:
            # You've a game saved, so you start in the level and position stored
            level_data = LevelDataClass(saved_state['Level']['ID'], self._screen, self._scrSize, self._managers, player)
            self._level = level_manager.load_level(level_data)
            player.rect.x = saved_state['Level']['PositionX']
            player.rect.y = saved_state['Level']['PositionY']
        else:
            # Don't have a game file? You start where everyone does (We respect and support equality)
            level_data = LevelDataClass("DoomValley", self._screen, self._scrSize, self._managers, player)
            self._level = level_manager.load_level(level_data)
            player.rect.x = self._level.levelInit[0]
            player.rect.y = self._level.levelInit[1]

        player.plainLevel = self._level.plainLevel

    def _handle_screen_events(self, screen_holder: _ScreenHolder, callback):
        if screen_holder.screen.event_handler():
            if screen_holder.screen.quit_all:
                return self.quit_game()
            elif screen_holder.screen.resume:
                callback()
                return False
            else:
                return True

    def _save_screen_cleaning(self):
        self._level.player.saveFlag = False
        self._save = _ScreenHolder()

    def _pause_screen_cleaning(self):
        self._pause = _ScreenHolder()

    def _handle_game_screen_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return self.quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.direction.left = True
                    self.player.direction.right = not self.player.direction.left
                if event.key == pygame.K_RIGHT:
                    self.player.direction.right = True
                    self.player.direction.left = not self.player.direction.right
                if event.key == pygame.K_UP:
                    self.player.direction.up = True
                if event.key == pygame.K_DOWN:
                    self.player.direction.down = True
                if event.key == pygame.K_p:
                    screen = PauseScreen(self._screen, self._scrSize, self._managers, self._level.player)
                    self._pause = _ScreenHolder(screen, True)
                if event.key == pygame.K_TAB:
                    if self._level.player.saveFlag:
                        self._save = _ScreenHolder(SaveGame(self._screen, self._scrSize, self._level), True)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.direction.left = False
                if event.key == pygame.K_RIGHT:
                    self.player.direction.right = False
                if event.key == pygame.K_UP:
                    self.player.direction.up = False
                if event.key == pygame.K_DOWN:
                    self.player.direction.down = False

        return False
