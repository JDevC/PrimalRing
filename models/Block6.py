#!/usr/bin/env python3

# ---------------------- IMPORTS ---------------------
from pygame import sprite, image, mixer, Surface
from math import sqrt
from constants6 import GRAVITY, MAX_FALL_VELOCITY, COLORS, FPS, ROOT


class _Block(sprite.Sprite):
    def __init__(self, color, width, height):
        """
        A parent class for all sprites in the game screen, such as the main player,
        all kind of platforms, enemies and so on.

        :param color:
        :param width:
        :param height:
        """
        super().__init__()
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
    def get_rect(self):
        return self.rect


class _AnimatedBlock(_Block):
    def __init__(self, color, width, height):
        """
        It's alive! Class for animated blocks, with some additions (Animated is for textures, not for
        changing its position (at least for now...)

        :param color:
        :param width:
        :param height:
        """
        super().__init__(color, width, height)
        self.name = "AnimatedBlock"
        # Tile container and pointer on animation
        self.imageList = []
        self.imageListIndex = 0
        # Frame Rate
        self.fps = FPS
        # Delay for frame animations
        self.refresh = 0

    # ---------- Methods --------------------------
    def set_frames(self, origin, quantity=1):
        """
        Loads all tiles incoming from a specified folder

        :param origin: The tile folder and image name in the format '{folder}/{image}'
        :param quantity: Count of tiles for the animation
        :return: None
        """
        for i in range(quantity):
            self.imageList.append(image.load(f'{ROOT}/resources/images/{origin}{i+1}.png').convert())

    def update(self):
        """
        Updates the image every certain time

        :return: None
        """
        # We configure the refresh rating here
        if self.refresh < self.fps:
            self.refresh += self.fps / 2
        else:
            # We switch the current tile to next in a concrete sequence
            if self.imageListIndex < len(self.imageList) - 1:
                self.imageListIndex += 1
            else:
                self.imageListIndex = 0
            self.image = self.imageList[self.imageListIndex]
            self.image.set_colorkey(COLORS['BLACK'])
            # We reset the refresh state
            self.refresh = 0


class _Enemy(_Block):
    def __init__(self, color, width, height):
        """
        Evil army! This class is for all enemy objects (It will extend from
        _AnimatedBlock in a future; Still lacks tiles)

        :param color:
        :param width:
        :param height:
        """
        super().__init__(color, width, height)
        self.life = 0                           # Enemy's life count
        self.isDead = False                     # Enemy's state
        self.firstX = 0


class Platform(_Block):
    def __init__(self, color, width, height, init_point, axis='X'):
        """
        This block is so bored about being on the same point that he's going to move

        :param color:
        :param width:
        :param height:
        :param init_point:
        :param axis:
        """
        super().__init__(color, width, height)
        self.name = "Platform"
        self.initPoint = init_point
        self.velX = self.velY = 1
        # Movement limit
        self.maxRun = 50
        self.axis = axis

    # ------------ Methods ------------------------
    def update(self):
        # if self.refresh < self.fps:
        #     self.refresh += self.fps
        # else:
        # The current position it's still into the limits
        if self.maxRun >= abs(self.rect.x - self.initPoint[0]) \
                and self.maxRun >= abs(self.rect.y - self.initPoint[1]):
            # It's moving in the X or Y axis?
            if self.axis == 'X':
                self.rect.x += self.velX
            elif self.axis == 'Y':
                self.rect.y += self.velY
        elif self.maxRun < abs(self.rect.x - self.initPoint[0]):
            # We convert the velocity value to its opposite
            self.velX *= -1
            self.rect.x += self.velX
        elif self.maxRun < abs(self.rect.y - self.initPoint[1]):
            # We convert the velocity value to its opposite
            self.velY *= -1
            self.rect.y += self.velY

        # We reset the refresh rating
        # self.refresh = 0


class Snow(_Block):
    def __init__(self, color, width, height, screen_size):
        super().__init__(color, width, height)
        self.name = "Snow"
        self.screen_size = screen_size
        self.firstX = 0
        self.acc = 5

    # ---------- Methods --------------------------
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


