import menu

def fuck ():
    print(1+1)

a_menu = menu.Menu(10,10,0,0,True,5,False)
a_menu.add_item(0, 'first', fuck, breaking=False)

a_menu.display()