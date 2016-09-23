#!/usr/bin/env python

# ---------------------- IMPORTS ---------------------
# Python libs
import pygame
# Own libs
from Block6 import Player
from Level6 import Level1, Level2
import PauseScreen
import SaveGame
from constants6 import COLORS, PLAYER_SIZE, ANTIALIASING, DEBUG
''' This is the general manager game class. It has the
    main functions and attributes which rule above all
    the rest.'''


class Game(object):
    # ---------- Constructor ----------------------
    def __init__(self, screen, scr_size, saved_state_name=None):
        # Main game attributes
        self.gameOver = False                                           # Endgame (also a truly brutal Megadeth album)
        self.quit_all = False
        self.screen = screen
        self.scrSize = scr_size
        self.font = pygame.font.SysFont('Calibri', 25, True, False)
        # GAME OVER text
        self.gOverText = []
        self.gOverText.append(self.font.render("GAME OVER", ANTIALIASING, COLORS['WHITE']))
        self.gOverText.append(self.font.render("Want to try again?", ANTIALIASING, COLORS['WHITE']))
        self.gOverText.append(self.font.render("Yes / No", ANTIALIASING, COLORS['WHITE']))
        # PAUSE elements
        self.pause = None
        self.pauseFlag = False                                          # Well, this is obvious
        # SAVE GAME elements
        self.save = None
        self.saveFlag = False                                           # Well, this is obvious
        # Game loading
        savedState = None
        if saved_state_name is not None:
            savedState = SaveGame.load_file(saved_state_name)           # We try to load a game file
        # Player
        self.player = Player(COLORS['RED'], PLAYER_SIZE, PLAYER_SIZE, savedState)
        # Levels
        self.levels = {"Doom Valley": Level1(screen, scr_size, self.player, DEBUG),
                       "The RING": Level2(screen, scr_size, self.player, DEBUG)}
        if savedState is not None:
            # You've a game saved, so you start in the level and position stored
            self.level = self.levels[savedState['Level']['ID']]
            self.player.rect.x = savedState['Level']['PositionX']
            self.player.rect.y = savedState['Level']['PositionY']
        else:
            # Don't have a game file? You start where everyone does (We respect and support equality)
            self.level = self.levels['Doom Valley']
            self.player.rect.x = self.level.levelInit[0]
            self.player.rect.y = self.level.levelInit[1]

        self.player.plainLevel = self.level.plainLevel

    # ---------- Methods ----------------------
    # This function manages all events in game
    def event_handler(self):
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
                        self.pauseFlag = False                          # Exits the pause screen
                    elif event.key == pygame.K_RETURN:
                        self.pause.acceptSound.play()
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
                        # (Pfffiuuuu... what a relief)
                        self.save.save_file()
                        # Game saved
                        # self.save.load_file()
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
                if event.type == pygame.KEYDOWN:
                    # Figure out if it was an arrow key. If it's so, adjust speed.
                    if event.key == pygame.K_LEFT:                      # <-
                        self.level.player.go_left()
                    if event.key == pygame.K_RIGHT:                     # ->
                        self.level.player.go_right()
                    if event.key == pygame.K_UP:
                        if self.level.player.plainLevel:
                            self.level.player.go_up()
                        else:
                            self.level.player.jump()
                    if event.key == pygame.K_DOWN:
                        if self.level.player.plainLevel:
                            self.level.player.go_down()
                    if event.key == pygame.K_p:                         # 'p' key
                        self.pauseFlag = True
                        self.pause = PauseScreen.PauseScreen(self.screen, self.scrSize, self.level.player)
                    if event.key == pygame.K_TAB:                         # 'TAB' key
                        if self.level.player.saveFlag:
                            self.saveFlag = True
                            self.save = SaveGame.SaveGame(self.screen, self.scrSize, self.level)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.level.player.stop_x()
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        if self.level.player.plainLevel:
                            self.level.player.stop_y()

        return False

    # This function is given to refresh all objects and check collisions
    def run_logic(self):
        # Checks if the player still lives on
        if not self.gameOver:
            if self.pauseFlag:
                self.pause.update()
            elif self.saveFlag:
                pass
            else:
                # Updates all sprites and checks if the player has made a level change
                reached = self.level.update()
                if reached:
                    # It swaps into another level.
                    # This point needs a revision: our game map should consist on a central level from where
                    # we can travel into the others, but at least it's a beginning
                    # self.gameOver = True
                    self.level = self.levels['The RING']
                    self.player.rect.x = self.level.levelInit[0]
                    self.player.rect.y = self.level.levelInit[1]
                    self.player.plainLevel = self.level.plainLevel

    # This function displays all graphic resources and effects
    def display_frame(self):
        self.screen.fill(COLORS['BLACK'])
        # Checks if the player still lives on
        if self.gameOver:
            self.screen.blit(self.gOverText[0], [(self.scrSize[0]/2) - 45, self.scrSize[1]/2 - 50])
            self.screen.blit(self.gOverText[1], [(self.scrSize[0]/2) - 70, self.scrSize[1]/2 - 25])
            self.screen.blit(self.gOverText[2], [(self.scrSize[0]/2) - 50, self.scrSize[1]/2 + 50])
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

    # Quick game exit
    def quit_game(self):
        self.quit_all = True
        return True

    def __str__(self):
        return "Game"
