#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gettext
import logging
from constants import ROOT


class LocalizationManager:
    LOGGER = logging.getLogger(__name__)

    def __init__(self):
        """
        This manager handles all involving in-game translations
        """
        localization_route = f"{ROOT}/resources/localization"
        try:
            print(localization_route)
            self.lang_dict = {
                "en": gettext.translation("PrimalRing_en", localization_route, languages=["en"]),
                "es": gettext.translation("PrimalRing_es", localization_route, languages=["es_ES"])
            }
        except FileNotFoundError as fnfex:
            self.LOGGER.error(fnfex.strerror)
            print(localization_route)

    def set_lang(self, lang_code: str) -> None:
        try:
            self.LOGGER.info(f"Translating to \"{lang_code}\"")
            self.lang_dict[lang_code].install()
        except IOError as ie:
            self.LOGGER.error(f"Error at loading translation: {ie}")
            self.lang_dict["en"].install()
