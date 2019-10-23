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
                            "temperature" : self.temperature,
                            "ups" : self.ups
                            }
    

    def hdd(self, disk_info=None):
        if disk_info == None:
            disk_info = Collaudo.device_info["device_disk"]
        size_hdd = [self.send_ssh_command("fdisk -l 2>&1 | grep '/dev/%s:' | awk '{print $5}'"%keys) for keys in disk_info]
        logging.info(f"Dimensioni dei dischi di riferimento: {disk_info}. Dimensioni reali: {size_hdd}.")
        return size_hdd == list(disk_info.values())

    def ram_size(self, size_ram=None): 
        if size_ram == None:
            size_ram = Collaudo.device_info["device_ram_size"]
        ram_size = self.send_ssh_command("cat /proc/meminfo | grep MemTotal | awk '{print $2}'")
        logging.info(f"Dimensione della RAM di riferimento: {size_ram}. Dimensione RAM sul device {ram_size}.")
        return ram_size > size_ram*0.9 and ram_size < size_ram*1.1 #Maybe a range?

    def cpu_type(self, cpu_info=None):
        if cpu_info == None:
            cpu_info = Collaudo.device_info["device_cpu"]
        info_cpu = self.send_ssh_command("""cat /proc/cpuinfo | grep -m 1 "model name" | awk '{print $6 " " $9}'""").split()
        logging.info(f"Le informazioni di riferimento della CPU sono {cpu_info}. Quelle del dispositivo sono {info_cpu}.")
        return cpu_info == info_cpu
    
    def temperature(self): # TODO: Testa questo metodo
        temp_min, temp_max = 10, 90
        value_temp = self.send_ssh_command("sensors | grep -A2 'lm73' | sed -n 's/temp1: *+\\([0-9]*\\)\\..*/\\1/p'")
        logging.info(f"La temperatura misurata è {value_temp}.")
        return value_temp > temp_min and value_temp < temp_max

    def ups(self, ups_capacity=None):
        if ups_capacity == None:
            ups_capacity = Collaudo.device_info["device_ups_capacity"]
        capacity_ups = self.send_ssh_command("/opt/scripts/showMtbfParameters.sh | grep UPS_CAPACITY | awk '{print $3}'")
        logging.info(f"Dimensione UPS di riferimento: {ups_capacity}. Dimensione del device: {capacity_ups}. Con un errore del 10% si considera il test passato.")
        return float(capacity_ups) > float(ups_capacity)*0.9 and float(capacity_ups) < float(ups_capacity)*1.1 #Chiedi se un range sia accettabile



# if __name__ == "__main__":
#     if len(sys.argv) == 1:
#         full_collaudo = CollaudoHardware()
#         full_collaudo.make_full_collaudo()
#     else:
#         partial_collaudo = CollaudoHardware()
#         partial_collaudo.make_partial_collaudo()
