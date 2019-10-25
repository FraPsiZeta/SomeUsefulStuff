from collaudo import *

class CollaudoSoftware(Collaudo):
    '''Questa classe racchiude tutti e soli i metodi per i collaudi Sofware di tutti i dispositivi.
    Ciascun metodo si occupa di un singolo test, avendo come variabile di ritorno una lista, 
    che abbia da 1 a 4 elementi, nel seguente ordine: 
    [ Risulato del test (bool), Valore del test (può essere una lista a sua volta) (str),
    Valore minimo del test (str), Valore massimo del test (str) ]
    Se presenti, altri valori risultanti dai vari collaudi vengono salvati in una variabile della 
    classe madre Collaudo, per essere poi caricati su db.
    '''
    def __init__(self):
        super().__init__()
    
    @logging_auto
    def bios(self, bios_version_ref=None):
        if bios_version_ref == None:
            bios_version_ref = Collaudo.device_info["device_bios"]
        bios_version_real = self.send_ssh_command("dmidecode -s bios-version")
        return [bios_version_ref == bios_version_real, bios_version_real]
    
    @logging_auto
    def smartalim_fw(self, smartalim_version_ref=None):
        if smartalim_version_ref == None:
            smartalim_version_ref = Collaudo.device_info["device_smartalim_version"]
        smartalim_version_ref_real = self.send_ssh_command("cat /proc/smartalim/fw_version")
        return [smartalim_version_ref_real == smartalim_version_ref, smartalim_version_ref_real]

    @logging_auto
    def swkit(self, swkit_version_ref=None): 
        '''Questo metodo garantisce che i valori dei SK siano ritornati in ordine alfabetico rispetto
        al nome del device a cui appartengono (sda, sdb, sdc, etc.).
        '''
        if swkit_version_ref == None:
            swkit_version_ref = Collaudo.device_info["device_swkit_version"]
        file_disk_location = self.send_ssh_command("""find / -name deviceinfo -exec """
                            """sh -c "df {} | sed -n 's#.*/dev/\\([a-z]\\{3\\}\\).*#\\1#p'" \\;""").split()
        swkit_version_real = self.send_ssh_command("""find / -name deviceinfo -exec """
                            """sh -c 'cat {} | grep SWKIT | cut -d "\\"" -f 2' \\;""").split()
        swkit_version_real_dic = dict(zip(file_disk_location, swkit_version_real))
        return [all([swkit_version_ref[keys] == swkit_version_real_dic[keys] for keys 
                in swkit_version_ref]), [value for key, value in sorted(swkit_version_real_dic.items())] ]

# if __name__ == "__main__":
#     if len(sys.argv) == 1:
#         full_collaudo = CollaudoSoftware()
#         full_collaudo.make_full_collaudo()
#     else:
#         partial_collaudo = CollaudoSoftware()
#         partial_collaudo.make_partial_collaudo()
