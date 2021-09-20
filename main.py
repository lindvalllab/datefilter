from ui import UserInterface

if __name__ == '__main__':
    ui = UserInterface(
        lambda a, b, c: print('a', a, 'b', b, 'c', c)
    )
    ui.run()
