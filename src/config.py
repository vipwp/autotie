#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 smallevilbeast
#
# Author:     smallevilbeast <houshao55@gmail.com>
# Maintainer: smallevilbeast <houshao55@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gobject    
from xdg_support import get_config_file
from ConfigParser import RawConfigParser as ConfigParser
from logger import Logger
from constant import CONFIG_FILENAME


class Config(gobject.GObject, Logger):
    __gsignals__ = {
        "config-changed" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                            (gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING))
        }
    
    def __init__(self):
        gobject.GObject.__init__(self)
        self._config       = ConfigParser()
        self.remove_option = self._config.remove_option
        self.has_option    = self._config.has_option
        self.add_section   = self._config.add_section
        self.getboolean    = self._config.getboolean
        self.getint        = self._config.getint
        self.getfloat      = self._config.getfloat
        self.options       = self._config.options
        
        # Load default configure.
        for section, items in self.__get_default().iteritems():
            self.add_section(section)
            for key, value in items.iteritems():
                self._config.set(section, key, value)
                
    def load(self):            
        ''' Load config items from the file. '''
        self._config.read(get_config_file(CONFIG_FILENAME))
        
    
    def get(self, section, option, default=""):
        ''' specified the section for read the option value. '''
        try:
            return self._config.get(section, option)
        except:
            return default
            
    def set(self, section, option, value):        
        if not self._config.has_section(section):
            self.logdebug("Section \"%s\" not exist. create...", section)
            self.add_section(section)
        self._config.set(section, option, value)    
        self.emit("config-changed", section, option, value)
        
    def write(self):    
        ''' write configure to file. '''
        filename = get_config_file("config")
        f = file(filename, "w")
        self._config.write(f)
        f.close()
        
    def __get_default(self):    
        return {
            "window" : {
                },
            }
        
    
config = Config()    
