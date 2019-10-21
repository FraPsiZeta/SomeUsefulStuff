import os
import time
import sys
import subprocess

from logging_collaudo import *
from interactive_menu import *
from sql_collaudo import *
from conf_file import *
from conf_file_ssh import *

class Collaudo:
    def __init__(self):
        self.test_values = {
                            "hdd" : None,
                            "ram" : None,
                            "usb" : None,
                            "hdmi" : None,
                            "serial_usb" : None,
                            "cpu" : None,
                            "swkit" : None,
                            "smartalim_fw" : None,
                            "bios" : None,
                            "reset" : None,
                            "ups" : None,
                            "lan" : None
                            }
        self.start()
        self.device_name = "MEDIA3N_SERVER"


    def custom_test(self, ssh_command="", test_type="is_equal", verify_value="42"):
        '''Funzione che permette di compiere test più o meno arbitrari.
        Il parametro ssh_command richiede il comando da inviare al device.
        Il parametro test_type può essere:
            - "is_equal"
            - ""
        Il parametro verify_value ideve essere una stringa e fa riferimento
        al test "is_equal".'''
        tests = {
                "is_equal" : self.is_equal
                }
        return tests[test_type](ssh_command, verify_value)

    def is_equal(self, command, value):
        '''Ritorna True se il risultato di "command" è uguale a "value".'''
        return self.send_ssh_command(command) == value

    # def insert_info(self):
    #     '''Funzione che chiede al collaudatore alcune informazionii extra'''
    #     while True:
    #         product_code = input("Inserire codice prodotto: ")
    #         tester_name = input("Inserire nome collaudatore: ")
    #         print("Questi sono i dati inseriti:")
    #         print("Codice Prodotto PF: %s"%product_code)
    #         print("Nome collaudatore: %s"%tester_name)
    #         print("I dati sono corretti? [si/no]")
    #         input("")
    #         if si_no == "si" or si_no == "Si" or si_no == "SI":
    #             break
    #         else:
    #             continue
    
    def send_ssh_command(
            self, command, 
            SSH_OPTIONS="-o ConnectTimeout=10 -q -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null", 
            ssh_ip=device_info_ssh["device_ssh_ip"], 
            ssh_user=device_info_ssh["device_ssh_user"],
            ssh_passwd=device_info_ssh["device_ssh_passwd"]):
        '''Ritorna l'output di "command" richiesto via ssh all'indirizzo "ssh_ip" con passwd "ssh_passwd" come stringa.
        In caso di mancata connessione viene riprovato fino a 3 volte prima di uscire dal programma.'''
        arg_list = command.split()
        arg_list.insert(0, "%s@%s"%(ssh_user, ssh_ip))
        arg_list[0:0] = SSH_OPTIONS.split()
        arg_list[0:0] = ("sshpass -p %s ssh"%ssh_passwd).split()
        flag = 0
        while True:
            try:
                ssh_output = subprocess.check_output([*arg_list])
                break
            except subprocess.CalledProcessError as ssh_error:
                print("Errore: Impossibile connettersi al server SSH.")
                if flag == 3:
                    print("Esco dal programma...")
                    sys.exit(1)
                print("Nuovo tentativo di connessione in corso: tentativi rimasti %d"%(3-flag))
                flag += 1
                time.sleep(5)
                continue
        return ssh_output.decode("utf-8").rstrip()

    def get_config_from_db(self):
        db = MySQL()
        db.select(self.device_name, "some_value")
        #Da completare una volta disponibile il db effettivo
        


    def run_once(f):
        def wrapper(*args, **kwargs):
            if not wrapper.has_run:
                wrapper.has_run = True
                return f(*args, **kwargs)
        wrapper.has_run = False
        return wrapper

    @run_once
    def start(self):
        if len(sys.argv) == 1:
            print("Inizio collaudo in modalità interattiva!")
            while True:
                global menu
                menu = Menu()
                print("\nI dati inseriti sono i seguenti:")
                print("Test da effettuare:")
                for t in menu.answer['tests']:
                    print("- ", t.upper())
                print("Nome collaudatore: ", menu.answer['tester_name'])
                print("Postazione: ", menu.answer['test_station'])
                print("Codice Prodotto: ", menu.answer['product_code'])
                si_no = input("I dati inseriti sono corretti? [si/no] ")
                if si_no == "si" or si_no == "Si" or si_no == "SI":
                    print("")
                    break
                else:
                    continue

    
    def nicer_output(self, return_value):
        if return_value == True:
            return "Successo!"
        elif return_value == False:
            return "FALLITO!"
        else:
            return "ERRORE: ripetere il Test."

    def make_full_collaudo(self):
        for func_names in self.functions_names:
            if func_names in self.functions_names and func_names in menu.answer['tests']:
                tmp_return_value = self.functions_names[func_names]()
                self.test_values[func_names] = tmp_return_value
                print("Test", func_names.upper(), ":", self.nicer_output(tmp_return_value))
    
    def make_partial_collaudo(self):
        for func_names in sys.argv[1:]:
            if func_names in self.functions_names:
                tmp_return_value = self.functions_names[func_names]()
                self.test_values[func_names] = tmp_return_value
                print("Test", func_names.upper(),":", self.nicer_output(tmp_return_value))

