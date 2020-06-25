#!python
#
# synth_example.py
#
# Demonstrate use of the EraSynth class
#
# (C)2020 Jonathan Horne
#
import erasynth
import time

#Open device
# This is the default serial port device for the ERAsynth Micro on my Mac.
# Yours will likely differ.
synth = erasynth.EraSynth('/dev/cu.usbmodem14201')

#Display temperature and current
tempC = synth.get_temp()
amps = synth.get_current()
print(f"Temp = {tempC} deg C")
print(f"Current = {amps} Amps")

#Set output frequency in Hz
synth.set_freq(500e6)

#Set output amplitude in dBm
synth.set_dbm(-12)

#Enable the output, pause, then disable
synth.rf_on()
time.sleep(2)
synth.rf_off()

