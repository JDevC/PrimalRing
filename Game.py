#!/usr/bin/env python3

# ---------------------- IMPORTS ---------------------
# Python libs
import pygame
# Own libs
from SaveGame import SaveGame
from models.Block import Player
from models.Level import Level1, Level2
from views.PauseScreen import PauseScreen
from constants import COLORS, PLAYER_SIZE, ANTIALIASING, DEBUG


class Game:
    def __init__(self, screen, scr_size, sound_manager, saved_state_name=None):
        """ This is the general manager game class. It has the main functions and attributes which rule above
        all the rest.

        :param screen:
        :param scr_size:
        :param saved_state_name: """
        # Main game attributes
        self.screen = screen
        self.scrSize = scr_size
        self.soundMan = sound_manager
        self.font = pygame.font.SysFont('Calibri', 25, True, False)
        # Endgame (also a truly brutal Megadeth album)
        self.gameOver = False
        self.quit_all = False
        # GAME OVER text
        self.gOverText = [self.font.render("GAME OVER", ANTIALIASING, COLORS['WHITE']),
                          self.font.render("Want to try again?", ANTIALIASING, COLORS['WHITE']),
                          self.font.render("Yes / No", ANTIALIASING, COLORS['WHITE'])]
        # PAUSE elements
        self.pause = None
        self.pauseFlag = False                                          # Well, this is obvious
        # SAVE GAME elements
        self.save = None
        self.saveFlag = False                                           # Well, this is obvious
        # Game loading
        saved_state = None
        if saved_state_name is not None:
            saved_state = SaveGame.load_file(saved_state_name)
        # Player
        self.player = Player(COLORS['RED'], PLAYER_SIZE, PLAYER_SIZE, sound_manager, saved_state)
        # Levels
        self.levels = {"Doom Valley": Level1(screen, scr_size, sound_manager, self.player, DEBUG),
                       "The RING": Level2(screen, scr_size, sound_manager, self.player, DEBUG)}
        if saved_state is not None:
            # You've a game saved, so you start in the level and position stored
            self.level = self.levels[saved_state['Level']['ID']]
            self.player.rect.x = saved_state['Level']['PositionX']
            self.player.rect.y = saved_state['Level']['PositionY']
        else:
            # Don't have a game file? You start where everyone does (We respect and support equality)
            self.level = self.levels['Doom Valley']
            self.player.rect.x = self.level.levelInit[0]
            self.player.rect.y = self.level.levelInit[1]

        self.player.plainLevel = self.level.plainLevel
        # We activate the music in the current level
        self.level.set_theme()

    # ---------- Methods ----------------------
    def event_handler(self):
        """ Manages all events in game

        :return: True if the player wants to exit the game; False otherwise """
        # Pause screen
        if self.pauseFlag:
            for event in pygame.event.get():                            # User did something
                if event.type == pygame.QUIT:                           # If user clicked close
                    return self.quit_game()                             # We are done so we exit this loop
                # Incoming functionality on next versions!
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pass
                    elif event.key == pygame.K_RIGHT:
                        pass
                    elif event.key == pygame.K_UP:
                        self.pause.go_up()
                    elif event.key == pygame.K_DOWN:
                        self.pause.go_down()
                    elif event.key == pygame.K_p:
                        # We resume the music streaming
                        self.soundMan.pause_music(False)
                        self.pauseFlag = False                          # Exits the pause screen
                    elif event.key == pygame.K_RETURN:
                        self.pause.soundMan.play_fx('Accept')
                        if self.pause.menuList[self.pause.currentMenu]['Name'] == '- Inventory':
                            print("Accessing inventory... soon!")
                        elif self.pause.menuList[self.pause.currentMenu]['Name'] == '- Skills':
                            print("Accessing skill board... soon!")
                        elif self.pause.menuList[self.pause.currentMenu]['Name'] == '- Options':
                            print("Accessing options... soon!")
                        elif self.pause.menuList[self.pause.currentMenu]['Name'] == '- Quit':
                            return True
        # Save screen
        elif self.saveFlag:
            for event in pygame.event.get():                            # User did something
                if event.type == pygame.QUIT:                           # If user clicked close
                    return self.quit_game()                             # We are done so we exit this loop
                # Incoming functionality on next versions!
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:                         # 'TAB' key
                        # We clean all flags and the save screen object
                        self.saveFlag = False
                        self.level.player.saveFlag = False
                        self.save = None
                    elif event.key == pygame.K_UP:
                        pass
                    elif event.key == pygame.K_DOWN:
                        pass
                    elif event.key == pygame.K_y:                       # 's' key
                        # This saves your game!
                        self.save.save_file()
                        # Game saved (Pfffiuuuu... what a relief)
                        self.saveFlag = False
                        self.level.player.saveFlag = False
                        self.save = None
                        pass
                    elif event.key == pygame.K_n:                       # 'n' key
                        # This avoids your game for being saved!
                        # You have a confident will, don't you?
                        self.saveFlag = False
                        self.level.player.saveFlag = False
                        self.save = None
        # Game Screen
        else:
            for event in pygame.event.get():                            # User did something
                if event.type == pygame.QUIT:                           # If user clicked close
                    return self.quit_game()                             # We are done so we exit this loop
                if event.type == pygame.KEYDOWN:                        # User hit a key
                    if event.key == pygame.K_LEFT:                      # <-
                        self.player.direction['LEFT'] = True
                        self.player.direction['RIGHT'] = not self.player.direction['LEFT']
                    if event.key == pygame.K_RIGHT:                     # ->
                        self.player.direction['RIGHT'] = True
                        self.player.direction['LEFT'] = not self.player.direction['RIGHT']
                    if event.key == pygame.K_UP:
                        self.player.direction['UP'] = True
                    if event.key == pygame.K_DOWN:
                        self.player.direction['DOWN'] = True
                    if event.key == pygame.K_p:                           # 'p' key
                        # We pause the music streaming
                        self.soundMan.pause_music()
                        self.pauseFlag = True
                        self.pause = PauseScreen(self.screen, self.scrSize, self.soundMan, self.level.player)
                    if event.key == pygame.K_TAB:                         # 'TAB' key
                        if self.level.player.saveFlag:
                            self.saveFlag = True
                            self.save = SaveGame(self.screen, self.scrSize, self.level)

                if event.type == pygame.KEYUP:                          # User released a key
                    if event.key == pygame.K_LEFT:
                        self.player.direction['LEFT'] = False
                    if event.key == pygame.K_RIGHT:
                        self.player.direction['RIGHT'] = False
                    if event.key == pygame.K_UP:
                        self.player.direction['UP'] = False
                    if event.key == pygame.K_DOWN:
                        self.player.direction['DOWN'] = False

        return False

    def run_logic(self):
        """ This refresh all in-game objects and check collisions """
        # Checks if the player still lives on
        if not self.gameOver:
            if self.pauseFlag:
                self.pause.update()
            elif self.saveFlag:
                pass
            else:
                # Updates all sprites and checks if the player has made a level change
                update = self.level.update()
                if update:
                    # It swaps into another level.
                    # This point needs a revision: our game map should consist on a central level from where
                    # we can travel into the others, but at least it's a beginning
                    if self.level.player.isDead:
                        self.gameOver = True
                    else:
                        self.soundMan.stop_music()
                        self.level = self.levels['The RING']
                        self.player.rect.x = self.level.levelInit[0]
                        self.player.rect.y = self.level.levelInit[1]
                        self.player.plainLevel = self.level.plainLevel
                        # We activate the music in the current level
                        self.level.set_theme()

    def display_frame(self):
        """ This function displays all graphic resources and effects """
        self.screen.fill(COLORS['GREY'])                   # BLACK
        # Checks if the player still lives on
        if self.gameOver:
            self.screen.blit(self.gOverText[0], [(self.scrSize[0] / 2) - 45, self.scrSize[1] / 2 - 50])
            self.screen.blit(self.gOverText[1], [(self.scrSize[0] / 2) - 70, self.scrSize[1] / 2 - 25])
            self.screen.blit(self.gOverText[2], [(self.scrSize[0] / 2) - 50, self.scrSize[1] / 2 + 50])
        else:
            self.level.display()
            # This implementation allows us to cover our game screen with the pause screen,
            # stopping all mechanics and events in game except those who are involved in the
            # pause screen logic flow, but also letting us to see a static impression of the
            # game behind the pause screen.
            if self.pauseFlag:
                self.pause.display()
            elif self.saveFlag:
                self.save.display()
        # --- This is 'update' for pygame library
        pygame.display.flip()

    def quit_game(self):
        """ Quick game exit """
        # We kill the music stream
        self.soundMan.panic()
        self.quit_all = True
        return True
