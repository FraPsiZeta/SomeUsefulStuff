from collaudo import *

class CollaudoEsterno(Collaudo):
    def __init__(self):
        super().__init__()
        self.functions_names = {
                            "reset" : self.reset,
                            "usb" : self.usb,
                            "hdmi" : self.hdmi,
                            "lan" : self.lan,
                            "serial_usb" : self.serial_usb
                            } 
    
    def reset(self):
        print("Test per il funzionamento del pulsante Reset.")
        input("Premi Enter per continuare, poi premi Reset sul dispositivo.")
        print("Aspettando il reset..")
        flag = 0
        running = 0
        while True:
            asd = subprocess.check_output(("ping -c 1 %s &>/dev/null ; echo $?"%device_info_ssh["device_ssh_ip"]), shell=True).decode("utf-8").rstrip()
            if asd == "0":
                if flag == 0 or flag == 1:
                    if running < 10000:
                        flag = 1
                        running += 1
                        continue
                    else:
                        print("Time Limit: nel caso si pensi di non essere riusciti a riavviare in tempo si riprovi il test.")
                        return False
                else:
                    print("Il dispositivo è nuovamente acceso, continuo il collaudo...")
                    while True:
                        try:
                            subprocess.check_output(("sshpass -p %s ssh -o ConnectTimeout=10 -q "
                            "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null %s@%s ls"
                            %(device_info_ssh["device_ssh_passwd"], device_info_ssh["device_ssh_user"], device_info_ssh["device_ssh_ip"])).split())
                            return True
                        except:
                            running += 1
                            time.sleep(0.1)
                            if running > 2000:
                                print("Il server ssh del dispositivo non sembra riuscire ad attivarsi. Riprovare il collaudo.")
                                sys.exit(1)
                            continue
            elif asd == "2" or asd == "1":
                if flag == 1:
                    flag = 2
                    print("Il dispositivo si è riavviato, attendere...")
                    running = 0
                running += 1
                if running > 1000:
                    print("Il dispositivo non riesce a riaccendersi.")
                    return False
            else:
                print("Errore nel riavvio del dispositivo, riprovare il collaudo.")
                return False
            running += 1
        return False

    def usb(self):
        disks_before = self.send_ssh_command("lsusb | awk '{print $2}'")
        input("Inserire la chiavetta USB, poi premi il tasto Enter per continuare.") 
        print("Controllando...")
        time.sleep(3)
        disks_after = self.send_ssh_command("lsusb | awk '{print $2}'")
        return disks_after.splitlines() != disks_before.splitlines()

    def hdmi(self):
        flag = True
        while True:
            if flag == True:
                print("Collegare il monitor all'uscita HDMI e controllarne il funzionamento.\nFunziona correttamente? [si/no]:") 
            si_no = input("")
            if si_no == "si" or si_no == "Si" or si_no == "SI":
                return True
            elif si_no == "no" or si_no == "No" or si_no == "NO":
                return False
            else:
                print("Input non valido: digita 'si' o 'no':")
                flag = False
                continue

    def lan(self):
        print("Verififcare il funzionamenteo della porte LAN.")
        while True:
            input("Si inserisca il cavo nella porta LAN 1, poi si prema Enter.")
            time.sleep(4)
            lan_1 = self.send_ssh_command("ip a | grep eth0 | sed -n 's/.* state \\([^ ]*\\).*/\\1/p'")
            lan_2 = self.send_ssh_command("ip a | grep eth1 | sed -n 's/.* state \\([^ ]*\\).*/\\1/p'")
            if lan_2 == "UP" and lan_1 == "DOWN":
                print("Sembra che la LAN sia stata inserita nella porta LAN 2. Vuoi riprovare? [si/no]")
                si_no = input("")
                if si_no == "si" or si_no == "Si" or si_no == "SI":
                    continue
                else:
                    pass
            input("Si inserisca il cavo nella porta LAN 2, poi si prema Enter.")
            time.sleep(4)
            lan_2 = self.send_ssh_command("ip a | grep eth1 | sed -n 's/.* state \\([^ ]*\\).*/\\1/p'")
            return lan_1 == "UP" and lan_2 == "UP"
            
    
    def serial_usb(self):
        print("Verificare il funzionamento della porta USB -> seriale.")
        usb_before = subprocess.check_output("lsusb")
        input("Inserisci la seriale nella porta USB di questo terminale e premi Enter.")
        usb_after = subprocess.check_output("lsusb")
        # if usb_before.decode("utf-8").find("Serial") != -1:
        #     input("Sembra che la seriale fosse già collegata a questo terminale.\nScollegala e premi Enter per eseguire nuovamente il test")
        # else:
        return usb_after.decode("utf-8").find("Serial") != -1


if __name__ == '__main__':
    if len(sys.argv) == 1:
        full_collaudo = CollaudoEsterno()
        full_collaudo.make_full_collaudo()
    else:
        partial_collaudo = CollaudoEsterno()
        partial_collaudo.make_partial_collaudo()
