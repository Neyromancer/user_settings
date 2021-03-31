#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum

class Errors( Enum ):
  SUCCESS = 0
  WARINING = 1
  FAILURE = 2
  START_FAILURE = 3

class ModuleNotFoundError( Exception ):
  pass

class ModuleExecutionError( Exception ):
  pass