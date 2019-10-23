import os
import argparse
import time
import sys
import subprocess

from logging_collaudo import *
from interactive_menu import *
from conf_file import *
from sql_collaudo import *
from conf_file_ssh import *

class Collaudo:
    def __init__(self):
        self.interactive = False
        self.argument_parser()
        if len(sys.argv) == 1 or arg_interactive == True:
            self.interactive = True
        self.start()
        self.set_test()

    '''In seguito le variabili che racchiudono i risultati dei test, i test da effettuare su
    ciascun dispositivo e i valori con cui confrontare i risultati. In futuro verranno
    direttamente presi da db.'''
    
    device_info = device_info_db # TODO Questo verrà preso da db
    device_tests = device_tests_db # TODO Questo verrà preso da db
    device_names = ["MEDIA3N_SERVER", "OBOE"]
    test_values = {
                    "hdd" : [None, None, None, None],
                    "ram" : [None, None, None, None],
                    "usb" : [None, None, None, None],
                    "hdmi" : [None, None, None, None],
                    "serial_usb" : [None, None, None, None],
                    "cpu" : [None, None, None, None],
                    "swkit" : [None, None, None, None],
                    "smartalim_fw" : [None, None, None, None],
                    "bios" : [None, None, None, None],
                    "reset" : [None, None, None, None],
                    "ups" : [None, None, None, None],
                    "lan" : [None, None, None, None]
                    }
    
    '''Definizione dei metodi condivisi fra tutti i tipi di collaudi.'''

    def custom_test(self, ssh_command="", test_type="is_equal", verify_value="42"):
        '''Funzione che permette di compiere test più o meno arbitrari.
        Il parametro ssh_command richiede il comando da inviare al device.
        Il parametro test_type può essere:
            - "is_equal"
            - ""
        Il parametro verify_value ideve essere una stringa e fa riferimento
        al test "is_equal". TODO: aggiungere tipi di test generici
        '''
        tests = {
                "is_equal" : self.is_equal
                }
        return tests[test_type](ssh_command, verify_value)

    def is_equal(self, command, value):
        '''Ritorna True se il risultato di "command" è uguale a "value".'''
        return self.send_ssh_command(command) == value

    def send_ssh_command(
            self, command, 
            SSH_OPTIONS="-o ConnectTimeout=10 -q -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null", 
            ssh_ip=device_info_ssh["device_ssh_ip"], 
            ssh_user=device_info_ssh["device_ssh_user"],
            ssh_passwd=device_info_ssh["device_ssh_passwd"]):
        '''Ritorna l'output di "command" richiesto via ssh all'indirizzo "ssh_ip" con passwd "ssh_passwd" come stringa.
        In caso di mancata connessione viene riprovato l'accesso fino a 3 volte prima di uscire dal programma.
        '''
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

    def put_results_db(self):
        db_put = MySQL()
        for resu in self.test_values:
            if self.test_values[resu] != None:
                #Put resu on db
                pass
            
    def get_config_from_db(self):
        db_get = MySQL()
        db_get.select("table", "some_value")
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
        '''Questa funzione genera il menu interattivo per il setting del collaudo
        (se lo script viene avviato senza argomenti). 
        In base alle scelte effettuate verrà generata la configurazione adeguata
        dalla funzione set_test.
        '''
        if self.interactive:
            print("Inizio collaudo in modalità interattiva!")
            while True:
                global menu
                menu = Menu(Collaudo.device_tests)
                print("\nI dati inseriti sono i seguenti:")
                print("\nDispositivo da collaudare:")
                print("- ", menu.answer['devices'])
                print("\nTest da effettuare:")
                for t in menu.answer['tests']:
                    print("- ", t.upper())
                print("\nNome collaudatore: ", menu.answer['tester_name'])
                print("Postazione: ", menu.answer['test_station'])
                print("Codice Prodotto: ", menu.answer['product_code'])
                print("Part Number: ", menu.answer['part_number'])
                si_no = input("\nI dati inseriti sono corretti? [si/no] ")
                if si_no == "si" or si_no == "Si" or si_no == "SI":
                    print("")
                    break
                else:
                    continue
    
    @run_once
    def set_test(self):
        '''Funzione che genera la configurazione adeguata dei test per il dispositivo
        scelto. Per il momento si basa su configurazioni pre-impostate per ciascun
        dispositivo; TODO: prendere queste infomazioni direttamente dal db.
        '''
        if self.interactive:
            try:
                Collaudo.device_info = devices_spec_db[menu.answer['devices']]
            except ValueError as e:
                print("Non è stato scelto il dispositivo.")
                sys.exit(0)
        else:
            if str(arg_device_name).upper() in  Collaudo.device_names:
                Collaudo.device_info = devices_spec_db[arg_device_name.upper()]
            else:
                print("Non è stato scelto un dispositivo valido.")
                print("Seleziona un dispositivo con l'opzione -d NOME_DISPOSITIVO oppure utilizza il software in modalità interattiva.")
                print("Si usi l'opzione -h per una lista dei dispositivi compatibili.")
                sys.exit(0)


        
    
    def nicer_output(self, return_value):
        if return_value == True:
            return "Successo!"
        elif return_value == False:
            return "FALLITO!"
        else:
            return "ERRORE: ripetere il Test."

    @run_once
    def argument_parser(self):
        '''Questa funzione gestisce i parametri passati al software quando utilizzato in maniera non interattiva.'''
        parser = argparse.ArgumentParser(description="Software di collaudo. Per la modalità interattiva si esegua lo script senza argomenti.")
        parser.add_argument("-i", "--interactive", action="store_true", dest="arg_interactive")
        parser.add_argument("-d","--device", action="store", dest="arg_device_name", help="Nome del device su cui si effettua il collaudo. "
                            "Valori accettati: MEDIA3N_SERVER, OBOE")
        parser.add_argument("-t", "--test", nargs="+", dest="arg_test_list")
        parser.add_argument('--version', action='version', version='%(prog)s 0.1')
        globals().update(vars(parser.parse_args()))


    def make_full_collaudo(self):
        '''Questa funzione genera il collaudo completo come richiesto dall'utente, noto il dispositivo
        e i test da effettuare su questo. Stampa sullo schermo i risultati dei test e TODO salverà
        tutto sul db.
        '''
        if self.interactive:
            print("\nInizio", self.__class__.__name__,":")
            for func_names in self.functions_names:
                if func_names in self.functions_names and func_names in menu.answer['tests']:
                    logging.info(f"TEST {func_names.upper()}:")
                    tmp_return_value = self.functions_names[func_names]()           #Esecuzione funzioni di collaudo
                    logging.info(f"Test result: {self.nicer_outpu(tmp_return_value)}\n")
                    Collaudo.test_values[func_names][0] = tmp_return_value
                    print("Test", func_names.upper(), ":", self.nicer_output(tmp_return_value))
        else:
            print("\nInizio", self.__class__.__name__,":")
            for func_names in arg_test_list:
                if func_names in self.functions_names:
                    logging.info(f"TEST {func_names.upper()}:")
                    tmp_return_value = self.functions_names[func_names]()           #Esecuzione funzioni di collaudo
                    logging.info(f"Test result: {self.nicer_outpu(tmp_return_value)}\n")
                    Collaudo.test_values[func_names][0] = tmp_return_value
                    print("Test", func_names.upper(),":", self.nicer_output(tmp_return_value))

                    
    
    # def make_partial_collaudo(self):
    #     '''Questa funzione genera il collaudo parziale del dispositivo in base
    #     ai test richiesti come argomenti dello script.
    #     '''
    #     for func_names in sys.argv[1:]:
    #         if func_names in self.functions_names:
    #             tmp_return_value = self.functions_names[func_names]()
    #             self.test_values[func_names] = tmp_return_value
    #             print("Test", func_names.upper(),":", self.nicer_output(tmp_return_value))

