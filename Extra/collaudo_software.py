from collaudo import *

class CollaudoSoftware(Collaudo):
    def __init__(self):
        super().__init__()
        self.functions_names = {
                            "bios" : self.bios,
                            "smartalim_fw" : self.smartalim_fw,
                            "swkit" : self.swkit
                            } 

    def bios(self, bios_version=None):
        if bios_version == None:
            bios_version = Collaudo.device_info["device_bios"]
        version_bios = self.send_ssh_command("dmidecode -s bios-version")
        logging.info("Versione BIOS di riferimento: %s. Versione sul device %s", bios_version, version_bios)
        return bios_version == version_bios

    def smartalim_fw(self, smartalim_version=None):
        if smartalim_version == None:
            smartalim_version = Collaudo.device_info["device_smartalim_version"]
        version_smartalim = self.send_ssh_command("cat /proc/smartalim/fw_version")
        logging.info("Versione FW della Smartalim di riferimento: %s. Versione sul device %s", smartalim_version, version_smartalim)
        return version_smartalim == smartalim_version

    def swkit(self, swkit_version=None): #chiedi dove trovare il /deviceinfo per il secondo disco
        if swkit_version == None:
            swkit_version = Collaudo.device_info["device_swkit_version"]
        version_list = [self.send_ssh_command("""cat /deviceinfo | grep SWKIT | sed 's/.*"\\(.*\\)"/\\1/'""") for keys in Collaudo.device_info["device_swkit_version"]]
        logging.info(f"Versione del SWKIT dei dischi di riferimento: {Collaudo.device_info['device_swkit_version']}. Versioni sul device {version_list}")
        return all([Collaudo.device_info["device_swkit_version"][keys] == version_list[i] for keys, i in 
                    zip(Collaudo.device_info["device_swkit_version"], range(0, len(Collaudo.device_info["device_swkit_version"])))])

# if __name__ == "__main__":
#     if len(sys.argv) == 1:
#         full_collaudo = CollaudoSoftware()
#         full_collaudo.make_full_collaudo()
#     else:
#         partial_collaudo = CollaudoSoftware()
#         partial_collaudo.make_partial_collaudo()
