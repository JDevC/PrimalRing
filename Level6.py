#!/usr/bin/env python

# ---------------------- IMPORTS ---------------------
# Python libs
from pygame import image, font, sprite
from random import randrange
# Own libs
# We could just import the Block module, but it's more reliable as is
from Block6 import Snow, Player, Floor, Hole, Coin
from constants6 import COLORS, ANTIALIASING, ROOT, PLAYER_SIZE, COIN_SIZE, FLOOR_SIZE
''' This class manages all in terms of creating level structures
    and loading graphic and audio resources. Every level created
    has inheritance from this Level class.'''


# General class
class Level(object):
    # Globals
    root = ROOT

    # ---------- Constructor ----------------------
    def __init__(self, screen, scr_size, debug=False):
        # -- Attributes -----------------------
        self.debug = debug                          # Flag for debugging into the game
        self.screen = screen                        # A reference for the main screen
        self.scr_size = scr_size                    # The screen size
        self.structure = []
        self.backgroundImg = image.load(self.root + "/images/astro.jpg").convert()
        self.font = font.SysFont('Calibri', 25, True, False)
        # Sprite lists for the win!
        self.colliders = sprite.Group()             # Walls, platforms, floor, enemies, switches...
        self.temporary = sprite.Group()             # Coins, ammo, lifepoints...
        self.bodies = sprite.Group()                # All sprites (this is for render on the screen)
        self.player = Player(COLORS['RED'], PLAYER_SIZE, PLAYER_SIZE)
        # HUD elements
        self.coinText = self.font.render("Coins: " + str(self.player.coins), ANTIALIASING, COLORS['WHITE'])
        self.lifeText = self.font.render("Life: " + str(self.player.life), ANTIALIASING, COLORS['WHITE'])
        # Debug
        if self.debug:
            self.coords = self.font.render("X: " + str(self.player.rect.x)
                                           + "; Y: " + str(self.player.rect.y), ANTIALIASING, COLORS['WHITE'])

    # ---------- Methods --------------------------
    def display(self):
        self.bodies.add(self.player)
        self.screen.blit(self.backgroundImg, [0, 0])
        self.bodies.draw(self.screen)
        self.screen.blit(self.coinText, [50, 50])
        self.screen.blit(self.lifeText, [50, 70])
        if self.debug:
            self.screen.blit(self.coords, [500, 70])

        self.bodies.remove(self.player)


# 2D Plain level's type class
class PlainLevel(Level):
    # ---------- Constructor ----------------------
    def __init__(self, screen, scr_size, debug=False):
        # -- Parent constructor ---------------
        super().__init__(screen, scr_size, debug)
        self.player.plainLevel = True

    # ---------- Methods --------------------------
    def update(self):
        # Update all elements in level
        self.bodies.update()
        self.player.update(self.colliders, self.temporary)
        self.coinText = self.font.render("Coins: " + str(self.player.coins), ANTIALIASING, COLORS['WHITE'])
        self.lifeText = self.font.render("Life: " + str(self.player.life), ANTIALIASING, COLORS['WHITE'])
        if self.debug:
            self.coords = self.font.render("X: " + str(self.player.rect.x) + "; Y: "
                                           + str(self.player.rect.y) + "VelX: " + str(self.player.velX)
                                           + "; VelY: " + str(self.player.velY), True, COLORS['WHITE'])

        return False


# 2D Horizontal level's type class
class HorizontalLevel(Level):
    # ---------- Constructor ----------------------
    def __init__(self, screen, scr_size, debug=False):
        # -- Parent constructor ---------------
        super().__init__(screen, scr_size, debug)
        self.player.plainLevel = False

    # ---------- Methods --------------------------
    def update(self):
        # Update all elements in level
        self.bodies.update()
        # Checks the condition for going out the level
        if self.player.coins < 10:
            self.player.update(self.colliders, self.temporary)
            self.coinText = self.font.render("Coins: " + str(self.player.coins), ANTIALIASING, COLORS['WHITE'])
            self.lifeText = self.font.render("Life: " + str(self.player.life), ANTIALIASING, COLORS['WHITE'])
            if self.debug:
                '''self.coords = self.font.render("X: " + str(self.player.rect.x) + "; Y: "
                                               + str(self.player.rect.y)
                                               + "VelX: " + str(self.player.velX)
                                               + "; VelY: "
                                               + str(self.player.velY), ANTIALIASING, COLORS['WHITE'])'''
                self.coords = self.font.render("X: " + str(self.player.rect.x) + "; Y: "
                                               + str(self.player.rect.y)
                                               + "; Obj: "
                                               + str(self.player.coins), ANTIALIASING, COLORS['WHITE'])

            return False

        else:
            return True


