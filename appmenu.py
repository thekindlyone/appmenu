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

    def __init__(self,appcache):
        self.a = appindicator.Indicator('appmenu', os.path.join(cwd,'appmenu.png'), appindicator.CATEGORY_APPLICATION_STATUS)
        self.a.set_status( appindicator.STATUS_ACTIVE )
        self.menu=gtk.Menu()
        self.appcache=appcache
        self.build_menu()
        self.a.set_menu(self.menu)
        # self.running_processes=[]

    def build_menu(self):        
        for category,programs in sorted(self.appcache.items()):
            categoryitem=gtk.MenuItem(category)
            categorymenu=gtk.Menu()
            categoryitem.set_submenu(categorymenu)
            self.menu.append(categoryitem)
            categoryitem.show()
            for program in programs:
                name=program.get('name')
                programitem=gtk.MenuItem(name)
                programitem.connect('activate',self.runProgram,program)
                categorymenu.append(programitem)
                programitem.show()

    def cleanup(self,executable):
        found_list=re.findall('%.',executable)
        cleaned = executable
        for found in found_list:
            cleaned=string.replace(executable,found,'')
        return cleaned

    def runProgram(self,item,program):
        executable=self.cleanup(program.get('exec'))

        print executable
        if program.get('terminal')=='false':
            pid=subprocess.Popen(executable,shell=True)
                   
        else:
            print 'terminal'
            pid=subprocess.Popen(['gnome-terminal', '-x', executable])
        # self.running_processes.append(pid)




def main():
    appcache=Cache()
    indicator=Indicator(appcache.get_cache())
    gtk.main()

if __name__ == '__main__':
    main()

