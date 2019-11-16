#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pygame import font, sprite
from models.Bodies.LavaBody import LavaBody
from models.Bodies.FloorBody import FloorBody
from models.Bodies.HoleBody import HoleBody
from models.Bodies.SavePointBody import SavePointBody
from models.Bodies.PlatformBody import PlatformBody
from models.Bodies.CoinBody import CoinBody
from models.Bodies.LifePowerUpBody import LifePowerUpBody
from constants import COLORS, ANTIALIASING, COIN_SIZE, FLOOR_SIZE, LIFE_POWER_UP_SIZE


class _LevelBase:
    def __init__(self, screen, scr_size, managers, player, debug: bool = False):
        """ This class manages all in terms of creating level structures and loading graphic and audio resources.
        Every level created has inheritance from this Level class.

        :param screen: A reference for the main screen
        :param scr_size: The screen size
        :param managers:
        :param player:
        :param debug: Flag for debugging into the game """
        # -- Attributes -----------------------
        self.debug = debug
        self.screen = screen
        self.scrSize = scr_size
        self._managers = managers
        self.ID = None                              # A level identifier
        self.structure = []                         # Level structure map
        self.levelInit = [0, 0]                     # Level enter point
        self.reference = []                         # Level fixed references for scroll
        self.backgroundImg = None                   # Background image reference
        # HUD graphic elements
        self.hud = [self._managers.image.load_image(f'Life.png'),
                    self._managers.image.load_image(f'Energy.png'),
                    self._managers.image.load_image(f'Coin_Frames/coin.png')]
        for x in range(len(self.hud)):
            self.hud[x].set_colorkey(COLORS['WHITE'])

        self.font = font.SysFont('Calibri', 25, True, False)
        # Sprite lists for the win!
        self._solid_group = sprite.Group()              # Walls, platforms, floor, enemies, switches...
        self._weak_group = sprite.Group()               # Coins, ammo, lifepoints...
        self.player_display = sprite.Group()            # The player itself
        self.player = player
        self.player_display.add(self.player)
        self._bodies = sprite.Group()                # All sprites (this is for render on the screen)
        # Music
        self.musicTheme = None
        # Debug
        if self.debug:
            text = f'X: {self.player.rect.x}; Y: {self.player.rect.y}'
            self.debText = self.font.render(text, ANTIALIASING, COLORS['WHITE'])

    # ---------- Public Methods --------------------------
    def update(self) -> bool:
        pass

    def display(self):
        # We check if the level has a background image and blit it to the screen
        if self.backgroundImg is not None:
            self.screen.blit(self.backgroundImg, [0, 0])

        self._bodies.draw(self.screen)
        self.player_display.draw(self.screen)

        if self.hud is not None:
            self.screen.blit(self.hud[0], [50, 50])
            self.screen.blit(self.hud[1], [50, 80])
            self.screen.blit(self.hud[2], [50, 110])

        self.screen.blit(self.font.render(f': {self.player.life}', ANTIALIASING, COLORS['WHITE']), [80, 50])
        self.screen.blit(self.font.render(f': {self.player.energy}', ANTIALIASING, COLORS['WHITE']), [80, 80])
        self.screen.blit(self.font.render(f': {self.player.coins}', ANTIALIASING, COLORS['WHITE']), [80, 110])

        if self.debug:
            self.screen.blit(self.debText, [50, 560])

    def set_theme(self):
        if self.musicTheme is not None:
            self._managers.sound.play_music(self.musicTheme)

    # ---------- Internal Methods --------------------------
    def _fill_level(self, structure: list):
        """ It fills all level gaps with elements taking a pattern

        :param structure: A string list which contains all elements available in a level (WIP) """
        cnt_y = 0  # Initial Y-axis tile grid
        temp_row = 0
        for row in structure:
            cnt_x = 0  # Initial X-axis tile grid
            temp_col = 0
            for char in row:
                if char == "f":  # 'f' stands for 'Floor'
                    floor = FloorBody(COLORS['BLUE'], FLOOR_SIZE, FLOOR_SIZE, self._managers)
                    self._set_body(floor, cnt_x, cnt_y, self._solid_group)
                    # We append the opposite level corners
                    if cnt_y == 0 and cnt_x == 0:
                        self.reference.append(floor)
                    elif cnt_y == (len(structure) - 1) * FLOOR_SIZE and cnt_x == (len(structure[0]) - 1) * FLOOR_SIZE:
                        self.reference.append(floor)
                elif char == "h":  # 'h' stands for 'Hole'
                    if structure[temp_row - 1][temp_col] == ' ' or structure[temp_row - 1][temp_col] == 'c':
                        hole = HoleBody(COLORS['BLACK'], FLOOR_SIZE, FLOOR_SIZE, self._managers, "hole_metal")
                    elif structure[temp_row - 1][temp_col] == 'f':
                        hole = HoleBody(COLORS['BLACK'], FLOOR_SIZE, FLOOR_SIZE, self._managers, "hole_floor")
                    else:
                        hole = HoleBody(COLORS['BLACK'], FLOOR_SIZE, FLOOR_SIZE, self._managers)
                    self._set_body(hole, cnt_x, cnt_y, self._solid_group)
                elif char == "s":  # 's' stands for 'SavePoint'
                    save = SavePointBody(COLORS['WHITE'], FLOOR_SIZE, FLOOR_SIZE, self._managers)
                    self._set_body(save, cnt_x, cnt_y, self._solid_group)
                elif char == "c":  # 'c' stands for 'Coin'
                    coin = CoinBody(COLORS['ORANGE'], COIN_SIZE, COIN_SIZE, self._managers)
                    self._set_body(coin, cnt_x + 10, cnt_y + 10, self._weak_group)
                elif char == "p":  # 'p' stands for 'Platform on Y'
                    platform = PlatformBody(COLORS['GREEN'], FLOOR_SIZE, FLOOR_SIZE, self._managers, [cnt_x, cnt_y], 'Y')
                    self._set_body(platform, cnt_x, cnt_y, self._solid_group)
                elif char == "P":  # 'p' stands for 'Platform on X'
                    platform = PlatformBody(COLORS['GREEN'], FLOOR_SIZE, FLOOR_SIZE, self._managers, [cnt_x, cnt_y])
                    self._set_body(platform, cnt_x, cnt_y, self._solid_group)
                elif char == "l":  # 'l' stands for 'Lava'
                    lava = LavaBody(COLORS['RED'], FLOOR_SIZE, FLOOR_SIZE, self._managers)
                    self._set_body(lava, cnt_x, cnt_y, self._solid_group)
                elif char == "v":
                    life_power_up =\
                        LifePowerUpBody(COLORS['ORANGE'], LIFE_POWER_UP_SIZE, LIFE_POWER_UP_SIZE, self._managers)
                    self._set_body(life_power_up, cnt_x, cnt_y, self._weak_group)

                # Increment X-axis for the next tile
                cnt_x += FLOOR_SIZE
                temp_col += 1

            # Increment Y-axis for the next tile
            cnt_y += FLOOR_SIZE
            temp_row += 1

    def _set_body(self, body, pos_x, pos_y, sprite_group):
        body.rect.x = pos_x
        body.rect.y = pos_y
        sprite_group.add(body)
        self._bodies.add(body)

    def _scroll(self):
        """ It manages the level scrolling """
        self.player.rect.x = \
            self._scroll_on_corner(self.player.rect.x, self.scrSize[0], self.reference[1].rect.x + FLOOR_SIZE, 'x')
        self.player.rect.x = self._scroll_axis(self.player.rect.x, self.scrSize[0] / 2, 'x')
        self.player.rect.y = \
            self._scroll_on_corner(self.player.rect.y, self.scrSize[1], self.reference[1].rect.y + FLOOR_SIZE, 'y')
        self.player.rect.y = self._scroll_axis(self.player.rect.y, self.scrSize[1] / 2, 'y')

    def _scroll_on_corner(self, player_coordinate, screen_coordinate, self_ref_coordinate, axis):
        new_player_coord = player_coordinate
        if player_coordinate < 0:
            screen_midpoint = screen_coordinate / 2
            diff = screen_midpoint - player_coordinate
            new_player_coord = screen_midpoint
            self._update_bodies(diff, axis)
        elif player_coordinate > screen_coordinate:
            diff = self_ref_coordinate - screen_coordinate
            new_player_coord -= diff
            self._update_bodies(-diff, axis)

        return new_player_coord

    def _scroll_axis(self, player_coordinate, screen_midpoint, axis):
        new_player_coord = player_coordinate
        if player_coordinate < screen_midpoint:
            # The player is far from the beginning of the level
            self_ref = self.reference[0].rect.x if axis == 'x' else self.reference[0].rect.y
            if player_coordinate - self_ref > screen_midpoint:
                diff = screen_midpoint - player_coordinate
                new_player_coord = screen_midpoint
                self._update_bodies(diff, axis)
        # The player is located near to the end of the screen (going to the right)
        elif player_coordinate > screen_midpoint:
            # The player is far from the beginning of the level
            self_ref = self.reference[1].rect.x if axis == 'x' else self.reference[1].rect.y
            if self_ref + FLOOR_SIZE - player_coordinate > screen_midpoint:
                diff = player_coordinate - screen_midpoint
                new_player_coord = screen_midpoint
                self._update_bodies(-diff, axis)

        return new_player_coord

    def _update_bodies(self, diff, axis):
        if axis == 'x':
            for body in self._bodies:
                body.rect.x += diff
                if isinstance(body, PlatformBody):
                    body.initPoint[0] += diff
        elif axis == 'y':
            for body in self._bodies:
                body.rect.y += diff
                if isinstance(body, PlatformBody):
                    body.initPoint[1] += diff

    def _update_player_debug(self):
        player_pos = f'X: {self.player.rect.x}; Y: {self.player.rect.y}; '
        player_vel = f'VelX: {self.player.velX}; VelY: {self.player.velY}'
        self.debText = self.font.render(player_pos + player_vel, ANTIALIASING, COLORS['WHITE'])
