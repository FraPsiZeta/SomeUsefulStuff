from collaudo_hardware import *
from collaudo_software import *
from collaudo_esterno import *


if __name__ == '__main__':
    subprocess.Popen(["clear"])

    c1 = CollaudoHardware()
    c2 = CollaudoSoftware()
    c3 = CollaudoEsterno()


    c1.make_full_collaudo()
    c2.make_full_collaudo()
    c3.make_full_collaudo()
