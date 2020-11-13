

import network, socket, time
from machine import UART,SPI
from Maix import GPIO
from fpioa_manager import fm
########## config ################
wifi_ap_ssid   = "Sipeed_2.4G"
wifi_ap_passwd = "Sipeed123."
server_ip      = "192.168.0.141"
server_port    = 8000
##################################
addr = (server_ip, server_port)
if 0:
    # En SEP8285
    fm.register(8, fm.fpioa.GPIOHS0, force=True)
    wifi_en=GPIO(GPIO.GPIOHS0,GPIO.OUT)
    fm.register(7,fm.fpioa.UART2_TX, force=True)
    fm.register(6,fm.fpioa.UART2_RX, force=True)
    
    def wifi_enable(en):
        global wifi_en
        wifi_en.value(en)
    
    def wifi_reset():
        global uart
        wifi_enable(0)
        time.sleep_ms(200)
        wifi_enable(1)
        time.sleep(2)
        uart = UART(UART.UART2,115200,timeout=1000, read_buf_len=4096)
        tmp = uart.read()
        uart.write("AT+UART_CUR=115200,8,1,0,0\r\n")
        print(uart.read())
        uart = UART(UART.UART2,115200,timeout=1000, read_buf_len=4096)
        uart.write("AT\r\n")
        tmp = uart.read()
        print(tmp)
        if   tmp==None:
            print("reset fail")
            return None
        try:
            print("try")
            nic = network.ESP8285(uart)
            print(nic)
        except Exception:
            print("e")
            return None
        return nic
    
    clock = time.clock()
    
    nic = None
    while True:
        if not nic or not nic.isconnected():
            nic = wifi_reset()
        if not nic:
            print("wifi reset fail")
            continue
        try:
            print("try1")
            print(nic.isconnected())
            nic.connect(wifi_ap_ssid, wifi_ap_passwd)
            print(nic.ifconfig())
        except Exception:
            print(Exception)
            continue
        if not nic.isconnected():
            print("WiFi connect fail")
            continue
else:
    spi1 = SPI(4, mode=SPI.MODE_MASTER, baudrate=600 * 1000,
            polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=21, mosi=8,miso = 15)
    nic = network.WIZNET5K(spi = spi1, cs = 20, rst = 7)
    print(nic.ifconfig())
    

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)
print("socket send")
sock.sendto("hello udp\n".encode(),addr)
while 1:

    try:
        data, addr = sock.recvfrom(1)
        print(data)
    except Exception as e:
        print("receive error:", e)

sock.close()

#sock = socket.socket()
#sock.connect(addr)
#while 1:

    #sock.send("hello tcp\n")
    #try:
          #data = b""
          #tmp = sock.recv(1)
          #print(tmp)
          #data += tmp
    #except Exception as e:
          #print("rcv:", len(data), data)
        ##time.sleep(2)
    
#sock.close()
