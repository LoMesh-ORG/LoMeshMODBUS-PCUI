#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.22
#  in conjunction with Tcl version 8.6
#    Aug 23, 2019 06:09:39 PM EDT  platform: Windows NT
#    May 15, 2020 12:33:03 PM EDT  platform: Windows NT
#    May 15, 2020 04:33:48 PM EDT  platform: Windows NT
#    May 15, 2020 04:36:38 PM EDT  platform: Windows NT
#    May 16, 2020 11:12:38 AM EDT  platform: Windows NT
#    May 20, 2020 12:20:45 AM EDT  platform: Windows NT
#    May 20, 2020 08:57:58 PM EDT  platform: Windows NT
#    May 20, 2020 09:03:07 PM EDT  platform: Windows NT
#    May 27, 2020 08:45:53 PM EDT  platform: Windows NT

import sys
import serial
import serial.tools.list_ports
import re
import time
from tkinter import filedialog
import subprocess
import packet_error_rate_helper
import xt101

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False

except ImportError:
    import tkinter.ttk as ttk
    py3 = True
    
baud_dict = {
                "9800" : 9800,
                "19200" : 19200,
                "38400" : 38400,
                "57600" : 57600,
                "115200" : 115200
            }
parity_dict = {
                "Even" : serial.PARITY_EVEN,
                "Odd"  : serial.PARITY_ODD,
                "None" : serial.PARITY_NONE
              }                        
    
def bootload():
    global w, top_level, root
    try:
        filename = filedialog.askopenfilename(initialdir = "/",title = "Select hex file to load",filetypes = (("hex files","*.hex"),))
        print(filename)
        if(filename):
            cmd = "python bootloader.py " + filename + " " + Combobox_COMText.get() + " " + "115200"
            print(cmd)
            subprocess.call(cmd, shell=True)
    except Exception as e:
        print("Error in bootloading the device " + str(e))

def softReset():
    global w, top_level, root
    try:
        #Get current COM port selected
        global Combobox_COMText
        port = Combobox_COMText.get()        
        #Create a modbus instrument
        xt101_radio = xt101.xt101(port, 247)
        xt101_radio.radio_reset()
    except Exception as e:
        print("Error in resetting the device " + str(e))
    sys.stdout.flush()    

def bcastMessage():
    global w, top_level, root      
    global RXTXShortID   
    global Packet  
    try:
        #Get current COM port selected
        global Combobox_COMText
        port = Combobox_COMText.get()        
        #Create a modbus instrument
        xt101_radio = xt101.xt101(port, 247)
        value = Packet.get()
        dest = 0xFFFF
        b = bytearray()
        b.extend(map(ord, value))
        xt101_radio.send_message(dest, b)            
    except Exception as e:
        print("Error in sending unicast: " + str(e))
    sys.stdout.flush()

def recvMessage():
    #Read the last message
    global w, top_level, root
    global RXTXShortID   
    global Packet    
    try:
        #Get current COM port selected
        global Combobox_COMText
        port = Combobox_COMText.get()        
        #Create a modbus instrument
        xt101_radio = xt101.xt101(port, 247)
        ShortID, value= xt101_radio.read_message()
        print(ShortID, value)
        RXTXShortID.set(str(hex(ShortID)))
        Packet.set(value)
    except Exception as e:
        print("Error in reading message: " + str(e))
    sys.stdout.flush()

def sendMessage():
    global w, top_level, root      
    global RXTXShortID   
    global Packet  
    try:
        #Get current COM port selected
        global Combobox_COMText
        port = Combobox_COMText.get()        
        #Create a modbus instrument
        xt101_radio = xt101.xt101(port, 247)
        value = Packet.get()
        dest = int(RXTXShortID.get()[0:4], 16)
        b = bytearray()
        b.extend(map(ord, value))
        xt101_radio.send_message(dest, b)            
    except Exception as e:
        print("Error in sending unicast: " + str(e))
    sys.stdout.flush()

def sendSinkMessage():
    global w, top_level, root            
    global Packet  
    try:
        #Get current COM port selected
        global Combobox_COMText
        port = Combobox_COMText.get()        
        #Create a modbus instrument
        xt101_radio = xt101.xt101(port, 247)
        value = Packet.get()
        dest = xt101_radio.get_sink_id() #Get current sink address
        print(dest)
        b = bytearray()
        b.extend(map(ord, value))
        xt101_radio.send_message(dest, b)
    except Exception as e:
        print("Error in sending message to sink " + str(e))
    sys.stdout.flush()

def setSink():
    #Set this device as a data sink
    global w, top_level, root        
    try:
        #Get current COM port selected
        global Combobox_COMText
        port = Combobox_COMText.get()        
        #Create a modbus instrument
        xt101_radio = xt101.xt101(port, 247)
        xt101_radio.set_sink()
    except Exception as e:
        print("Error in setting device as sink " + str(e))
    sys.stdout.flush()

    

