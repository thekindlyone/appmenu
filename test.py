import gobject
import gtk
import appindicator

def clean_quit(w):
print "in quit"
gtk.main_quit()

if __name__ == "__main__":
ind = appindicator.Indicator ("example-simple-client",
"indicator-messages",
appindicator.CATEGORY_APPLICATION_STATUS)
ind.set_status (appindicator.STATUS_ACTIVE)
ind.set_attention_icon ("indicator-messages-new")

# create a menu
menu = gtk.Menu()
listMenu=gtk.Menu()
listItems=gtk.MenuItem("Show List")
listItems.set_submenu(listMenu)
inews = gtk.MenuItem("Import")
inews.show()
listMenu.append(inews)
menu.append(listItems)
listItems.show()
# create some
menu_items=gtk.MenuItem("Quit")
menu.append(menu_items)
menu_items.connect("activate", clean_quit)
menu_items.show()
ind.set_menu(menu)

gtk.main()