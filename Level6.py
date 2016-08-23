#!/usr/bin/env python

# ---------------------- IMPORTS ---------------------
# Python libs
# import pygame
from pygame import image, font, sprite
from random import randrange
# Own libs
# We could just import the Block module, but it's more reliable as is
from Block6 import Snow, Hero, Floor
from constants6 import WHITE, RED, BLUE, ROOT
''' This class manages all in terms of creating level structures
    and loading graphic and audio resources. Every level created
    has inheritance from this Level class.'''


class Level(object):
    # Globals
    root = ROOT

    # ---------- Constructor ----------------------
    # def __init__(self, screen, scr_size, root, debug=False):
    def __init__(self, screen, scr_size, debug=False):
        # -- Attributes -----------------------
        self.debug = debug                      # Flag for debugging into the game
        self.screen = screen                    # A reference for the main screen
        self.scr_size = scr_size                # The screen size
        # self.root = root
        self.coins = 0                          # Coins collected
        self.structure = []
        self.backgroundImg = image.load(self.root + "/images/astro.jpg").convert()
        self.font = font.SysFont('Calibri', 25, True, False)
        # self.ring = pygame.mixer.Sound("sounds/fart.ogg")
        # Sprite lists for the win!
        self.colliders = sprite.Group()  # Walls, platforms, floor, enemies, switches...
        self.temporary = sprite.Group()  # Coins, ammo, lifepoints...
        self.bodies = sprite.Group()     # All sprites (this is for render on the screen)
        self.hero = Hero(RED, 50, 50)
        self.bodies.add(self.hero)              # Appends the hero body for checking collisions
        # HUD elements
        self.coinText = self.font.render("Coins: " + str(self.coins), True, WHITE)
        self.lifeText = self.font.render("Life: " + str(self.hero.life), True, WHITE)
        # Debug
        if self.debug:
            self.coords = self.font.render("X: " + str(self.hero.rect.x)
                                           + "; Y: " + str(self.hero.rect.y), True, WHITE)

    # ---------- Methods --------------------------
    def update(self):
        # Update all elements in level
        # self.hero.update()
        self.bodies.update()
        # It merges all collisions done in two lists (False for avoiding automatic drop)
        solid = sprite.spritecollide(self.hero, self.colliders, False)
        weak = sprite.spritecollide(self.hero, self.temporary, True)
        for body in solid:
            if body.docs() == "Floor":
                # self.hero.velY = 0
                self.hero.stop_fall()
                self.hero.rect.y = body.rect.y - 50
            
        for body in weak:
            if body.docs() == "Snow":
                self.hero.life -= 1
                # self.ring.play()
                self.lifeText = self.font.render("Life: " + str(self.hero.life), True, WHITE)
        
        if self.debug:
            self.coords = self.font.render("X: " + str(self.hero.rect.x) + "; Y: "
                                           + str(self.hero.rect.y)
                                           + "VelX: " + str(self.hero.velX)
                                           + "; VelY: " + str(self.hero.velY), True, WHITE)
    
    def display(self):
        self.screen.blit(self.backgroundImg, [0, 0])
        self.bodies.draw(self.screen)
        self.screen.blit(self.coinText, [50, 50])		
        self.screen.blit(self.lifeText, [50, 70])
        if self.debug:
            self.screen.blit(self.coords, [500, 70])		


# All levels must inherit from 'Level'
class Level1(Level):
    # ---------- Constructor ----------------------
    # def __init__(self, screen, src_size, root, debug=False):
    def __init__(self, screen, src_size, debug=False):
        # -- Parent constructor ---------------
        # Level.__init__(self, screen, src_size, self.root, debug)
        Level.__init__(self, screen, src_size, debug)
        # self.lvlSize = (800,600)
        # -- Attributes -----------------------
        # self.scr_size[0] = 800
        # self.scr_size[1] = 600
        # -- Extra attributes -----------------
        self.structure = \
            [['f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f'],
             ['f', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'f'],
             ['f', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'f'],
             ['f', ' ', ' ', ' ', 'f', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'f', ' ', ' ', 'f'],
             ['f', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'f', 'f', ' ', ' ', 'f'],
             ['f', ' ', ' ', 'f', ' ', 'f', 'f', 'f', 'f', ' ', 'f', 'f', 'f', ' ', ' ', 'f'],
             ['f', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'f', ' ', 'f'],
             ['f', ' ', 'f', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'f'],
             ['f', 'h', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'f'],
             ['f', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'f'],
             ['f', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'f'],
             ['f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f']]
        # Populating level
        cnt_y = 0                                       # Initial Y-axis grid
        for row in self.structure:
            cnt_x = 0                                   # Initial X-axis grid
            for column in row:
                if column == 'f':                       # 'f' stands for 'Floor'
                    floor = Floor(BLUE, 50, 50)
                    floor.rect.x = cnt_x
                    floor.rect.y = cnt_y
                    self.colliders.add(floor)
                    self.bodies.add(floor)
                elif column == 'h':                     # 'h' stands for 'Hero'
                    # self.hero = Hero(RED, 50, 50)
                    self.hero.rect.x = cnt_x
                    self.hero.rect.y = cnt_y
                    # self.bodies.add(self.hero)

                cnt_x += 50                             # Increment X-axis for the next tile

            cnt_y += 50                                 # Increment Y-axis for the next tile

        # Random location for snow flakes
        for i in range(50):     # 50
            # Snow instance
            flake = Snow(WHITE, 2, 2, self.scr_size)
            # We create a random placement
            flake.rect.x = randrange(self.scr_size[0])
            flake.rect.y = randrange(self.scr_size[1])
            # Then we add the flake to the block lists
            flake.firstX = flake.rect.x
            self.temporary.add(flake)
            self.bodies.add(flake)
    
    # ------------ Methods ------------------------