def resetCADCounter():
    #Send reset the CAD counter
    global w, top_level, root
    try:
        #Get current COM port selected
        global Combobox_COMText
        port = Combobox_COMText.get()        
        #Create a serial object
        with serial.Serial(port, 19200, parity=serial.PARITY_ODD, timeout = 1) as ser:
            ser.write(b'AT+CADCOUNTERRST\r\n')
    except Exception as e:
        print("Error in reset the CAD counter " + str(e))
    sys.stdout.flush()

def writeData():
    global w, top_level, root
    try:
        #Get current COM port selected
        global Combobox_COMText
        port = Combobox_COMText.get()        
        #Create a modbus instrument
        xt101_radio = xt101.xt101(port, 247)
        #Set Network Address
        try:
            global NADDR_Text
            value = NADDR_Text.get()[0:2]
            value = int(value,10)
            #Code reached here so the value must be valid                 
            xt101_radio.set_net_id(value)
            time.sleep(0.75)
        except Exception as e:
            print("Illegal value for network address " + str(e))
        
        #Set TX power
        try:
            value = w.Combobox_TXPower.current() + 2
            value = int(value)
            xt101_radio.set_tx_power(value)
            time.sleep(0.75)
        except Exception as e:
            print("Error in setting TX power " + str(e))
            
        #Set RF Channel
        try:
            value = w.Combobox_RFCH.current()
            value = int(value)
            xt101_radio.set_rf_channel(value)
            time.sleep(0.75)
        except Exception as e:
            print("Error in setting RF channel " + str(e))
            
        #Set the spreading factor
        try:
            value = w.Combobox_sf.current()
            value = int(value) + 7
            xt101_radio.set_sf(value)
            time.sleep(0.75)
        except Exception as e:
            print("Illegal value for Spreading factor " + str(e))
            
        #Set RSSI CAD threshold
        try:
            global RSSILevel_Text
            value = RSSILevel_Text.get()[0:4].replace("-", "")
            value = int(value, 10)
            xt101_radio.set_target_rssi(value)
            time.sleep(0.75)
        except Exception as e:
            print("Illegal value for CAD RSSI threshold " + str(e))
            
        #Set the AES Application Encryption key
        try:
            global AES_Text
            value = AES_Text.get()[0:32]
            AES_Text.set('Value Hidden')
            #Code reached here so the value must be valid  
            if(len(value) == 32):
                j = 0
                for i in range(1,9):                    
                    print(int(value[j:j + 4], 16))
                    j = j + 4
        except Exception as e:
            print("Illegal value for AES application key " + str(e))
        
        #Set the AES Network Encryption key
        try:
            global net_key_text
            value = net_key_text.get()[0:32]
            net_key_text.set('Value Hidden')
            #Code reached here so the value must be valid  
            if(len(value) == 32):
                j = 0
                for i in range(1,9):                    
                    print(int(value[j:j + 3], 16))
                    j = j + 4
        except Exception as e:
            print("Illegal value for AES network key " + str(e))   
    except Exception as e:
        print("Error in saving new settings " + str(e))
    sys.stdout.flush()

def readData():
    global w, top_level, root
    try:
        #Get current COM port selected
        global Combobox_COMText
        port = Combobox_COMText.get()         
        baud = baud_dict[combobox_baudtext.get()]
        parity = parity_dict[combobox_paritytext.get()]
        #Create a modbus instrument
        xt101_radio = xt101.xt101(port, 247)
        #read network address
        NADDR_Text.set(xt101_radio.get_net_id())
        #read TX power
        w.Combobox_TXPower.current(int(xt101_radio.get_tx_power()) - 2)
        #read radio mode
        mode_Text.set(xt101_radio.get_mode())
        #read RF channel
        w.Combobox_RFCH.current(int(xt101_radio.get_rf_chnnel()))
        #Read SF
        w.Combobox_sf.current(int(xt101_radio.get_sf()) - 7)
        #Read RSSI CAD Level
        RSSILevel_Text.set(xt101_radio.get_target_rssi())
        #Read current CAD counter
        CADCounter_Text.set("")
        #Read MAC ID
        MAC_Text.set(xt101_radio.get_mac_address())
        #Read the Network Short ID
        ADDR_Text.set(xt101_radio.get_node_short_id())
        #Read the Firmware and AT Command version
        Firmware_Text.set(xt101_radio.get_firmware_version())
    except Exception as e:
        print("Error in loading values from selected device " + str(e))
        
    sys.stdout.flush()

def get_rx_queue():
    #Get the number of messages queued up for this node
    global w, top_level, root
    global RXTXShortID   
    global Packet
    try:
        #Get current COM port selected
        global Combobox_COMText
        port = Combobox_COMText.get()         
        baud = baud_dict[combobox_baudtext.get()]
        parity = parity_dict[combobox_paritytext.get()]
        #Create a serial object
        with serial.Serial(port, baudrate = baud, parity = parity, timeout = 0.25) as ser:
            ser.reset_input_buffer()
            ser.write(b'AT+RXCT?\r\n')
            data = ser.read_until().decode('utf-8')
            if("NOT OK" in data):
                Packet.set("No Packets")
            else:
                data.replace('\r', '')
                data.replace('\n', '')
                Packet.set(data)
            
    except Exception as e:
        print("Error in getting last message " + str(e))
    sys.stdout.flush()
    
