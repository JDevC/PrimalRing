#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from managers.LocalizationManager import LocalizationManager


@pytest.fixture()
def localization_manager_sut() -> LocalizationManager:
    return LocalizationManager()


def test_set_lang(localization_manager_sut: LocalizationManager):
    pass
