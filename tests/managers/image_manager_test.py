#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from constants import ROOT
from pygame import error
from managers.ImageManager import ImageManager

ROOT = "C:/Users/jcarl/PycharmProjects/PrimalRingProject/PrimalRing"


@pytest.fixture()
def image_manager_sut() -> ImageManager:
    return ImageManager()


def test_load_image_wrong_dir(image_manager_sut: ImageManager):
    # Test values
    bad_image_dir = "Partners.png"

    # Execution
    with pytest.raises(ArithmeticError):
        image_manager_sut.load_image(bad_image_dir)


def test_load_image(image_manager_sut: ImageManager):
    # Test values
    bad_image_dir = "foo"

    # Execution
    with pytest.raises(error):
        image_manager_sut.load_image(bad_image_dir)
