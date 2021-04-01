#!/usr/bin/env /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import os.path
import subprocess
import sys

import settings

sys.paht.insert( 1, "/opt/utils" )
from user_settings_exceptions import Errors

class GitSettingLoader:
  def __create_shell_session_config( self, aliases: list() ) -> str:
    shell_config_path = os.path.join( os.path.expanduser( '~' ), '.bash_aliases' )
    with open( shell_config_path, 'w' ) as f:
      for i in range( 0, len( aliases ) ):
        f.write( aliases[ i ] )
        if i < len( aliases ) - 1:
          f.write( '\n' )

    return shell_config_path

  def __exec_bash( self, path: str ) -> None:
    cmd = f'/bin/bash -c "source { path }"'
    try:
      ret = subprocess.run( cmd, shell = True, stdout = subprocess.PIPE )
      print( ret )
    except subprocess.CalledProcessError as exp:

      print( f"On executing { cmd } error occurred: { exp }" )
    except Exception as exp:
      print( f"Unexpected error: { exp } occurred on executing { cmd }" )

  def set_permanent_aliases( self ) -> None:
    git_aliases = [ f"alias { alias }='{ git_cmd }'" for alias, git_cmd in settings.GIT_CMD_ALIASES.items() ]
    shell_config = self.__create_shell_session_config( git_aliases )
    self.__exec_bash( shell_config )


if __name__ == '__main__':
    settings.init()
    git_settings = GitSettingLoader()
    git_settings.set_permanent_aliases()

