#!/usr/bin/env python

# ---------------------- IMPORTS ---------------------
# Python libs
from pygame import image, font, sprite
from random import randrange
# Own libs
from Block6 import Snow, Player, Floor, Hole, Coin, SavePoint
from constants6 import COLORS, ANTIALIASING, ROOT, PLAYER_SIZE, COIN_SIZE, FLOOR_SIZE
''' This class manages all in terms of creating level structures
    and loading graphic and audio resources. Every level created
    has inheritance from this Level class.'''


# General class
class Level(object):
    # Globals
    root = ROOT

    # ---------- Constructor ----------------------
    # def __init__(self, screen, scr_size, debug=False):
    def __init__(self, screen, scr_size, player, debug=False):
        # -- Attributes -----------------------
        self.debug = debug                          # Flag for debugging into the game
        self.screen = screen                        # A reference for the main screen
        self.scrSize = scr_size                     # The screen size
        self.ID = None                              # A level identifier
        self.structure = []                         # Level structure reference
        self.levelInit = [0, 0]                         # Level enter point
        self.backgroundImg = None                   # Background image reference
        self.font = font.SysFont('Calibri', 25, True, False)
        # Sprite lists for the win!
        self.colliders = sprite.Group()             # Walls, platforms, floor, enemies, switches...
        self.temporary = sprite.Group()             # Coins, ammo, lifepoints...
        self.player_display = sprite.Group()        # The player itself
        self.player = player
        self.player_display.add(self.player)
        self.bodies = sprite.Group()                # All sprites (this is for render on the screen)
        # HUD elements
        self.coinText = self.font.render("Coins: " + str(self.player.coins), ANTIALIASING, COLORS['WHITE'])
        self.lifeText = self.font.render("Life: " + str(self.player.life), ANTIALIASING, COLORS['WHITE'])
        self.energyText = self.font.render("Energy: " + str(self.player.energy), ANTIALIASING, COLORS['WHITE'])
        # Debug
        if self.debug:
            self.debText = self.font.render("X: " + str(self.player.rect.x)
                                            + "; Y: " + str(self.player.rect.y),
                                            ANTIALIASING, COLORS['WHITE'])

    # ---------- Methods --------------------------
    def display(self):
        # We check if the level has a background image and blit it to the screen
        if self.backgroundImg is not None:
            self.screen.blit(self.backgroundImg, [0, 0])
        self.bodies.draw(self.screen)
        self.player_display.draw(self.screen)
        self.screen.blit(self.coinText, [50, 50])
        self.screen.blit(self.lifeText, [50, 70])
        self.screen.blit(self.energyText, [50, 90])
        if self.debug:
            self.screen.blit(self.debText, [500, 70])

    # It fills all level gaps with elements taking a pattern
    def fill_level(self, structure):
        cnt_y = 0  # Initial Y-axis tile grid
        for row in structure:
            cnt_x = 0  # Initial X-axis tile grid
            for column in row:
                if column == "f":  # 'f' stands for 'Floor'
                    floor = Floor(COLORS['BLUE'], 50, 50)
                    floor.rect.x = cnt_x
                    floor.rect.y = cnt_y
                    self.colliders.add(floor)
                    self.bodies.add(floor)
                elif column == "h":  # 'h' stands for 'Hole'
                    hole = Hole(COLORS['BLACK'], 50, 50)
                    hole.rect.x = cnt_x
                    hole.rect.y = cnt_y
                    self.colliders.add(hole)
                    self.bodies.add(hole)
                elif column == "s":  # 's' stands for 'SavePoint'
                    save = SavePoint(COLORS['WHITE'], 50, 50)
                    save.rect.x = cnt_x
                    save.rect.y = cnt_y
                    self.colliders.add(save)
                    self.bodies.add(save)
                elif column == "c":  # 'c' stands for 'Coin'
                    coin = Coin(COLORS['ORANGE'], COIN_SIZE, COIN_SIZE)
                    coin.rect.x = cnt_x + 10
                    coin.rect.y = cnt_y + 10
                    self.temporary.add(coin)
                    self.bodies.add(coin)

                cnt_x += 50  # Increment X-axis for the next tile

            cnt_y += 50  # Increment Y-axis for the next tile

    # It renders all main hud information
    def render_hud(self):
        self.coinText = self.font.render("Coins: " + str(self.player.coins), ANTIALIASING, COLORS['WHITE'])
        self.lifeText = self.font.render("Life: " + str(self.player.life), ANTIALIASING, COLORS['WHITE'])
        self.energyText = self.font.render("Energy: " + str(self.player.energy), ANTIALIASING, COLORS['WHITE'])


