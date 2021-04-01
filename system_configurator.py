#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import ConfigParser
import logging
import os
import os.path
import sys
import subprocess

import settings

sys.path.insert( 1, "/opt/utils" )
from user_settings_exceptions import Errors, ModuleNotFoundError, ModuleExecutionError

class UserSettingLoader:
  def __init__( self ):
    self.modules_path = settings.EXERNAL_MODULES_DIR
    self.log = settings.LOG_PATH
    self.modules = dict()

    logging.basicConfig( filename = self.log, format='%(asctime)-15s %(message)s', level=logging.INFO )
    self.logger = logging.getLogger( 'user_system_settings' )
    consoleHandler = logging.StreamHandler()
    self.logger.addHandler( consoleHandler )
    self.logger.info( "Set system user configuration" )

  def load_modules( self ):
    self.logger.info( "Start loading configuration modules" )
    config = ConfigParser()
    config.read( settings.CONFIG_PATH )

    modules = config.sections()
    for module in modules:
      if module != "BASE" and config[ module ].get( 'enabled', '0' ) == '1':
        module_name = config[ module ].get( 'name', None )
        module_path = os.path.join( self.modules_path, module_name )
        if not os.path.exists( module_path ) or not os.path.isfile( module_path ):
          self.logger.error( f"Module { module_name } not found" )
          continue

        module_options = dict()
        module_options[ 'name' ] = module_name
        module_options[ 'params' ] = config[ module ].get( 'params', None )
        self.modules[ config[ module ].get( 'order', 1 ) ] = module_options

      if self.modules:
        self.logger.info( f"Successfully loaded modules: { [ self.modules[ module ].get( 'name' ) for module in self.modules ] }" )
      else:
        self.logger.critical( "Fail to load modules" )
        raise ModuleNotFoundError

  def execute_modules( self ):
    self.logger.info( "Execute modules" )
    if not self.modules:
      self.logger.critical( "No modules loaded" )
      raise ModuleNotFoundError

    executed_modules = list()
    for module in self.modules:
      module_name = self.modules[ module ].get( 'name', None )
      module_path = os.path.join( self.modules_path, module_name )
      if not os.path.exists( module_path ) or not os.path.isfile( module_path ):
        self.logger.error( f"Module { module_name } not found" )
        continue

      ret = Errors.FAILURE.value
      cmd = f"python3 { module_path } { self.modules[ module ][ 'params' ] }"
      try:
        ret = subprocess.check_output( cmd, shell = True, stderr = subprocess.STDOUT )
      except subprocess.CalledProcessError as exp:

        self.logger.error( f"On starting module { module_name } error occured: { exp.stderr }" )
      except Exception as exp:
        self.logger.error( f"Unxepected error: { exp } occurred on calling { module_name }" )

      if ret == Errors.FAILURE.value or ret == Errors.START_FAILURE.value:
        self.logger.critical( f"{ module_name } failed" )
        break

      executed_modules.append( module_name )

    if executed_modules:
      self.logger.info( f"Successfully executed modules: { executed_modules }" )
    else:
      self.logger.critical( "Fail to load modules" )
      raise ModuleExecutionError

  def main( self ):
    try:
      self.load_modules()
    except ( ModuleNotFoundError, Exception ):
      self.logger.critical( "Fail to complete load user settings" )
      sys.exit( Errors.FAILURE.value )

    try:
      self.execute_modules()
    except Exception as exp:
      self.logger.critical( f"Fail to complete load user settings. Error: { exp }" )
      sys.exit( Errors.FAILURE.value )
    else:
      self.logger.info( "User setting loader finished." )


if __name__ == '__main__':
    settings.init()
    settings_loader = UserSettingLoader()
    settings_loader.main()
