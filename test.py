import menu, time

def fuck ():
    print(1+1)
    time.sleep(3)
    print(1+1)
    

a_menu = menu.Menu(10,10,0,0,True,5,False)
b_menu = menu.Menu(10,10,0,0,True,4,True)
a_menu.add_item(0,'first', 'simple', fuck, breaking=True)
a_menu.add_item(1,'sub', mode='link',menu_obj=b_menu)
a_menu.display()