def set_Tk_var():    
    global combobox_sf
    combobox_sf = tk.StringVar()
    global net_key_text
    net_key_text = tk.StringVar()
    global net_key
    net_key = tk.StringVar()
    global per_time_out_var
    per_time_out_var = tk.StringVar()
    global per_result_var
    per_result_var = tk.StringVar()
    per_result_var.set('Label')
    global per_target_node
    per_target_node = tk.StringVar()
    global combobox_paritytext
    combobox_paritytext = tk.StringVar()
    global combobox_baudtext
    combobox_baudtext = tk.StringVar()
    global combobox
    combobox = tk.StringVar()
    global Combobox_COMText
    Combobox_COMText = tk.StringVar()
    global combobox_TXpowerText
    combobox_TXpowerText = tk.StringVar()
    global NADDR_Text
    NADDR_Text = tk.StringVar()    
    global mode_Text
    mode_Text = tk.StringVar()
    mode_Text.set('Unknown')
    global combobox_RFChannel
    combobox_RFChannel = tk.StringVar()    
    global HopCount_Text
    HopCount_Text = tk.StringVar()    
    global CADCounter_Text
    CADCounter_Text = tk.StringVar()
    CADCounter_Text.set('Unknown')
    global RSSILevel_Text
    RSSILevel_Text = tk.StringVar()    
    global AES_Text
    AES_Text = tk.StringVar()    
    global MAC_Text
    MAC_Text = tk.StringVar()
    MAC_Text.set('Unknown')
    global ADDR_Text
    ADDR_Text = tk.StringVar()
    ADDR_Text.set('Unknown')
    global Firmware_Text
    Firmware_Text = tk.StringVar()
    Firmware_Text.set('Unknown')
    global ATSet_Text
    ATSet_Text = tk.StringVar()
    ATSet_Text.set('Unknown')
    global RXTXShortID
    RXTXShortID = tk.StringVar()    
    global Packet
    Packet = tk.StringVar()
    global bl_version_number
    bl_version_number = tk.StringVar()
    bl_version_number.set('')

def refreshCOMPorts():
    global w, top_level, root
    try:
        global combobox_COM        
        w.Combobox_COM['values'] = [str(comport.device) for comport in serial.tools.list_ports.comports()]
        w.Combobox_COM.current(0)
    except Exception as e:
        print("Error in finding COM ports " + str(e))
    sys.stdout.flush()

def packet_error_rate():
    try:
        #Get the target node    
        target = per_target_node.get()[0:4]
        int(target,16)
        #if code reaches here then it a valid 16 bit address
        print("Target node ", target.encode('utf-8'))
        #Get current COM port selected
        global Combobox_COMText
        port = Combobox_COMText.get()         
        baud = baud_dict[combobox_baudtext.get()]
        parity = parity_dict[combobox_paritytext.get()]
        #Get time out from ui
        try:
            timeout = int(per_time_out_var.get())
        except Exception as e:
            timeout = 5
            print("Error in setting PER timeout", str(e))
        #Create a serial object
        with serial.Serial(port, baudrate = baud, parity = parity, timeout = 0.25) as ser:
            successful = 0
            for i in range(0,10):
                if (0 == packet_error_rate_helper.ping_test(target, 5, ser)):
                    successful = successful + 1
                time.sleep(2)
            rate = successful * 100/10
            per_result_var.set(str(rate))
            print("Packet success rate = ", rate)
    except Exception as e:
        print("Error in packet error rate function ", str(e))
    sys.stdout.flush()
    
def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top
    #Init GUI components
    w.Combobox_TXPower['values'] = ["2 dBm","3 dBm","4 dBm","5 dBm","6 dBm","7 dBm","8 dBm","9 dBm","10 dBm","11 dBm","12 dBm","13 dBm","14 dBm","15 dBm","16 dBm","17 dBm"]
    w.Combobox_RFCH['values'] = ["1: 906MHz","2: 908MHz","3: 910MHz","4: 912MHz","5: 914MHz","6: 916MHz","7: 918MHz","8: 920MHz","9: 922MHz","10: 924MHz"]
    w.Combobox_parity['values'] = ["Even", "Odd", "None"]    
    w.Combobox_parity.current(0)
    w.Combobox_sf['values'] = ["7", "8", "9", "10", "11", "12"]
    w.Combobox_baud['values'] = ["9600", "19200", "38400", "57600", "115200"]
    w.Combobox_baud.current(1)
    per_result_var.set("")

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import LoMesh_MODBUS
    LoMesh_MODBUS.vp_start_gui()





