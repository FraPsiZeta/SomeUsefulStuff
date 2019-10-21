from collaudo import *


class CollaudoHardware(Collaudo):
    def __init__(self):
        super().__init__()
        self.functions_names = {
                            "hdd" : self.hdd,
                            "ram" : self.ram_size,
                            "cpu" : self.cpu_type,
                            "ups" : self.ups
                            }
    
    def hdd(self, disk_info=device_info["device_disk"]):
        size_hdd = [self.send_ssh_command("fdisk -l 2>&1 | grep '/dev/%s:' | awk '{print $5}'"%keys) for keys in disk_info]
        # logging.info("Inizio test HDD.")
        # logging.info("Test HDD: Valori di riferimento: %s", disk_info)
        # logging.info("Test HDD: Valori del device: %s", size_hdd)
        # logging.info("Test HDD: Test: %s", self.nicer_output(size_hdd == list(disk_info.values())))
        return size_hdd == list(disk_info.values())

    def ram_size(self, size=device_info["device_ram_size"]): 
        ram_value = self.send_ssh_command("cat /proc/meminfo | grep MemTotal | awk '{print $2}'")
        return ram_value == size #Maybe a range?

    def cpu_type(self, cpu_core_numbers=device_info["device_cpu_cores_numbers"], cpu_freq=device_info["device_cpu_freq"]):
        freq_cpu = self.send_ssh_command("lscpu | grep  'Model name' | awk '{print $8}'")
        core_cpu = self.send_ssh_command("lscpu | grep  'Core(s)' | awk '{print $4}'")
        return core_cpu == cpu_core_numbers and freq_cpu == cpu_freq

    def ups(self, ups_capacity= device_info["device_ups_capacity"]):
        capacity_ups = self.send_ssh_command("/opt/scripts/showMtbfParameters.sh | grep UPS_CAPACITY | awk '{print $3}'")
        return float(capacity_ups) > float(ups_capacity)*0.9 and float(capacity_ups) < float(ups_capacity)*1.1 #Chiedi se un range sia accettabile



if __name__ == "__main__":
    if len(sys.argv) == 1:
        full_collaudo = CollaudoHardware()
        full_collaudo.make_full_collaudo()
    else:
        partial_collaudo = CollaudoHardware()
        partial_collaudo.make_partial_collaudo()
