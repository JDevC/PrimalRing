#!/usr/bin/env python3
from pygame import mixer
from constants import ROOT


class SoundManager:
    __slots__ = ['_soundDir', '_musicTracks', '_fxTracks', '_levelFxTracks']

    def __init__(self):
        """ This is a little manager class for all sound & music in game. All things involving sound and music
        handling should refer to the SoundManager in order to keep the code clean and easy to follow """
        mixer.pre_init(frequency=44100, size=16)
        self._soundDir = f'{ROOT}/resources/sounds/'
        music_dir = f'{ROOT}/resources/music/'
        self._musicTracks = {'Main Theme': f'{music_dir}strike_the_earth.ogg',
                             'Doom Valley': f'{music_dir}doom_valley.ogg',
                             'The RING': f'{music_dir}the_ring.ogg'}
        self._fxTracks = {'Select': mixer.Sound(f'{self._soundDir}select.ogg'),
                          'Accept': mixer.Sound(f'{self._soundDir}accept.ogg'),
                          'Cancel': mixer.Sound(f'{self._soundDir}cancel.ogg'),
                          'Coin': mixer.Sound(f'{self._soundDir}coin.wav')}
        self._levelFxTracks = {}

    def get_fx_vol(self):
        return self._fxTracks.get('Select').get_volume()

    def set_fx_vol(self, value, track_name=None):
        """ Defines a new fx volume for all tracks or the specified one

        :param value: Volume value
        :param track_name: Defines the new volume for only this track """
        if track_name is None:
            for track in self._fxTracks.values():
                track.set_volume(value)
        else:
            self._fxTracks.get(track_name).set_volume(value)

    def set_level_tracks(self, tracks: {}) -> None:
        self._levelFxTracks = {name: mixer.Sound(f'{self._soundDir}{fx}') for name, fx in tracks.items()}

    @staticmethod
    def get_music_vol():
        return mixer.music.get_volume()

    @staticmethod
    def set_music_vol(value):
        """ Defines a music volume

        :param value: Volume value """
        mixer.music.set_volume(value)

    def play_fx(self, name):
        self._fxTracks[name].play()

    def play_music(self, name, start=0):
        mixer.music.load(self._musicTracks[name])
        mixer.music.play(-1, start)

    @staticmethod
    def pause_music(pause=True):
        mixer.music.pause() if pause else mixer.music.unpause()

    @staticmethod
    def stop_music():
        mixer.music.stop()

    @staticmethod
    def panic():
        """ It stops the music module """
        mixer.music.stop()
        mixer.quit()
