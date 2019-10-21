from collaudo import *

class CollaudoSoftware(Collaudo):
    def __init__(self):
        super().__init__()
        self.functions_names = {
                            "bios" : self.bios,
                            "smartalim_fw" : self.smartalim_fw,
                            "swkit" : self.swkit
                            } 

    def bios(self, version_bios=device_info["device_bios"]):
        bios_version = self.send_ssh_command("dmidecode -s bios-version")
        return bios_version == version_bios

    def smartalim_fw(self, smartalim_version=device_info["device_smartalim_version"]):
        version_smartalim = self.send_ssh_command("cat /proc/smartalim/fw_version")
        return version_smartalim == smartalim_version

    def swkit(self, swkit_version=device_info["device_swkit_version"]): #chiedi dove trovare il /deviceinfo per il secondo disco
        version_list = [self.send_ssh_command("""cat /deviceinfo | grep SWKIT | sed 's/.*"\\(.*\\)"/\\1/'""") for keys in device_info["device_swkit_version"]]
        return all([device_info["device_swkit_version"][keys] == version_list[i] for keys, i in 
                    zip(device_info["device_swkit_version"], range(0, len(device_info["device_swkit_version"])))])

if __name__ == "__main__":
    if len(sys.argv) == 1:
        full_collaudo = CollaudoSoftware()
        full_collaudo.make_full_collaudo()
    else:
        partial_collaudo = CollaudoSoftware()
        partial_collaudo.make_partial_collaudo()
