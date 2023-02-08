from ballyhoo import Ballyhoo


def main():
    open('tasks.json', 'a').close()
    bh = Ballyhoo()
    bh.mainloop()
    

if __name__ == '__main__':
    main()    
