#!python
#
# erasynth.py
#
# Python interface to ERAsynth Micro made by ERAinstruments
# https://erainstruments.com
#
# (C)2020 Jonathan Horne
#

import serial
import io
import time

#Define the commands for the ERA Synth Micro as listed in the documentation here:
# https://github.com/erainstruments/erasynth-docs/blob/master/erasynth-command-list.pdf
class EraCmd:
    RF_ON           = ">SF1"
    RF_OFF          = ">SF0"
    FREQ            = ">F"      #>F{freq_in_Hz}
    AMP             = ">SA"     #>SA{amplitude_in_dBm} -- resolution is 1 dB
    LCD_HOME_UPDATE = ">GH"     #Updates LCD Home Page
    READ_TEMP       = ">RT"     #Return temp in degrees C
    READ_CURRENT    = ">RC"     #Read current in Amps

class EraSynth:
    SEND_DELAY = 0.1    #back-to-back serial commands don't work so pause this many seconds after sending

    #Constructor
    def __init__(self, serial_device):
        self.ser = serial.Serial(serial_device, 9600, timeout=1, rtscts=1)
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser))

    #Destructor
    def __del__(self):
        self.ser.close()

    #Send a command without a response
    def send_cmd(self, cmd):
        self.sio.write(f"{cmd}\r")
        self.sio.flush()
        time.sleep(self.SEND_DELAY)

    #Send a command without a response and update the display
    def send_cmd_update_display(self, cmd):
        self.sio.write(f"{cmd}\r")
        self.sio.flush()
        time.sleep(self.SEND_DELAY)
        self.sio.write(f"{EraCmd.LCD_HOME_UPDATE}\r")
        self.sio.flush()
        time.sleep(self.SEND_DELAY)

    #Send a command and return the response
    def send_cmd_resp(self, cmd):
        self.sio.write(f"{cmd}\r")
        self.sio.flush()
        response = self.sio.readline()
        resp_clean = response.strip()
        return(resp_clean)

    #read device temperature in degrees C
    def get_temp(self):
        temp = self.send_cmd_resp(f"{EraCmd.READ_TEMP}")
        return temp

    #read device current draw in Amps
    def get_current(self):
        amps = self.send_cmd_resp(f"{EraCmd.READ_CURRENT}")
        return amps

    #set synthesizer frequency
    def set_freq(self, freq):
        ifreq = int(freq)
        self.send_cmd_update_display(f"{EraCmd.FREQ}{ifreq}")

    #set synthesizer amplitude in integer-valued dBm [-50,15]
    def set_dbm(self, amp):
        iamp = int(amp)
        self.send_cmd_update_display(f"{EraCmd.AMP}{iamp}")

    #enable output
    def rf_on(self):
        self.send_cmd_update_display(f"{EraCmd.RF_ON}")

    #disable output
    def rf_off(self):
        self.send_cmd_update_display(f"{EraCmd.RF_OFF}")



if __name__ ==  '__main__':
    #set serial port device for ERAsynth here
    default_serial_dev = '/dev/cu.usbmodem14201'

    #Open device with default serial port
    synth = EraSynth(default_serial_dev)

    #display temperature and current
    tempC = synth.get_temp()
    amps = synth.get_current()
    print(f"Temp = {tempC} deg C")
    print(f"Current = {amps} Amps")

    #Set output frequency
    synth.set_freq(50e6)

    #set output amplitude
    synth.set_dbm(-10)

    #enable the output, pause, then disable
    synth.rf_on()
    time.sleep(2)
    synth.rf_off()
