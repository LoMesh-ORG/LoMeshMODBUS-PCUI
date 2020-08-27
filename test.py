if __name__ == "__main__":
    xt101_radio = xt101('COM9', 247)

    xt101_radio.send_message(0x1234, [1,2,4,5])
    
    print("Mac:", xt101_radio.get_mac_address())
    time.sleep(0.75)
    
    print("Sink:", xt101_radio.get_sink_address())
    time.sleep(0.75)
    
    print("Firmware:", xt101_radio.get_firmware_version())
    time.sleep(0.75)
    
    print("Region:", xt101_radio.get_region())
    time.sleep(0.75)
    
    print("Mode:", xt101_radio.get_mode())
    time.sleep(0.75)
    
    print("Node ID:", xt101_radio.get_node_short_id())
    time.sleep(0.75)
    
    print(xt101_radio.get_debug_regs())
    time.sleep(0.75)
    
    app_key = [0x1234, 0x2345, 0x3456, 0x4567, 0x5678, 0x6789, 0x789A, 0x89AB]
    net_key = [0x1234, 0x2345, 0x3456, 0x4567, 0x5678, 0x6789, 0x789A, 0x89AB]
    print("App key:", xt101_radio.set_aes_key(app_key, 'A'))
    time.sleep(1)
    print("Net key:", xt101_radio.set_aes_key(net_key, 'N'))
    time.sleep(1)
    
    print("Set as sink", xt101_radio.set_sink())
    time.sleep(0.75)
    
    old_val = xt101_radio.get_net_id()
    time.sleep(0.75)
    xt101_radio.set_net_id(0x55)
    time.sleep(0.75)
    new_val = xt101_radio.get_net_id()
    print("Net id:", old_val, new_val)
    time.sleep(0.75)
    
    old_val = xt101_radio.get_tx_power()
    time.sleep(0.75)
    xt101_radio.set_tx_power(13)
    time.sleep(0.75)
    new_val = xt101_radio.get_tx_power()
    print("Tx power:", old_val, new_val)

    old_val = xt101_radio.get_sf()
    time.sleep(0.75)
    xt101_radio.set_sf(8)
    time.sleep(0.75)
    new_val = xt101_radio.get_sf()
    print("SF:", old_val, new_val)

    old_val = xt101_radio.get_target_rssi()
    time.sleep(0.75)
    xt101_radio.set_target_rssi(81)
    time.sleep(0.75)
    new_val = xt101_radio.get_target_rssi()
    print("RSSI:", old_val, new_val)
