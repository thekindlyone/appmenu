# Appmenu - a start menu like program menu for ubuntu

##Dependencies:
python-appindicator,python-gio,python-gmenu       
to install via apt,       
```sudo apt-get install python-appindicator```         
```sudo apt-get install python-gio```        
```sudo apt-get install python-gmenu```         
##Instructions
1. enable icons in menus by running     
    ```gsettings set org.gnome.desktop.interface menus-have-icons true```       
    and logout and log back in.     
2. git clone this repository or download zip and extract directory
3. cd to appmenu-master and run ```python appmenu.py```

Here is a demonstration:     
https://www.youtube.com/watch?v=6uVUNFVIli4