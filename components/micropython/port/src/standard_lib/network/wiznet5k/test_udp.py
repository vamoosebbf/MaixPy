import network, socket
from Maix import GPIO
from fpioa_manager import fm
from board import board_info
import time
from machine import SPI


SERVER_ADDR = "192.168.0.141"
SERVER_PORT = 8000


spi1 = SPI(4, mode=SPI.MODE_MASTER, baudrate=600 * 1000,
        polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=21, mosi=8,miso = 15)
nic = network.WIZNET5K(spi = spi1, cs = 20, rst = 7)
print(nic.ifconfig())

# dhcp
while 1:
    ret = nic.dhclient()
    print(ret)
    if ret:
        print(nic.ifconfig())
        break
            
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)
while 1:
    try:
        sock.sendto("hello\n".encode(),(SERVER_ADDR, SERVER_PORT))
        data, addr = sock.recvfrom(1)
        print(data)
    except Exception as e:
        print("receive error:", e)
        continue
    print("addr:", addr, "data:", data)
    time.sleep(2)

sock.close()