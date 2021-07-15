#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass

from pygame.sprite import Sprite
from pytmx import TiledMap
from pygame import font, sprite, Surface
from models.Bodies.LavaBody import LavaBody
from models.Bodies.FloorBody import FloorBody
from models.Bodies.HoleBody import HoleBody
from models.Bodies.PlayerBody import PlayerBody
from models.Bodies.SavePointBody import SavePointBody
from models.Bodies.PlatformBody import PlatformBody
from models.Bodies.CoinBody import CoinBody
from models.Bodies.LifePowerUpBody import LifePowerUpBody
from constants import COLORS, ANTIALIASING, FLOOR_SIZE
from models.Bodies.StepableBody import StepableBody


class _LevelBase:
    def __init__(self, screen, scr_size: tuple, managers, player: PlayerBody, tilemap: TiledMap, debug: bool = False):
        """ This class manages all in terms of creating level structures and loading graphic and audio resources.
        Every level created has inheritance from this Level class.

        :param screen: A reference for the main screen
        :param scr_size: The screen size (Default: 600 * 800)
        :param managers:
        :param player:
        :param debug: Flag for debugging into the game """
        # -- Attributes -----------------------
        self.debug = debug
        self.screen = screen
        self.scrSize = scr_size
        self._managers = managers
        self.ID = None                              # Current level identifier
        self.next_id = None                         # The next level to show
        self._tilemap = tilemap
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

    def display(self) -> None:
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

    def set_theme(self) -> None:
        if self.musicTheme is not None:
            self._managers.sound.play_music(self.musicTheme)

    # ---------- Internal Methods --------------------------
    @dataclass
    class TmxBody:
        img: Surface = None
        name: str = ""
        width: int = 0
        height: int = 0
        x: int = 0
        y: int = 0
        img_list: list = list

    def _fill_tmx_level(self, structure: TiledMap) -> None:
        """ It fills all level gaps with elements taking a pattern

        :param structure: A string list which contains all elements available in a level (WIP) """
        floor_layer = structure.get_layer_by_name("Floor").id - 1
        items_layer = structure.get_layer_by_name("Items").id - 1
        for row in range(structure.width):
            for col in range(structure.height):
                floor_tile = self._build_tmx_body(row, col, floor_layer, structure)
                item_tile = self._build_tmx_body(row, col, items_layer, structure)
                if floor_tile is not None:
                    self._fill_tmx_floor(row, col, floor_tile, structure)
                if item_tile is not None:
                    self._fill_tmx_items(item_tile)

    def _fill_tmx_floor(self, row: int, col: int, tile: TmxBody, structure: TiledMap) -> None:
        body = None
        if "Floor" in tile.name:
            body = FloorBody(COLORS['BLUE'], tile.width, tile.height, self._managers)
            # We append the opposite level corners
            if (col == 0 and row == 0) or (col == structure.height - 1 and row == structure.width - 1):
                self.reference.append(body)
        elif "Hole" in tile.name:
            body = HoleBody(COLORS['BLACK'], tile.width, tile.height, self._managers)
        elif "Stepable" in tile.name:
            body = StepableBody(COLORS['BLACK'], tile.width, tile.height, self._managers)
        elif "YPlatform" in tile.name:
            init_point = [row, col]
            body = PlatformBody(COLORS['GREEN'], tile.width, tile.height, self._managers, init_point, 'Y')
        elif "XPlatform" in tile.name:
            init_point = [row, col]
            body = PlatformBody(COLORS['GREEN'], tile.width, tile.height, self._managers, init_point)
        elif "Lava" in tile.name:
            body = LavaBody(COLORS['RED'], tile.width, tile.height, self._managers)
            body.imageList = tile.img_list

        body.image = tile.img
        body.image.set_colorkey(COLORS['WHITE'])
        self._set_body(body, tile.x, tile.y, self._solid_group)

    def _fill_tmx_items(self, tile: TmxBody) -> None:
        if "SavePoint" in tile.name:
            body = SavePointBody(COLORS['WHITE'], tile.width, tile.height, self._managers)
            body.imageList = tile.img_list
            body.image = tile.img
            body.image.set_colorkey(COLORS['BLACK'])
            self._set_body(body, tile.x, tile.y, self._solid_group)
        elif "Coin" in tile.name:
            body = CoinBody(COLORS['ORANGE'], tile.width, tile.height, self._managers)
            body.image = tile.img
            body.image.set_colorkey(COLORS['WHITE'])
            self._set_body(body, tile.x, tile.y, self._weak_group)
        elif "LifePowerUp" in tile.name:
            body = LifePowerUpBody(COLORS['ORANGE'], tile.width, tile.height, self._managers)
            self._set_body(body, tile.x, tile.y, self._weak_group)
        
    def _build_tmx_body(self, row: int, col: int, layer_id: int, structure: TiledMap) -> TmxBody:
        image = structure.get_tile_image(row, col, layer_id)
        if image is not None:
            props = structure.get_tile_properties(row, col, layer_id)
            x = props["width"] * row
            y = props["height"] * col
            img_list = [structure.get_tile_image_by_gid(x.gid).convert() for x in props["frames"]]
            return self.TmxBody(image.convert(), props["Name"], props["width"], props["height"], x, y, img_list)

    def _set_body(self, body: Sprite, pos_x: int, pos_y: int, sprite_group: sprite.Group) -> None:
        body.rect.x = pos_x
        body.rect.y = pos_y
        sprite_group.add(body)
        self._bodies.add(body)

    def _scroll(self) -> None:
        """ It manages the level scrolling """
        self.player.rect.x = \
            self._scroll_on_corner(self.player.rect.x, self.scrSize[0], self.reference[1].rect.x + FLOOR_SIZE, 'x')
        self.player.rect.x = self._scroll_axis(self.player.rect.x, self.scrSize[0] / 2, 'x')
        self.player.rect.y = \
            self._scroll_on_corner(self.player.rect.y, self.scrSize[1], self.reference[1].rect.y + FLOOR_SIZE, 'y')
        self.player.rect.y = self._scroll_axis(self.player.rect.y, self.scrSize[1] / 2, 'y')

    def _scroll_on_corner(self, player_coordinate: int, screen_coordinate: int, self_ref_coordinate: int, axis):
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

    def _scroll_axis(self, player_coordinate: int, screen_midpoint: float, axis):
        """

        :param player_coordinate:
        :param screen_midpoint:
        :param axis: x: horizontal update; y: vertical update
        :return:
        """
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

    def _update_bodies(self, diff: float, axis: str):
        """

        :param diff:
        :param axis: x: horizontal update; y: vertical update
        :return:
        """
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
