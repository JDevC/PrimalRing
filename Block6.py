#!/usr/bin/env python

# ---------------------- IMPORTS ---------------------
from pygame import sprite, image, Surface
# from random import randrange
''' A parent class for all sprites in the game screen, such as the main player,
    all kind of platforms, enemies and so on.'''


# General Block sprite class
class Block(sprite.Sprite):
    # ---------- Constructor ----------------------
    def __init__(self, color, width, height):
        # -- Parent constructor ---------------
        super().__init__()                      # sprite.Sprite.__init__(self)
        self.name = "Block"
        self.velX = 0
        self.velY = 0
        # We create the block's surface
        self.image = Surface([width, height])
        # We fill this 'surface' with a color
        self.image.fill(color)
        # Set our transparent color
        # self.image.set_colorkey(WHITE)
        # self.image.set_colorkey((255, 0, 0))
        # We get the 'collider' box
        self.rect = self.image.get_rect()

        # Load the image
        # self.image = image.load("player.png").convert()
        # Draw the ellipse
        # pygame.draw.ellipse(self.image, color, [50, 50, width, height])

    # ---------- Methods --------------------------
    def docs(self):
        return self.name


class Snow(Block):
    # ---------- Constructor ----------------------
    def __init__(self, color, width, height, screen_size):
        super().__init__(color, width, height)  # Block.__init__(self, color, width, height)
        self.name = "Snow"
        self.screen_size = screen_size
        self.firstX = 0
        self.acc = 5

    # ---------- Methods --------------------------
    # Update method
    def update(self):
        self.rect.y += 1
        if self.rect.y > self.screen_size[1]:
            self.rect.y = -1

    # Function for falling snow flakes
    def bounce(self):
        if self.rect.x == self.firstX:
            pass
        else:
            # self.rect.x +=
            pass


# Class for ground floor tiles
class Floor(Block):
    # ---------- Constructor ----------------------
    def __init__(self, color, width, height):
        super().__init__(color, width, height)      # Block.__init__(self, color, width, height)
        self.name = "Floor"


# Class for ground tiles
class Hole(Block):
    # ---------- Constructor ----------------------
    def __init__(self, color, width, height):
        super().__init__(color, width, height)  # Block.__init__(self, color, width, height)
        self.name = "Hole"


# Class for the player character
class Player(Block):
    # ---------- Constructor ----------------------
    def __init__(self, color, width, height):
        super().__init__(color, width, height)      # Block.__init__(self, color, width, height)
        self.name = "Player"
        self.life = 100
        self.velY = .35
        self.maxFallVelocity = 10
        self.plainLevel = False                     # Enable/Disable horizontal gravity
        self.jumping = False
        # self.acc = 9

    # ---------- Methods --------------------------
    # Update method
    def update(self):
        self.rect.x += self.velX
        self.rect.y += self.velY
        if not self.plainLevel:
            self.fall()
        # print "X: " + str(self.rect.x) + "; Y: " + str(self.rect.y) + "; vX: "
        # + str(self.velX) + "; velY: " + str(self.velY)

    # X movement to the left
    def go_left(self):
        # print "Goin' left"
        self.velX = -3

    # X movement to the right
    def go_right(self):
        # print "Goin' right"
        self.velX = 3

    # Y up movement (Only used on plain levels)
    def go_up(self):
        self.velY = -3

    # Y down movement (Only used on plain levels)
    def go_down(self):
        self.velY = 3

    # Stop for the X axis
    def stop_x(self):
        # print "Stoppin'"
        self.velX = 0

    # Stop for the X axis
    def stop_y(self):
        # print "Stoppin'"
        self.velY = 0

    # Y movement for jumping
    def jump(self):
        # print "Jumpin'"
        if not self.jumping:
            self.velY = -10
            self.jumping = True

    # Stop for the Y axis
    def stop_fall(self):
        # print "Fall complete"
        self.velY = 0
        self.jumping = False

    # This is a simple gravity calculus for hero's fall velocity
    def fall(self):
        # print "Falling"
        self.velY += .35
        if self.velY > self.maxFallVelocity:
            self.velY = self.maxFallVelocity
