from collaudo import *


class CollaudoHardware(Collaudo):
    '''Questa classe racchiude tutti e soli i metodi per i collaudi Hardware di tutti i dispositivi.
    Ciascun metodo si occupa di un singolo test, avendo come valore di ritorno il riultato del test.
    Se presenti, altri valori risultanti dai vari collaudi vengono salvati in una variabile della 
    classe madre Collaudo, per essere poi caricati su db.
    '''
    def __init__(self):
        super().__init__()
        self.functions_names = {
                            "hdd" : self.hdd,
                            "ram" : self.ram_size,
                            "cpu" : self.cpu_type,
                            "ups" : self.ups
                            }
    

    def hdd(self, disk_info=None):
        if disk_info == None:
            disk_info = Collaudo.device_info["device_disk"]
        size_hdd = [self.send_ssh_command("fdisk -l 2>&1 | grep '/dev/%s:' | awk '{print $5}'"%keys) for keys in disk_info]
        # logging.info("Inizio test HDD.")
        # logging.info("Test HDD: Valori di riferimento: %s", disk_info)
        # logging.info("Test HDD: Valori del device: %s", size_hdd)
        # logging.info("Test HDD: Test: %s", self.nicer_output(size_hdd == list(disk_info.values())))
        return size_hdd == list(disk_info.values())

    def ram_size(self, size_ram=None): 
        if size_ram == None:
            size_ram = Collaudo.device_info["device_ram_size"]
        ram_size = self.send_ssh_command("cat /proc/meminfo | grep MemTotal | awk '{print $2}'")
        return ram_size == size_ram #Maybe a range?

    def cpu_type(self, cpu_core_numbers=None, cpu_freq=None):
        if cpu_core_numbers == None:
            cpu_core_numbers = Collaudo.device_info["device_cpu_cores_numbers"]
        if cpu_freq == None:
            cpu_freq = Collaudo.device_info["device_cpu_freq"]
        freq_cpu = self.send_ssh_command("lscpu | grep  'Model name' | awk '{print $8}'")
        core_cpu = self.send_ssh_command("lscpu | grep  'Core(s)' | awk '{print $4}'")
        return core_cpu == cpu_core_numbers and freq_cpu == cpu_freq

    def ups(self, ups_capacity=None):
        if ups_capacity == None:
            ups_capacity = Collaudo.device_info["device_ups_capacity"]
        capacity_ups = self.send_ssh_command("/opt/scripts/showMtbfParameters.sh | grep UPS_CAPACITY | awk '{print $3}'")
        return float(capacity_ups) > float(ups_capacity)*0.9 and float(capacity_ups) < float(ups_capacity)*1.1 #Chiedi se un range sia accettabile



# if __name__ == "__main__":
#     if len(sys.argv) == 1:
#         full_collaudo = CollaudoHardware()
#         full_collaudo.make_full_collaudo()
#     else:
#         partial_collaudo = CollaudoHardware()
#         partial_collaudo.make_partial_collaudo()
