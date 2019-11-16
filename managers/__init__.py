#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .LocalizationManager import LocalizationManager
from .ManagerDataClass import ManagerDataClass

managers = ManagerDataClass()
managers.localization = LocalizationManager()
