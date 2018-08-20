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
        self.lang_dict = {
            "en": gettext.translation("PrimalRing_en", f"{ROOT}/resources/localization", languages=["en"]),
            "es": gettext.translation("PrimalRing_es", f"{ROOT}/resources/localization", languages=["es_ES"])
        }

    def set_lang(self, lang_code: str) -> None:
        try:
            self.LOGGER.info(f"Translating to \"{lang_code}\"")
            self.lang_dict[lang_code].install()
        except IOError as ie:
            self.LOGGER.error(f"Error at loading translation: {ie}")
