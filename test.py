import menu, time

def fuck ():
    print(1+1)
    time.sleep(3)
    print(1+1)

x = ['1']
a_menu = menu.Menu(10,10,0,0,True,5,False)
b_menu = menu.Menu(10,10,0,0,True,4,True)
c_menu = menu.Menu(15,15,0,0,True,3,False)
a_menu.add_item(0,'first', 'simple', fuck, breaking=True)
a_menu.add_item(1,'sub', mode='link',menu_obj=b_menu)
b_menu.add_item(2,'sub', mode='link',menu_obj=c_menu)
a_menu.add_item(4, 'exit', 'exit')
b_menu.add_item(3, 'exit', 'exit')
a_menu.add_item(3,'edit', mode='edit', edit_target=x)

a_menu.display()

print(a_menu.Items[3]['mode'])
print(a_menu.Items[3]['edit_target'])
print(x)