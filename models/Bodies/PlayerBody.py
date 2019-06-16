#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from math import sqrt
from pygame.sprite import spritecollide
from .HoleBody import HoleBody
from .FloorBody import FloorBody
from .LavaBody import LavaBody
from .PlatformBody import PlatformBody
from .SavePointBody import SavePointBody
from models.Bodies._BodyBase import _BodyBase
from managers import ImageManager
from managers import SoundManager
from constants import GRAVITY, MAX_FALL_VELOCITY
from dataclasses import dataclass


class PlayerBody(_BodyBase):
    def __init__(self, color: [], width: int, height: int, sound_manager: SoundManager, image_manager: ImageManager, save_file=None):
        """ Class for the player character (It will extend from _AnimatedBlock in a future; Still lacks tiles)

        :param color:
        :param width:
        :param height:
        :param sound_manager:
        :param save_file: """
        super().__init__(color, width, height, image_manager)
        self.soundMan = sound_manager
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

        self.maxFallVelocity = MAX_FALL_VELOCITY    # A limit to gravity acceleration
        self.saveFlag = False                       # Enable/Disable saving feature
        self.plainLevel = False                     # Enable/Disable horizontal gravity
        self.direction = self.Direction()
        self.jumping = False                        # Jumping state flag
        self.isDead = False                         # Living state flag

    @dataclass
    class Direction:
        up: bool = False
        down: bool = False
        left: bool = False
        right: bool = False

    # ---------- Public Methods --------------------------
    def update(self, solid: [], weak: []):
        if self.saveFlag:
            self.saveFlag = False

        self._calc_vel()
        self._do_horizontal_checking(solid, weak)
        self._do_vertical_checking(solid, weak)

        if not self.plainLevel:
            self.fall()

        self.isDead = self.life <= 0 or self.rect.y > 900

    def stop_y(self):
        self.velY = 0

    def stop_fall(self):
        self.velY = 0
        self.jumping = False

    def fall(self):
        """ This is a simple gravity calculus for player's fall velocity """
        # This avoids the "jumping on air" bug
        if not self.jumping and self.velY > 0.7:
            self.jumping = True

        self.velY += GRAVITY
        if self.velY > self.maxFallVelocity:
            self.velY = self.maxFallVelocity

    def distance(self, body):
        """ Calculates a distance between central points of the player and other bodies. It emulates the
        following formula:
                  _____________________________
            d = \/(x_2 - x_1)^2 + (y_2 - y_1)^2
        :param body:
        :return: Distance between central points of the player and other body """
        x_1 = self.rect.centerx * 1.0
        y_1 = self.rect.centery * 1.0
        x_2 = body.centerx * 1.0
        y_2 = body.centery * 1.0
        # Calculation time
        x_operator = (x_2 - x_1) * (x_2 - x_1)
        y_operator = (y_2 - y_1) * (y_2 - y_1)

        return sqrt(x_operator + y_operator)

    # ---------- Internal Methods --------------------------
    def _do_horizontal_checking(self, solid_boxes, weak_boxes):
        self.rect.x += self.velX
        # We divide all collisions done in two lists (False for avoiding automatic drop)
        solid_collide_list = spritecollide(self, solid_boxes, False)
        for body in solid_collide_list:
            if isinstance(body, FloorBody):
                dist = self.rect.centerx - body.rect.centerx
                if 45 > dist > 0:
                    # Moving to the left
                    self.rect.left = body.rect.right
                elif -45 < dist < 0:
                    # Moving to the right
                    self.rect.right = body.rect.left
            elif isinstance(body, PlatformBody):
                # Moving to the right
                # if self.velX > 0:
                #    self.rect.right = body.rect.left
                # Moving to the left
                # elif self.velX < 0:
                #    self.rect.left = body.rect.right
                if self.velX == 0:
                    # Platforms collides with the player
                    if body.velY < 0:
                        # Platform's moving up
                        self.rect.bottom = body.rect.top
                    elif body.velY > 0:
                        # Platform's moving down
                        self.stop_y()
                        self.rect.top = body.rect.bottom
                else:
                    pass
            elif isinstance(body, HoleBody):
                if self.distance(body.rect) < body.rect.width * 0.75:
                    if self.rect.x > body.rect.x:
                        self.rect.x -= 2
                    elif self.rect.x < body.rect.x:
                        self.rect.x += 2
            elif isinstance(body, SavePointBody):
                body.react(self)
            elif isinstance(body, LavaBody):
                body.react(self)

        self._manage_weak_collisions(weak_boxes)

    def _do_vertical_checking(self, solid_boxes, weak_boxes):
        self.rect.y += self.velY
        # We divide all collisions done in two lists (False for avoiding automatic drop)
        solid_collide_list = spritecollide(self, solid_boxes, False)
        for body in solid_collide_list:
            if isinstance(body, FloorBody):
                dist = self.rect.centery - body.rect.centery
                if -45 < dist < 0:
                    self._rigid_body_under(body)
                elif 45 > dist > 0:
                    self._rigid_body_upon(body)
            elif isinstance(body, PlatformBody):
                if self.velY > 0:
                    self._rigid_body_under(body)
                elif self.velY < 0:
                    self._rigid_body_upon(body)
            elif isinstance(body, HoleBody):
                if self.distance(body.rect) < body.rect.width * 0.75:
                    if self.rect.y > body.rect.y:
                        self.rect.y -= 2
                    elif self.rect.y < body.rect.y:
                        self.rect.y += 2
            elif isinstance(body, SavePointBody):
                body.react(self)
            elif isinstance(body, LavaBody):
                body.react(self)

        self._manage_weak_collisions(weak_boxes)

    def _rigid_body_under(self, body):
        self.stop_fall()
        self.rect.bottom = body.rect.top

    def _rigid_body_upon(self, body):
        self.stop_y()
        self.rect.top = body.rect.bottom

    def _manage_weak_collisions(self, boxes):
        bodies = spritecollide(self, boxes, True)
        for body in bodies:
            body.react(self)

    def _jump(self):
        if not self.jumping:
            self.velY = -10
            self.rect.y -= 0.1
            self.jumping = True

    def _calc_vel(self):
        if self.plainLevel:
            if self.direction.up:
                self.velY = -3
            elif self.direction.down:
                self.velY = 3
            else:
                self.stop_y()
        else:
            if self.direction.up and not self.jumping:
                """self.velY = -10
                self.jumping = True"""
                self._jump()

        if self.direction.right:
            self.velX = 3
        elif self.direction.left:
            self.velX = -3
        else:
            self.velX = 0
