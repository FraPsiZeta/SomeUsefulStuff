import signal
from collaudo_hardware import *
from collaudo_software import *
from collaudo_esterno import *

def exit_cool(signum, frame):
    print("\nUscendo dal programma..")
    sys.exit(1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_cool)
    
    subprocess.Popen(["clear"])
    
    c1 = CollaudoHardware()
    c2 = CollaudoSoftware()
    c3 = CollaudoEsterno()

    c1.make_full_collaudo()
    c2.make_full_collaudo()
    c3.make_full_collaudo()
    
    Collaudo.create_attachment()
    Collaudo.put_results_mysql_db()
    
    # Collaudo.put_results_mysql_db()
