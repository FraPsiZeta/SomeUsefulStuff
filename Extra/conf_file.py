'''
File di configurazione, qui sono elencati tutti i parametri da confrontare (device_info e device_spec), 
e la lista di test da effettuare per ciascun device (device_test). Quando in futuro verranno
presi questi dati da DB, verranno inseriti in questi dictionaries per mantenere la strutura 
del programma invariata.
'''

#Default device info, questo verrà sostitutito
device_info_db = {        
                "device_disk" : { "sda" : "256060514304", "sdb" : "128035676160" },
                "device_bios" : "E204",
                "device_ram_size" : "16341396",
                "device_cpu_cores_numbers" : "4",
                "device_cpu_freq" : "2.90GHz",
                "device_serial_port" : "Serial Port",
                "device_ups_capacity" : "3.362",
                "device_smartalim_version" : "21.04 R258",
                "device_swkit_version" : { "sda" : "SK0096-PK02-000", "sdb" : ""}
                }
        
devices_spec_db = {
                "MEDIA3N_SERVER" : {
                                    "device_disk" : { "sda" : "1024209543168", "sdb" : "128035676160" },
                                    "device_bios" : "E204",
                                    "device_ram_size" : "16341396",
                                    "device_cpu_cores_numbers" : "4",
                                    "device_cpu_freq" : "2.90GHz",
                                    "device_serial_port" : "Serial Port",
                                    "device_ups_capacity" : "3.362",
                                    "device_smartalim_version" : "21.04 R258",
                                    "device_swkit_version" : { "sda" : "SK0096-PK02-000", "sdb" : ""}
                                    },
                "OBOE" : {}
                }

device_tests_db = {
                "MEDIA3N_SERVER" : {
                                    "hardware" : ["hdd", "ram", "cpu", "ups"],
                                    "software" : ["bios", "smartalim_fw", "swkit"],
                                    "esterno" : ["lan", "reset", "hdmi", "serial_usb", "usb"]
                                    },
                "OBOE" : {
                            "hardware" : ["None"],
                            "software" : ["None"],
                            "esterno" : ["None"]
                    }
                }
                                    
                                                        
