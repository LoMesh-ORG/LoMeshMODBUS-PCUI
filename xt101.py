import minimalmodbus
import time

class xt101(minimalmodbus.Instrument):
    """Modbus radio class for xt101"""
    
    def __init__(self, portname, slaveaddress):
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)
        self.serial.parity = minimalmodbus.serial.PARITY_EVEN
        self.serial.timeout = 0.75
        self.serial.close_port_after_each_call = True
        
    def get_mac_address(self):
        mac = self.read_registers(0, 6)
        mac_str = ""
        for i in mac:
            mac_str = mac_str + format(i, 'x') 
        return mac_str

    def get_sink_address(self):
        return format(self.read_register(6), 'x')

    def get_firmware_version(self):
        return str(self.read_register(7)/100)

    def get_region(self):
        region_dict = {1:"North America",
                       2:"India"
            }
        return region_dict[self.read_register(8)]

    def get_mode(self):
        mode_dict = {0:"Repeater",
                     1:"End Node"
                     }
        return mode_dict[self.read_register(9)]

    def get_tx_id(self):
        return self.read_register(10)

    def get_rx_id(self):
        return self.read_register(11)

    def get_pending_rx_messages(self):
        return self.read_register(12)

    def get_node_short_id(self):
        return format(self.read_register(13), 'x')

    def get_debug_regs(self):
        debug_regs_raw = self.read_registers(14, 2)
        debug_regs = []
        debug_regs.append(format(debug_regs_raw[0], 'x'))
        debug_regs.append(format(debug_regs_raw[1], 'x'))
        return debug_regs

    def set_aes_key(self, key, type_of_key):
        if (len(key) != 8):
            return -1
        if('A' == type_of_key):
            addr = 500
        elif('N' == type_of_key):
            addr = 508
        else:
            return -1
        self.write_registers(addr, key)
        return 0

    def set_sink(self):
        self.write_register(516, 1)

    def get_net_id(self):
        return self.read_register(1000)

    def set_net_id(self, netid):
        self.write_register(1000, (netid & 0xFF))

    def get_tx_power(self):
        return self.read_register(1001)

    def set_tx_power(self, power):
        self.write_register(1001, (power & 0xFF))

    def get_sf(self):
        return self.read_register(1002)

    def set_sf(self, sf):
        self.write_register(1002, sf)

    def get_target_rssi(self):
        return -1 * self.read_register(1003)

    def set_target_rssi(self, rssi):
        self.write_register(1003, rssi)
        
    def get_rf_chnnel(self):
        return self.read_register(1005)
        
    def set_rf_channel(self, channel):
        self.write_register(1005, channel)

    def send_message(self, dest, payload):
        if(len(payload) > 64):
            return -1
        pad_size = 64 - len(payload)
        payload = [*payload, *[0] * pad_size]
        index = 0
        modbus_index = 0
        modbus_payload = [0]*32
        while(index < len(payload)):
            modbus_payload[modbus_index] = (payload[index] << 8) | payload[index+1]
            index = index + 2
            modbus_index = modbus_index + 1
        #Add the destination address
        modbus_payload.insert(0, dest)
        
        self.write_registers(2001, modbus_payload)
        #print(modbus_payload)
        #Set the tx control reg to 1
        self.write_register(2000, 1)
        
    def read_message(self):
        src_addr = self.read_register(3001)
        modbus_payload = self.read_registers(3002, 15)
        #Set the rx control reg to 0
        self.write_register(3000, 0)
        return [src_addr, modbus_payload]
    
    def radio_reset(self):
        self.write_register(1016, 1)
        
    def get_sink_id(self):
        return self.read_register(6)
        
    def set_sink(self):
        self.write_register(516, 1)