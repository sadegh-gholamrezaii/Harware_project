from machine import UART, Pin

import time

from esp8266 import ESP8266

from machine import  I2C

from ssd1306 import SSD1306_I2C
WIDTH =128 
HEIGHT= 64
i2c=I2C(0,scl=Pin(5),sda=Pin(4),freq=200000)
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)
list_led = [Pin(13, Pin.OUT),Pin(12, Pin.OUT),Pin(10, Pin.OUT),Pin(9, Pin.OUT),Pin(8, Pin.OUT),Pin(7, Pin.OUT)]

def control_led_with_integer(num_6):
    count = 0
    for val in num_6:
        list_led[count].value(int(val))
        count += 1
        
def all_led_on():
    for led in list_led:
        led.value(1)
        
def all_led_off():
    for led in list_led:
        led.value(0)
                
esp01 = ESP8266()

esp8266_at_ver = None

led=Pin(25,Pin.OUT)

print("StartUP",esp01.startUP())
oled.text("StartUP", 0, 16)
oled.show()

#print("ReStart",esp01.reStart())

print("StartUP",esp01.startUP())
oled.text("StartUP", 0, 24)
oled.show()

print("Echo-Off",esp01.echoING())
oled.text("Echo-Off", 0, 36)
oled.show()

print("\r\n\r\n")

'''

Print ESP8266 AT command version and SDK details

'''

esp8266_at_var = esp01.getVersion()

if(esp8266_at_var != None):

    print(esp8266_at_var)

'''

set the current WiFi in SoftAP+STA

'''

esp01.setCurrentWiFiMode()

apList = esp01.getAvailableAPs()
name_of_access_wifi = []
for items in apList:
    name_of_access_wifi.append(items)
    #print(items)

    #for item in tuple(items):

    #    print(item)
print(name_of_access_wifi)
print("\r\n\r\n")


led = Pin(25, Pin.OUT)

led.toggle()
time.sleep(0.7)
led.value(0)


oled.fill(0)
oled.text("WiFi availables:", 0, 0)
oled.show()

x = 0
y = 16
 
for i in name_of_access_wifi:
    oled.text(i[1], x, y)
    y += 8
oled.show()
time.sleep(0.125)
#oled.fill(0)    


print("Try to connect with the WiFi..")
oled.text("Try connect WiFi", 0, 48)
oled.show()
err_ = "o"
while (1):

    #if "WIFI CONNECTED" in esp01.connectWiFi("TP-LINK","1424344454"):
    if "WIFI CONNECTED" in esp01.connectWiFi("Galaxy A30sA0C2" , "khalvai#9003"):
        print("ESP8266 connect with the TP-LINK")
        
        oled.fill(0)
        oled.text("ESP8266 connect with", 0, 16)
        oled.text("TP-LINK", 8, 24)
        oled.show()
        time.sleep(0.125)
        break;

    else:

        print(".")
        err_ += "o"
        oled.text(err_, 0, 56)
        oled.show()

        time.sleep(2)

print("\r\n\r\n")

print("Now it's time to start HTTP Get/Post Operation.......\r\n")
datas = {} 
while(1):   

    led.toggle()

    time.sleep(0.5)

    '''
    Going to do HTTP Get Operation with www.httpbin.org/ip, It return the IP address of the connected device
    '''
    
    #httpCode, httpRes = esp01.doHttpGet("www.httpbin.org","/ip","RaspberryPi-Pico", port=80)
    #httpCode, httpRes = esp01.doHttpGet("192.168.1.4","/", port=80)
    #httpCode, httpRes = esp01.doHttpGet("circuitdigest.com","/microcontroller-projects/interfacing-esp8266-01-wifi-module-with-raspberry-pi-pico","RaspberryPi-Pico", port=80)
    #httpCode, httpRes = esp01.doHttpGet("www.tala.ir","/price/sekke-grm","RaspberryPi-Pico", port=80)
    
    #data_raw, httpRes_noting = esp01.doHttpGet("192.168.1.4","/", port=80)
    data_raw, httpRes_noting = esp01.doHttpGet("192.168.32.239","/", port=80)
    
    if data_raw == 0:
        
        oled.fill(0)
        oled.text("can not requests", 0, 0)
        oled.text("Please check", 0, 8)
        oled.text("Pleas run server", 0, 16)
        oled.show()
        continue
    
    
    structure_data = data_raw.decode().split('class="data"')[1][6:].split("\n}\n</pre>")[0].replace('"','').split(",\n  ")
    for item in structure_data:
        key,val = item.split(":")
        datas[key] = val
    
    oled.fill(0)
    oled.text('text_ssd : ', 0, 0)
    str_show = datas['text_ssd']
    len_str_show = len(str_show)
    if len_str_show > 16 :
        start = 0
        end = 16
        row = 16
        while(start < len_str_show ):
            oled.text(str_show[start:end], 0, row)
            start, end, row = start + 16, end + 16, row+8
            
        
    else:
        oled.text(str_show, 0, 16)
    oled.show()
    
    '''
    print("-*-*-*-*-*-*-*-* Get Operation Result *-*-*-*-*-*-*-*-")
    print("HTTP Code:",httpCode)
    print("HTTP Response:",httpRes)
    print("-----------------------------------------------------------------------------\r\n\r\n")
    '''
    
    print(datas)
    
    #control_led_with_integer(datas["led"].strip())
    control_led_with_integer(datas['led_tick'].strip())

    
    '''
    Going to do HTTP Post Operation with www.httpbin.org/post

    post_json="abcdefghijklmnopqrstuvwxyz"  #"{\"name\":\"Noyel\"}"

    httpCode, httpRes = esp01.doHttpPost("www.httpbin.org","/post","RPi-Pico", "application/json",post_json,port=80)

    print("------------- www.httpbin.org/post Post Operation Result -----------------------")

    print("HTTP Code:",httpCode)

    print("HTTP Response:",httpRes)

    print("--------------------------------------------------------------------------------\r\n\r\n")

    #break
    '''




