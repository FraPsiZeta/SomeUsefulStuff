import os
import argparse
import time
import sys
import subprocess
import itertools
from datetime import datetime

from logging_collaudo import *
from interactive_menu import *
from conf_file import *
from sql_collaudo import *
from conf_file_ssh import *

# TODO: chiedi come entrano in gioco i nomi dei treni

class Collaudo:
    '''Classe madre per il collaudo, sono presenti tutti i metodi che devono essere
    condivisi fra i vari tipi di collaudo, e premette di utilizzarli singolarmente
    (Hardware, Software o Esterno).

    Nella versione attuale sono hard-coded le seguenti:
    - Lista dei dispositivi per cui il collaudo è disponibile.
    - Lista dei collaudi da effettuare per ogni dispositivo. 
    - Lista dei treni.
    - I valori di configurazione in conf_file.
    - Le credenziali ssh in conf_file_ssh.

    Il software permette l'aggiunta di nuovi metodi di collaudo (quindi all'interno della
    classe di riferimento: CollaudoHardware, CollaudoSoftware o CollaudoEsterno), è sufficiente seguire 
    alcune linee guida:
    - Aggiungere il nome del metodo come stringa al dict 'test_values' presente
    fra le variabili statiche di questa classe.
    - Lo stesso nome venga aggiunto nell'elenco di test da effettuare per il relativo device,
    presente per ora nel file conf_file.py. TODO: assicurarsi che l'elenco dei test per il 
    dispositivo che verrranno presi da db abbiano lo stesso nome di test_values.
    - Il nome della funzione sia il più possibile rappresentativo del tipo di collaudo
    che sta effettuando.
    - Deve avere come variabile di ritorno una lista, che abbia da 1 a 4 elementi, in questo ordine: 
    [ Risulato del test (bool), Valore del test (può essere una lista a sua volta) (str),
    Valore minimo del test (str), Valore massimo del test (str)]
    '''
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
    
    device_info = device_info_db # TODO: Questo verrà preso da db
    device_tests = device_tests_db # TODO: Questo verrà preso da db
    device_names = ["MEDIA3N_SERVER", "OBOE"] # TODO: anche questa lista potrebbe essere presa da db
    configurations_name = ["ROCK", "TRENO"] # TODO: come sopra
    allegato = []

    '''Il dic test_values definito in seguito racchiude rispettivamente: 
    "nome_test" : [risultato test, valore test, valore min, valore max]
    '''
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
                    "temperature" : [None, None, None, None],
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

    @staticmethod
    def put_results_mysql_db():
        '''Metodo provvisorio e incompleto'''
        db_put = MySQL()
        column_list = [col[0] for col in db_put.generic_query(f"SHOW columns FROM {menu.answer['devices']}")]

        values = [menu.answer['test_number'], menu.answer['part_number'], "0000", Collaudo.test_values['ram'][1], Collaudo.test_values['bios'][1]]
        if isinstance(Collaudo.test_values['hdd'][1], list):
            values.append(Collaudo.test_values['hdd'][1][0])
            values.append(Collaudo.test_values['hdd'][1][1])
        else:
            values.append(None)
            values.append(None)
        if isinstance(Collaudo.test_values['lan'][1], list):
            values.append(Collaudo.test_values['lan'][1][0])
            values.append(Collaudo.test_values['lan'][1][1])
        else:
            values.append(None)
            values.append(None)
        values.append(Collaudo.test_values['smartalim_fw'][1])
        if isinstance(Collaudo.test_values['swkit'][1], list):
            values.append(Collaudo.test_values['swkit'][1][1]) # TODO ask:sdb??
        else:
            values.append("")
        values.extend([menu.answer['trains'], datetime.today().strftime('%Y-%m-%d'), menu.answer['tester_name'], "1", "".join(Collaudo.allegato)])

        resu = dict(itertools.zip_longest(column_list, values, fillvalue=None))
        # db_put.insert(menu.answer['devices'], **resu)

    @staticmethod
    def create_attachment():
        '''Si spera sia una funzione provvisoria, in attesa di MongoDB..'''
        for key in Collaudo.test_values:
            if Collaudo.test_values[key][1] != None:
                Collaudo.allegato.append(key)
                Collaudo.allegato.append("=")
                if isinstance(Collaudo.test_values[key][1], list):
                    for s, i in enumerate(Collaudo.test_values[key][1]):
                        Collaudo.allegato.append(i)
                        if s != len(Collaudo.test_values[key][1]) - 1: #Ovvero se non siamo a fine lista
                            Collaudo.allegato.append(", ")
                else:
                    Collaudo.allegato.append(Collaudo.test_values[key][1])
                Collaudo.allegato.append("\n")

    def get_config_from_db(self):
        db_get = MySQL()
        db_get.select("table", "some_value")
        #Da completare una volta disponibile il db effettivo

    def fill_test_results(self, name, resu):
        for i in range(0, len(resu)):
            Collaudo.test_values[name][i] = resu[i]
        
    def run_once(f):
        def wrapper(*args, **kwargs):
            if not wrapper.has_run:
                wrapper.has_run = True
                return f(*args, **kwargs)
        wrapper.has_run = False
        return wrapper

    def create_title(self):
        lenght = 127
        left_space = 5
        print(" ", end="")
        for i in range(0,lenght):
            print("—", end="")
        print("")
        with open("title.dat", "r") as title:
            for i in title.readlines():
                print(" "*left_space, i, end='')
        print(" "*left_space, "Software di collaudo per prodotti Sadel.")
        print(" "*left_space, "Versione: 0.1")
        print(" ", end="")
        for i in range(0, lenght):
            print("—", end="")
        print("")
        print("")

    @run_once
    def start(self):
        '''Questa funzione genera il menu interattivo per il setting del collaudo
        (se lo script viene avviato senza argomenti). 
        In base alle scelte effettuate verrà generata la configurazione adeguata
        dalla funzione set_test.

        Il costruttore del menù prende in ingresso tre parametri:
        - La lista dei test che deve effettuare ciascun dispositivo
        - La lista dei nomi per cui è dispnibile il collaudo.
        - La lista con le configurazioni (treni?)
        '''
        self.create_title()
        if self.interactive:
            print("Inizio collaudo in modalità interattiva!")
            while True:
                global menu
                menu = Menu()
                menu.start_menu(Collaudo.device_tests, 
                            Collaudo.device_names, 
                            Collaudo.configurations_name)

                print("\nI dati inseriti sono i seguenti:")
                print("\nDispositivo da collaudare:")
                print(f"- {menu.answer['devices']}, treno {menu.answer['trains']}")
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
    
    @run_once # TODO: prendere queste infomazioni direttamente dal db.
    def set_test(self):
        '''Funzione che genera la configurazione adeguata dei test per il dispositivo
        scelto. Per il momento si basa su configurazioni pre-impostate per ciascun
        dispositivo.
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
                print("Seleziona un dispositivo con l'opzione -d NOME_DISPOSITIVO oppure "
                        "utilizza il software in modalità interattiva.")
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
        '''Questa funzione gestisce i parametri passati al software quando 
        utilizzato in maniera non interattiva.
        '''
        parser = argparse.ArgumentParser(description="Software di collaudo. Per la modalità interattiva "
                                                    "si esegua lo script senza argomenti.")
        parser.add_argument("-i", "--interactive", action="store_true", dest="arg_interactive")
        parser.add_argument("-d","--device", action="store", dest="arg_device_name", help="Nome del device "
                            "su cui si effettua il collaudo. Valori accettati: MEDIA3N_SERVER, OBOE")
        parser.add_argument("-t", "--test", nargs="+", dest="arg_test_list", help="Nome dei "
                            "test che si vogliono effettuare") # TODO: lista test divisa per dispositivi
        parser.add_argument("--log-off", action="store_true", dest="log_off", help="Se attiva, questa flag inibisce il logging "
                            "(leggero miglioramento nelle performance).")
        parser.add_argument('--version', action='version', version='%(prog)s 0.1')

        globals().update(vars(parser.parse_args()))


    def make_full_collaudo(self):
        '''Questa funzione genera il collaudo completo come richiesto dall'utente, noto il dispositivo
        e i test da effettuare su questo. Stampa sullo schermo i risultati dei test e TODO salverà
        tutto sul db. 

        Se lanciato in modalità interattiva, il software chiamerà solo le funzioni appartenenti
        sia all'elenco richiesto dall'utente che alla master-list dei metodi di collaudo 
        (denominata 'test-values') 
        In caso di modalità non-interarriva venogono chiamate solo le funzioni richieste
        all'avvio del programma.

        Il blocco di eccezione è stato aggiunto per evitare che vengano chimati metodi non appartenenti
        alla classe a cui l'oggetto istanziato appartiene.
        '''
        print_first = Collaudo.run_once(print)
        if self.interactive:
            for func_names in Collaudo.test_values:
                if func_names in menu.answer['tests']:
                    try:
                        tmp_return_value = getattr(self, func_names)()            
                        print_first("\nInizio", self.__class__.__name__,":")
                    except AttributeError:                                       
                        continue
                    self.fill_test_results(func_names, tmp_return_value)
                    print("Test", func_names.upper(), ":", self.nicer_output(tmp_return_value[0]))
        else:
            print("\nInizio", self.__class__.__name__,":")
            for func_names in arg_test_list:
                try:
                    tmp_return_value = getattr(self, func_names)()            
                    print_first("\nInizio", self.__class__.__name__,":")
                except AttributeError:                                       
                    continue
                self.fill_test_results(func_names, tmp_return_value)
                print("Test", func_names.upper(), ":", self.nicer_output(tmp_return_value[0]))