# 2D Plain level's type class
class PlainLevel(Level):
    # ---------- Constructor ----------------------
    def __init__(self, screen, scr_size, player, debug=False):
        # -- Parent constructor ---------------
        super().__init__(screen, scr_size, player, debug)
        self.plainLevel = True

    # ---------- Methods --------------------------
    def update(self):
        # Update all elements in level
        self.bodies.update()
        self.player.update(self.colliders, self.temporary)
        self.render_hud()
        if self.debug:
            self.debText = self.font.render("X: " + str(self.player.rect.x) + "; Y: "
                                           + str(self.player.rect.y) + "VelX: " + str(self.player.velX)
                                           + "; VelY: " + str(self.player.velY), True, COLORS['WHITE'])

        return False


# 2D Horizontal level's type class
class HorizontalLevel(Level):
    # ---------- Constructor ----------------------
    def __init__(self, screen, scr_size, player, debug=False):
        # -- Parent constructor ---------------
        super().__init__(screen, scr_size, player, debug)
        self.backgroundImg = image.load(self.root + "/images/astro.jpg").convert()
        self.plainLevel = False

    # ---------- Methods --------------------------
    def update(self):
        # Update all elements in level
        self.bodies.update()
        # Checks the condition for going out the level
        if self.player.coins < 10:
            self.player.update(self.colliders, self.temporary)
            self.render_hud()
            if self.debug:
                self.debText = self.font.render("X: " + str(self.player.rect.x) + "; Y: "
                                               + str(self.player.rect.y) + "VelX: " + str(self.player.velX)
                                               + "; VelY: " + str(self.player.velY), ANTIALIASING, COLORS['WHITE'])
                '''self.debText = self.font.render("X: " + str(self.player.rect.x) + "; Y: "
                                               + str(self.player.rect.y) + "; Obj: "
                                               + str(self.player.coins), ANTIALIASING, COLORS['WHITE'])'''

            return False

        else:
            return True


# All levels must inherit from 'HorizontalLevel' or 'Plain Level'
class Level1(HorizontalLevel):
    # ---------- Constructor ----------------------
    def __init__(self, screen, scr_size, player, debug=False):
        # -- Parent constructor ---------------
        super().__init__(screen, scr_size, player, debug)
        # Level data
        self.ID = "Doom Valley"
        self.levelInit = (50, 300)                     # Initial player position's coordinates
        # Level map structure
        self.structure = ["ffffffffffffffff",
                          "f            ccf",
                          "f   c       c  f",
                          "f   f       f  f",
                          "f     c    ff  f",
                          "f  f ffff fffc f",
                          "f c          f f",
                          "f fc  c c c    f",
                          "f  f           f",
                          "f              f",
                          "f              f",
                          "ffffffffffffffff"]
        # Populating level
        self.fill_level(self.structure)

        # Random location for snow flakes
        for i in range(50):     # 50
            # Snow instance
            flake = Snow(COLORS['WHITE'], 2, 2, self.scrSize)
            # We create a random placement
            flake.rect.x = randrange(self.scrSize[0])
            flake.rect.y = randrange(self.scrSize[1])
            # Then we add the flake to the block lists
            flake.firstX = flake.rect.x
            self.temporary.add(flake)
            self.bodies.add(flake)


# All levels must inherit from 'HorizontalLevel' or 'Plain Level'
class Level2(PlainLevel):
    # ---------- Constructor ----------------------
    def __init__(self, screen, src_size, player, debug=False):
        # -- Parent constructor ---------------
        super().__init__(screen, src_size, player, debug)
        # Level data
        self.ID = "The RING"
        self.levelInit = (50, 500)  # Initial player position's coordinates
        # -- Attributes -----------------------
        self.structure = ["fffffff ffffffff",
                          "f       fc c c f",
                          "f fffff fc c c f",
                          "fcfhf h     f  f",
                          "fcf        ff  f",
                          "fcff    f fff  f",
                          "fcf   h  c   f f",
                          "fcff  h        f",
                          "f     h    s   f",
                          "ffff ff        f",
                          "f    hf       ff",
                          "fffffffffffffff "]
        # Populating level
        self.fill_level(self.structure)
