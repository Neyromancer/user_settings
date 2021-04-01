#!/usr/bin/env /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import os.path
import sys

def init():
    global CONFIG_PATH
    CONFIG_PATH = "/etc/user_settings/user_settings.conf"

    if not os.path.exists( CONFIG_PATH ) or not os.path.isfile( CONFIG_PATH ):
        print( f"{ CONFIG_PATH } does not exist. Fail to read." )
        sys.exit( 1 )

    global EXERNAL_MODULES_DIR
    EXERNAL_MODULES_DIR = "/opt/user_settings/external/"

    if not os.path.exists( EXERNAL_MODULES_DIR ) or not os.path.isdir( EXERNAL_MODULES_DIR ):
        print( f"{ EXERNAL_MODULES_DIR } does not exist. Fail to load modules." )
        sys.exit( 1 )
    elif not os.listdir( EXERNAL_MODULES_DIR ):
        print( f"Fail to load modules. Directory: { EXERNAL_MODULES_DIR } is empty." )
        sys.exit( 1 )

    LOG_DIR = "/var/log/user_settings/"
    if not os.path.exists( LOG_DIR ) or not os.path.isdir( LOG_DIR ):
        os.makedirs( LOG_DIR, exist_ok = True )

    global LOG_PATH
    LOG_PATH = os.path.join( LOG_DIR, "user_settings.log" )