class Floor(_Block):
    def __init__(self, color, width, height):
        """
        Class for ground floor tiles

        :param color:
        :param width:
        :param height:
        """
        super().__init__(color, width, height)
        self.name = "Floor"


class Lava(_AnimatedBlock):
    def __init__(self, color, width, height):
        """
        Class for ground lava tiles

        :param color:
        :param width:
        :param height:
        """
        super().__init__(color, width, height)
        self.name = "Lava"
        # Animation image frames
        self.set_frames('Lava_Frames/Lava', 10)
        self.image = self.imageList[self.imageListIndex]
        # We set a transparent color for the image
        self.image.set_colorkey(COLORS['BLACK'])


class Coin(_Block):
    def __init__(self, color, width, height):
        """
        Class for coins

        :param color:
        :param width:
        :param height:
        """
        super().__init__(color, width, height)
        self.name = "Coin"
        self.image = image.load(f'{ROOT}/resources/images/Coin_Frames/coin.png').convert()
        # We set a transparent color for the image
        self.image.set_colorkey(COLORS['WHITE'])


class Hole(_Block):
    def __init__(self, color, width, height, img=None):
        """
        Class for hole tiles

        :param color:
        :param width:
        :param height:
        :param img:
        """
        super().__init__(color, width, height)
        self.name = "Hole"
        if img is not None:
            self.image = image.load(f'{ROOT}/resources/images/plain_hole/{img}.png').convert()


class SavePoint(_AnimatedBlock):
    def __init__(self, color, width, height):
        """
        Class for saving point tiles

        :param color:
        :param width:
        :param height:
        """
        super().__init__(color, width, height)
        self.name = "SavePoint"
        # Animation image frames
        self.set_frames('SP_Frames/save_point', 12)
        self.image = self.imageList[self.imageListIndex]
        # We set a transparent color for the image
        self.image.set_colorkey(COLORS['BLACK'])


