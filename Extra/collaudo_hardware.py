from collaudo import *


class CollaudoHardware(Collaudo):
    '''Questa classe racchiude tutti e soli i metodi per i collaudi Hardware di tutti i dispositivi.
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
    def hdd(self, disk_info_ref=None):
        if disk_info_ref == None:
            disk_info_ref = Collaudo.device_info["device_disk"]
        disk_info_real = [self.send_ssh_command("fdisk -l 2>&1 | grep '/dev/%s:' | awk '{print $5}'"%keys) for keys in disk_info_ref]
        return [disk_info_real == list(disk_info_ref.values()), disk_info_real]

    @logging_auto 
    def ram(self, ram_info_ref=None): 
        if ram_info_ref == None:
            ram_info_ref = Collaudo.device_info["device_ram_size"]
        ram_info_real = self.send_ssh_command("free --mega | grep Mem | awk '{print $2}'")
        return [ram_info_real == ram_info_ref, ram_info_real]

    @logging_auto 
    def cpu(self, cpu_info_ref=None):
        if cpu_info_ref == None:
            cpu_info_ref = Collaudo.device_info["device_cpu"]
        cpu_info_real = self.send_ssh_command("""cat /proc/cpuinfo | grep -m 1 "model name" | awk '{print $6 " " $9}'""").split()
        return [cpu_info_ref == cpu_info_real, cpu_info_real]
    
    @logging_auto 
    def temperature(self): # TODO: Testa questo metodo
        temp_min, temp_max = 10, 90
        value_temp = self.send_ssh_command("sensors | grep -A2 'lm73' | sed -n 's/temp1: *+\\([0-9]*\\)\\..*/\\1/p'")
        return [int(value_temp) > temp_min and int(value_temp) < temp_max, value_temp, temp_min, temp_max]

    @logging_auto 
    def ups(self, ups_info_ref=None):
        if ups_info_ref == None:
            ups_info_ref = Collaudo.device_info["device_ups_capacity"]
        ups_info_real = self.send_ssh_command("/opt/scripts/showMtbfParameters.sh | grep UPS_CAPACITY | awk '{print $3}'")
        return [float(ups_info_real) > float(ups_info_ref)*0.85 and float(ups_info_real) < float(ups_info_ref)*1.15, ups_info_real, str(float(ups_info_ref)*0.9), str(float(ups_info_ref)*1.1)]



# if __name__ == "__main__":
#     if len(sys.argv) == 1:
#         full_collaudo = CollaudoHardware()
#         full_collaudo.make_full_collaudo()
#     else:
#         partial_collaudo = CollaudoHardware()
#         partial_collaudo.make_partial_collaudo()
