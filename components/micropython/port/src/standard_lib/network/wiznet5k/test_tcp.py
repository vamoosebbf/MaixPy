

import socket, network, time
import lcd, image
from Maix import GPIO
from machine import UART,SPI
from fpioa_manager import fm
from board import board_info

SERVER_ADDR = "192.168.0.141"
SERVER_PORT = 80000


spi1 = SPI(4, mode=SPI.MODE_MASTER, baudrate=600 * 1000,
        polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=21, mosi=8,miso = 15)
nic = network.WIZNET5K(spi = spi1, cs = 20, rst = 7)
print(nic.ifconfig())
while 1:
    ret = nic.dhclient()
    if ret:
        print(nic.ifconfig())
        break
            
sock = socket.socket()
sock.connect((SERVER_ADDR, SERVER_PORT))

sock.settimeout(3)
while 1:
    sock.send("hello\n")
    #data = sock.recv(10) # old maxipy have bug (recv timeout no return last data)
    #print(data) # fix
    try:
      data = b""
      while True:
        tmp = sock.recv(1)
        print(tmp)
        if len(tmp) == 0:
            raise Exception('timeout or disconnected')
        data += tmp
    except Exception as e:
      print("rcv:", len(data), data)
    #time.sleep(2)

sock.close()
