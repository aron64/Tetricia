# Tetricia
Tetris with multiplayer mode

Guidelines: https://www.dropbox.com/s/g55gwls0h2muqzn/tetris%20guideline%20docs%202009.zip?dl=0

# Software Requirements
* Python 3.5+
    * tkinter, ttk
    * pynput - pip install pynput
    * PIL - pip install pillow
* Runs on most OS with GUI and networking

# Usage
* Server
   * Make sure to have the correct local address as your HOST variable
   * Make sure your PORT is going to be accessible by the other players
   
* Client
   * Run gameobjects.py for Solo experience
   * Run main.py for multiplayer experience
      * Ensure you have set the correct ip:port address in the Connection Settings menu
      * type *!level n* to set the starting level for the next game
      * type *help.get* to find out about stuff

* Basic Controls
   * Arrow Left: Move left
   * Arrow Right: Move Right
   * Arrow Down: Soft Drop
   * Arrow Up: Rotate clockwise
   * Left Ctrl: Rotate counter-clockwise
   * Space: Hard Drop
   * C, Left shift: Hold
   * F11: Fullscreen mode *(multiplayer only)*
   * Escape: Exit Fullscreen mode *(multiplayer only)*

# HAVE FUN 
