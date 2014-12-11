#!/usr/bin/python

import appindicator
import gtk
import os
from build_cache import Cache
import gio
import re
import string
cwd = os.getcwd()

class Indicator:

    def __init__(self,cache):
        self.a = appindicator.Indicator('appmenu', self.lookupIcon('preferences-desktop-remote-desktop'), appindicator.CATEGORY_APPLICATION_STATUS)
        self.a.set_status( appindicator.STATUS_ACTIVE )
        self.cache=cache        
        self.appdict=self.cache.get_cache()        
        self.build_menu()       
        
    def lookupIcon(self,icon_name):
        icon=''
        icon_theme = gtk.icon_theme_get_default()
        if icon_name:            
            icon = icon_theme.lookup_icon(icon_name, 48, 0)
        if icon:
            return icon.get_filename()
        else:
            return icon_theme.lookup_icon('gnome-terminal', 48, 0).get_filename()

    def rescan(self,item):        
        self.appdict=self.cache.create_cache()
        self.build_menu()

    def build_menu(self):
        self.menu=gtk.Menu()       
        rescanitem=gtk.MenuItem('Rebuild Cache')
        rescanitem.connect('activate',self.rescan)
        self.menu.append(rescanitem)
        rescanitem.show()
        for category,programs in sorted(self.appdict.items()):
            categoryitem=gtk.ImageMenuItem(category[0])
            img=gtk.Image()
            img.set_from_file(self.lookupIcon(category[1]))
            categoryitem.set_image(img)
            categorymenu=gtk.Menu()
            categoryitem.set_submenu(categorymenu)
            self.menu.append(categoryitem)
            categoryitem.show()            
            for program in programs:
                name=program.get('name')
                programitem=gtk.ImageMenuItem(name)
                img = gtk.Image()
                img.set_from_file(self.lookupIcon(program.get('icon')))
                programitem.set_image(img)
                programitem.connect('activate',self.runProgram,program)
                categorymenu.append(programitem)
                programitem.show()
        self.a.set_menu(self.menu)

    def runProgram(self,item,program):
        info=gio.unix.desktop_app_info_new_from_filename(program.get('exec'))        
        info.launch()        

def main():
    cache=Cache()
    indicator=Indicator(cache)
    gtk.main()

if __name__ == '__main__':
    main()
