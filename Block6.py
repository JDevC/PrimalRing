#!/usr/bin/env python

# ---------------------- IMPORTS ---------------------
from pygame import sprite, image, mixer, Surface
from math import sqrt
from constants6 import GRAVITY, MAX_FALL_VELOCITY, COLORS
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
        # We get the 'collider' box
        self.rect = self.image.get_rect()

    # ---------- Methods --------------------------
    def docs(self):
        return self.name

    def getRect(self):
        return self.rect


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
            pass


# Class for ground floor tiles
class Floor(Block):
    # ---------- Constructor ----------------------
    def __init__(self, color, width, height):
        super().__init__(color, width, height)      # Block.__init__(self, color, width, height)
        self.name = "Floor"


# Class for coins
class Coin(Block):
    # ---------- Constructor ----------------------
    def __init__(self, color, width, height):
        super().__init__(color, width, height)  # Block.__init__(self, color, width, height)
        self.name = "Coin"
        self.image = image.load('images\\coin.png').convert()
        # We set a transparent color for the image
        self.image.set_colorkey(COLORS['WHITE'])


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
        self.coins = 9
        # Insert here your favourite sound, and all coins will 'tink' when you touch them!
        self.coinSound = mixer.Sound('sounds\\coin.wav')
        self.maxFallVelocity = MAX_FALL_VELOCITY
        self.plainLevel = False                     # Enable/Disable horizontal gravity
        self.jumping = False

    # ---------- Methods --------------------------
    # Update method
    def update(self, solid, weak):
        # Collecting all 'solid' boxes (they don't vanish for colliding)
        solid_boxes = solid
        # Collecting all 'weak' boxes (they disappear for colliding)
        weak_boxes = weak
        # ------- HORIZONTAL CHECKING -------------------
        # We move the player on the X axis
        self.rect.x += self.velX
        # We merge all collisions done in two lists (False for avoiding automatic drop)
        solid_collide_list = sprite.spritecollide(self, solid_boxes, False)
        weak_collide_list = sprite.spritecollide(self, weak_boxes, True)
        for body in solid_collide_list:
            if body.docs() == "Floor":
                # Moving to the right
                if self.velX > 0:
                    self.rect.right = body.getRect().left
                # Moving to the left
                elif self.velX < 0:
                    self.rect.left = body.getRect().right

            elif body.docs() == "Hole":
                if self.safe_distance(self.rect.centerx, self.rect.centery,
                                      body.getRect().centerx, body.getRect().centery) < body.rect.width:
                    if self.rect.x > body.getRect().x:
                        self.rect.x -= 2
                    elif self.rect.x < body.getRect().x:
                        self.rect.x += 2

        for body in weak_collide_list:
            if body.docs() == "Snow":
                self.life -= 1
            elif body.docs() == "Coin":
                self.coins += 1
                self.coinSound.play()

        # ------- VERTICAL CHECKING -------------------
        # We move the player on the Y axis
        self.rect.y += self.velY
        # We merge all collisions done in two lists (False for avoiding automatic drop)
        solid_collide_list = sprite.spritecollide(self, solid_boxes, False)
        weak_collide_list = sprite.spritecollide(self, weak_boxes, True)
        for body in solid_collide_list:
            if body.docs() == "Floor":
                # Wall under the player
                if self.velY > 0:
                    self.stop_fall()
                    self.rect.bottom = body.getRect().top
                # Wall upon the player
                elif self.velY < 0:
                    self.stop_y()
                    self.rect.top = body.getRect().bottom

            elif body.docs() == "Hole":
                if self.safe_distance(self.rect.centerx, self.rect.centery,
                                      body.getRect().centerx, body.getRect().centery) < body.rect.width:
                    if self.rect.y > body.getRect().y:
                        self.rect.y -= 2
                    elif self.rect.y < body.getRect().y:
                        self.rect.y += 2

        for body in weak_collide_list:
            if body.docs() == "Snow":
                self.life -= 1
            elif body.docs() == "Coin":
                self.coins += 1
                self.coinSound.play()

        if not self.plainLevel:
            self.fall()

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

    # This is a simple gravity calculus for player's fall velocity
    def fall(self):
        # print "Falling"
        self.velY += GRAVITY
        if self.velY > self.maxFallVelocity:
            self.velY = self.maxFallVelocity

    # Calculus for safe distance between the player and a hole
    def safe_distance(self, player_center_x, player_center_y, hole_center_x, hole_center_y):
        # It emulates the following formula:
        #        _____________________________
        #  d = \/(x_2 - x_1)^2 + (y_2 - y_1)^2
        x_1 = player_center_x * 1.0
        y_1 = player_center_y * 1.0
        x_2 = hole_center_x * 1.0
        y_2 = hole_center_y * 1.0
        # Calculation time
        x_operator = (x_2 - x_1)*(x_2 - x_1)
        y_operator = (y_2 - y_1) * (y_2 - y_1)
        return sqrt(x_operator + y_operator)

