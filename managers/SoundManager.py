#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pygame import mixer
import logging
from constants import ROOT


class SoundManager:
    __slots__ = ['_mixer', '_soundDir', '_musicTracks', '_fxTracks', '_levelFxTracks']
    LOGGER = logging.getLogger(__name__)

    def __init__(self):
        """ This is a little manager class for all sound & music in game. All things involving sound and music
        handling should refer to the SoundManager in order to keep the code clean and easy to follow """
        mixer.pre_init(frequency=44100, size=16)
        self._mixer = mixer
        self._soundDir = f'{ROOT}/resources/sounds/'
        self._musicTracks = self._init_music_tracks_dict(f'{ROOT}/resources/music/')
        self._fxTracks = self._init_fx_tracks_dict(self._soundDir)
        self._levelFxTracks = {}

    # ------------- Public Methods -------------
    def get_fx_vol(self):
        return self._fxTracks.get('Select').get_volume()

    def set_fx_vol(self, value: float, track_name: str = None):
        """ Defines a new fx volume for all tracks or the specified one

        :param value: Volume value
        :param track_name: Defines the new volume for only this track """
        if track_name is None:
            for track in self._fxTracks.values():
                track.set_volume(value)
        else:
            self._fxTracks.get(track_name).set_volume(value)

    def set_level_tracks(self, tracks: {}) -> None:
        del self._levelFxTracks
        self._levelFxTracks = {name: self._mixer.Sound(f'{self._soundDir}{fx}') for name, fx in tracks.items()}

    def music_fadeout(self, seconds: int):
        self._mixer.music.fadeout(seconds)

    def get_music_vol(self) -> float:
        return self._mixer.music.get_volume()

    def set_music_vol(self, value) -> None:
        self._mixer.music.set_volume(value)

    def play_fx(self, name: str) -> None:
        self._fxTracks[name].play()

    def play_music(self, name: str, start: float = 0) -> None:
        self._mixer.music.load(self._musicTracks[name])
        self._mixer.music.play(-1, start)

    def pause_music(self, pause: bool = True) -> None:
        self._mixer.music.pause() if pause else self._mixer.music.unpause()

    def stop_music(self):
        self._mixer.music.stop()

    def panic(self):
        """ It stops the music module """
        self._mixer.music.stop()
        self._mixer.quit()

    # ------------- Internal Methods -------------
    @staticmethod
    def _init_music_tracks_dict(music_dir):
        return {'Main Theme': f'{music_dir}strike_the_earth.ogg',
                'Doom Valley': f'{music_dir}doom_valley.ogg',
                'The RING': f'{music_dir}the_ring.ogg'}

    def _init_fx_tracks_dict(self, sound_dir):
        return {'Select': self._mixer.Sound(f'{sound_dir}select.ogg'),
                'Accept': self._mixer.Sound(f'{sound_dir}accept.ogg'),
                'Cancel': self._mixer.Sound(f'{sound_dir}cancel.ogg'),
                'Coin': self._mixer.Sound(f'{sound_dir}coin.wav')}
