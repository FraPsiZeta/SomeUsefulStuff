from collaudo_hardware import *
from collaudo_software import *
from collaudo_esterno import *


if __name__ == '__main__':
    if "-h" in sys.argv or "-help" in sys.argv or "help" in sys.argv or "--help" in sys.argv:
        print("This will be the man page for the script")
        print("I need help!")
        sys.exit(0)

    c1 = CollaudoHardware()
    c2 = CollaudoSoftware()
    c3 = CollaudoEsterno()

    if len(sys.argv) == 1:
        '''Collaudo completo'''

        c1.make_full_collaudo()
        c2.make_full_collaudo()
        c3.make_full_collaudo()
    else:
        c1.make_partial_collaudo()   
        c2.make_partial_collaudo()   
        c3.make_partial_collaudo()   
