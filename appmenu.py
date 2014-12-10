#!/usr/bin/python

import appindicator
import gtk
import os
from build_cache import Cache
import subprocess
import re
import string
cwd = os.getcwd()

class Indicator:

    def __init__(self,cache):
        self.a = appindicator.Indicator('appmenu', os.path.join(cwd,'appmenu.png'), appindicator.CATEGORY_APPLICATION_STATUS)
        self.a.set_status( appindicator.STATUS_ACTIVE )
        self.cache=cache
        cachedict=self.cache.get_cache()
        self.appdict=cachedict.get('appcache')
        self.applist=cachedict.get('allprograms')
        self.build_menu()       

        
    def lookupIcon(self,icon_name):
        icon_theme = gtk.icon_theme_get_default()
        icon = icon_theme.lookup_icon(icon_name, 48, 0)
        if icon:
            return icon.get_filename()
        else:
            return icon_theme.lookup_icon('gnome-terminal', 48, 0).get_filename()

    def rescan(self,item):
        cachedict=self.cache.create_cache()
        self.appdict=cachedict.get('appcache')
        self.applist=cachedict.get('allprograms')
        # self.appdict=self.cache.get_cache()
        self.build_menu()

    def build_menu(self):
        self.menu=gtk.Menu()       
        rescanitem=gtk.MenuItem('Rebuild Cache')
        rescanitem.connect('activate',self.rescan)
        self.menu.append(rescanitem)
        rescanitem.show()
        allprogramsitem=gtk.MenuItem('All Programs')
        self.menu.append(allprogramsitem)
        allprograms=self.applist
        sepitem=gtk.SeparatorMenuItem()
        self.menu.append(sepitem)
        sepitem.show()
        for category,programs in sorted(self.appdict.items()):
            categoryitem=gtk.MenuItem(category)
            categorymenu=gtk.Menu()
            categoryitem.set_submenu(categorymenu)
            self.menu.append(categoryitem)
            categoryitem.show()
            # allprograms.update(programs)
            for program in programs:
                name=program.get('name')
                programitem=gtk.ImageMenuItem(name)
                img = gtk.Image()
                img.set_from_file(self.lookupIcon(program.get('icon')))
                programitem.set_image(img)
                programitem.connect('activate',self.runProgram,program)
                categorymenu.append(programitem)
                programitem.show()
        # allprograms=sorted(list(allprograms))
        allprogramsmenu=gtk.Menu()
        allprogramsitem.set_submenu(allprogramsmenu)
        for program in allprograms:
            name=program.get('name')
            programitem=gtk.ImageMenuItem(name)
            img = gtk.Image()
            img.set_from_file(self.lookupIcon(program.get('icon')))
            programitem.set_image(img)
            programitem.connect('activate',self.runProgram,program)
            allprogramsmenu.append(programitem)
            programitem.show()

        allprogramsitem.show()
        self.a.set_menu(self.menu)

    def cleanup(self,executable):
        found_list=re.findall('%.',executable)
        cleaned = executable
        for found in found_list:
            cleaned=string.replace(executable,found,'')
        return cleaned

    def runProgram(self,item,program):
        # print self.lookupIcon(program.get('icon'))
        executable=self.cleanup(program.get('exec'))
        print executable
        if program.get('terminal')=='false':
            pid=subprocess.Popen(executable,shell=True)
                   
        else:
            print 'terminal'
            pid=subprocess.Popen(['gnome-terminal', '-x', executable])
        # self.running_processes.append(pid)




def main():
    cache=Cache()
    indicator=Indicator(cache)
    gtk.main()

if __name__ == '__main__':
    main()