# All levels must inherit from 'HorizontalLevel' or 'Plain Level'
class Level1(HorizontalLevel):
    # ---------- Constructor ----------------------
    # def __init__(self, screen, src_size, root, debug=False):
    def __init__(self, screen, scr_size, debug=False):
        # -- Parent constructor ---------------
        super().__init__(screen, scr_size, debug)
        # Level map structure
        self.structure = ["ffffffffffffffff",
                          "f            ccf",
                          "f   c       c  f",
                          "f   f       f  f",
                          "f          ff  f",
                          "f  f ffff fffc f",
                          "f     c c c  f f",
                          "f f   c c c    f",
                          "fP f           f",
                          "f              f",
                          "f              f",
                          "ffffffffffffffff"]
        # Populating level
        cnt_y = 0                                       # Initial Y-axis grid
        for row in self.structure:
            cnt_x = 0                                   # Initial X-axis grid
            for column in row:
                if column == "f":                       # 'f' stands for 'Floor'
                    floor = Floor(COLORS['BLUE'], FLOOR_SIZE, FLOOR_SIZE)
                    floor.rect.x = cnt_x
                    floor.rect.y = cnt_y
                    self.colliders.add(floor)
                    self.bodies.add(floor)
                elif column == "P":                     # 'P' stands for 'Player'
                    self.player.rect.x = cnt_x
                    self.player.rect.y = cnt_y
                elif column == "c":                     # 'c' stands for 'Coin'
                    coin = Coin(COLORS['ORANGE'], COIN_SIZE, COIN_SIZE)
                    coin.rect.x = cnt_x + 10
                    coin.rect.y = cnt_y + 10
                    self.temporary.add(coin)
                    self.bodies.add(coin)

                cnt_x += 50                             # Increment X-axis for the next tile

            cnt_y += 50                                 # Increment Y-axis for the next tile

        # Random location for snow flakes
        for i in range(50):     # 50
            # Snow instance
            flake = Snow(COLORS['WHITE'], 2, 2, self.scr_size)
            # We create a random placement
            flake.rect.x = randrange(self.scr_size[0])
            flake.rect.y = randrange(self.scr_size[1])
            # Then we add the flake to the block lists
            flake.firstX = flake.rect.x
            self.temporary.add(flake)
            self.bodies.add(flake)


# All levels must inherit from 'HorizontalLevel' or 'Plain Level'
class Level2(PlainLevel):
    # ---------- Constructor ----------------------
    def __init__(self, screen, src_size, debug=False):
        # -- Parent constructor ---------------
        super().__init__(screen, src_size, debug)
        # -- Attributes -----------------------
        self.structure = ["fffffff ffffffff",
                          "f       f      f",
                          "f fffff f      f",
                          "f fhf h     f  f",
                          "f f        ff  f",
                          "f ff    f fff  f",
                          "f f   h      f f",
                          "f ff  h        f",
                          "f     h        f",
                          "ffff ff        f",
                          "fP   hf       ff",
                          "fffffffffffffff "]
        # Populating level
        cnt_y = 0                                       # Initial Y-axis tile grid
        for row in self.structure:
            cnt_x = 0                                   # Initial X-axis tile grid
            for column in row:
                if column == "f":                       # 'f' stands for 'Floor'
                    floor = Floor(COLORS['BLUE'], 50, 50)
                    floor.rect.x = cnt_x
                    floor.rect.y = cnt_y
                    self.colliders.add(floor)
                    self.bodies.add(floor)
                elif column == "h":                     # 'h' stands for 'Hole'
                    hole = Hole(COLORS['BLACK'], 50, 50)
                    hole.rect.x = cnt_x
                    hole.rect.y = cnt_y
                    self.colliders.add(hole)
                    self.bodies.add(hole)
                elif column == "P":                     # 'P' stands for 'Player'
                    # self.hero = Hero(RED, 50, 50)
                    self.player.rect.x = cnt_x
                    self.player.rect.y = cnt_y
                    # self.bodies.add(self.hero)

                cnt_x += 50                             # Increment X-axis for the next tile

            cnt_y += 50  # Increment Y-axis for the next tile
