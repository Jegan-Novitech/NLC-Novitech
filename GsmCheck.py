import serial   
import os, time
 
# Enable Serial Communication
port = serial.Serial("/dev/ttyTHS1", baudrate=9600, timeout=1)
 
# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key
temp='AT\r\n' 
port.write(temp.encode())
rcv = port.read(10)
print (rcv)
