# curses_menu
A python module for creating CLI menu/user interface with curses. 


## Story 

I have been using curses to make some CLIs. I want to make my life easier by creating a menu module that based on curses. 

## Road Map

*v0.2.1* Item Type Update 5/?/19 (projected):
------------------------------

Update Wiki

**Future**: let user to add costumize text verification function for edit mode.

**Future**: add color support?

**Future**: allow use to add text to the menu

**Future**: more costumize options

**?**: bug fix

*v0.2.0* Item Type Update 4/18/19:
------------------------------

**Feature**: User now can make the item operate in 4 different mode:
1. *Simple mode*: User can supply the item with a function. When the item is selected in the menu, the supplied function will be executed
2. *Link mode*: User can supply the item with a menu object. When the item is selected in the menu, it will display the supplied menu. When exit the supplied menu, it will return the previouse menu.
3. *Edit mode*: User can supply the item with a variable. The variable will display within the menu. When the item is selected, user can edit the supplied variable.
4. *Exit mode*: When the item is selected, it will exit the current menu.

**Bug**: minor bug fixed

*v0.1.0* Useable Version 4/11/19:
------------------------------

**Feature**: User is able to create Menu object and create item that need to be display in the menu

**Feature**: User can call display() method to display the menu; the display is handle by the curses.wrapper()