class Player(_Block):
    def __init__(self, color, width, height, save_file=None):
        """
        Class for the player character (It will extend from _AnimatedBlock in a future; Still lacks tiles)

        :param color:
        :param width:
        :param height:
        :param save_file:
        """
        super().__init__(color, width, height)
        # We set its conditions depending on the save file
        if save_file is not None:
            self.name = save_file['Name']
            self.life = save_file['Life'][0]
            self.maxLife = save_file['Life'][1]
            self.energy = save_file['Energy'][0]
            self.maxEnergy = save_file['Energy'][1]
            self.coins = save_file['Coins'][0]
            self.maxWallet = save_file['Coins'][1]
        else:
            self.name = "Player"
            self.coins = 5
            # These attributes could be higher across the game, by power-ups that increase this limits
            self.life = self.maxLife = 100
            self.energy = self.maxEnergy = 100
            self.maxWallet = 100
        # Insert here your favourite sound, and all coins will go 'tink' when you touch them!
        self.coinSound = mixer.Sound(f'{ROOT}/resources/sounds/coin.wav')
        self.maxFallVelocity = MAX_FALL_VELOCITY    # A limit to gravity acceleration
        self.saveFlag = False                       # Enable/Disable saving feature
        self.plainLevel = False                     # Enable/Disable horizontal gravity
        self.jumping = False                        # Jumping state flag
        self.isDead = False                         # Living state flag

    # ---------- Methods --------------------------
    def update(self, solid, weak):
        # Collecting all 'solid' boxes (they don't vanish for colliding)
        solid_boxes = solid
        # Collecting all 'weak' boxes (they'll disappear for colliding)
        weak_boxes = weak
        # Cleaning flags
        if self.saveFlag:
            self.saveFlag = False
        # ------- HORIZONTAL CHECKING -------------------
        # We move the player on the X axis
        self.rect.x += self.velX
        # We merge all collisions done in two lists (False for avoiding automatic drop)
        solid_collide_list = sprite.spritecollide(self, solid_boxes, False)
        weak_collide_list = sprite.spritecollide(self, weak_boxes, True)
        for body in solid_collide_list:
            if isinstance(body, Floor) or isinstance(body, Platform):
                # Moving to the right
                if self.velX > 0:
                    self.rect.right = body.get_rect().left
                # Moving to the left
                elif self.velX < 0:
                    self.rect.left = body.get_rect().right
            elif isinstance(body, Hole):
                if self.distance(self.rect, body.get_rect()) < body.rect.width * 0.75:
                    if self.rect.x > body.get_rect().x:
                        self.rect.x -= 2
                    elif self.rect.x < body.get_rect().x:
                        self.rect.x += 2
            elif isinstance(body, SavePoint):
                if self.distance(self.rect, body.get_rect()) < body.rect.width / 2:
                    self.saveFlag = True
            elif isinstance(body, Lava):
                self.life -= 1
                self.velY = -5

        for body in weak_collide_list:
            if isinstance(body, Snow):
                self.life -= 1
            elif isinstance(body, Coin):
                self.get_coin()

        # ------- VERTICAL CHECKING -------------------
        # We move the player on the Y axis
        self.rect.y += self.velY
        # We merge all collisions done in two lists (False for avoiding automatic drop)
        solid_collide_list = sprite.spritecollide(self, solid_boxes, False)
        weak_collide_list = sprite.spritecollide(self, weak_boxes, True)
        for body in solid_collide_list:
            if isinstance(body, Floor) or isinstance(body, Platform):
                # Wall under the player
                if self.velY > 0:
                    self.stop_fall()
                    self.rect.bottom = body.get_rect().top
                # Wall upon the player
                elif self.velY < 0:
                    self.stop_y()
                    self.rect.top = body.get_rect().bottom
            elif isinstance(body, Hole):
                if self.distance(self.rect, body.get_rect()) < body.rect.width * 0.75:
                    if self.rect.y > body.get_rect().y:
                        self.rect.y -= 2
                    elif self.rect.y < body.get_rect().y:
                        self.rect.y += 2
            elif isinstance(body, SavePoint):
                if self.distance(self.rect, body.get_rect()) < body.rect.width / 2:
                    self.saveFlag = True
            elif isinstance(body, Lava):
                self.life -= 1
                self.velY = -5

        for body in weak_collide_list:
            if isinstance(body, Snow):
                self.life -= 1
            elif isinstance(body, Coin):
                self.get_coin()

        if not self.plainLevel:
            self.fall()

        if self.life <= 0:
            self.isDead = True

    def get_coin(self):
        # It prevents us for taking more coins than we can get
        if self.coins < self.maxWallet:
            self.coins += 1
        self.coinSound.play()

    def go_left(self):
        self.velX = -3

    def go_right(self):
        self.velX = 3

    def go_up(self):
        """
        Y up movement (Only used on plain levels)
        """
        self.velY = -3

    def jump(self):
        """
        Y movement for jumping
        """
        if not self.jumping:
            self.velY = -10
            self.jumping = True

    def go_down(self):
        """
        Y down movement (Only used on plain levels)
        """
        self.velY = 3

    def stop_x(self):
        self.velX = 0

    def stop_y(self):
        self.velY = 0

    def stop_fall(self):
        self.velY = 0
        self.jumping = False

    # This is a simple gravity calculus for player's fall velocity
    def fall(self):
        self.velY += GRAVITY
        if self.velY > self.maxFallVelocity:
            self.velY = self.maxFallVelocity

    def distance(self, player, body):
        """ Calculates a distance between central points of the player and other bodies. It emulates the
            following formula:
                  _____________________________
            d = \/(x_2 - x_1)^2 + (y_2 - y_1)^2
        :param player:
        :param body:
        :return: Distance between central points of the player and other body
        """

        x_1 = player.centerx * 1.0
        y_1 = player.centery * 1.0
        x_2 = body.centerx * 1.0
        y_2 = body.centery * 1.0
        # Calculation time
        x_operator = (x_2 - x_1) * (x_2 - x_1)
        y_operator = (y_2 - y_1) * (y_2 - y_1)
        return sqrt(x_operator + y_operator)
