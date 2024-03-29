import psutil
from pyfirmata2 import Arduino,util,STRING_DATA,PWM
from ping3 import ping
import time
import os
import configparser
from datetime import datetime
import threading
import json
#=============================================================================================
lock=threading.RLock()
config=configparser.ConfigParser()
boottime=datetime.fromtimestamp(psutil.boot_time())
config.read("config.ini", encoding="utf-8")
logfile_size=config.getint("global","logfile_size")
port=config.get("global","port")
light_change=config.getfloat("global","light_change")
lcdlight_pin=config.getint("global","lcdlight_pin")
start_waittime=config.getfloat("wait_time","start_waittime")
ping_waittime=config.getint("wait_time","ping_waittime")
cpu_and_memory_waittime=config.getfloat("wait_time","cpu_and_memory_waittime")
network_waittime=config.getfloat("wait_time","network_waittime")
network_LAN_inf=config.get("global","network_LAN_inf")
network_WAN_inf=config.get("global","network_WAN_inf")
homepage_waittime=config.getint("wait_time","homepage_waittime")
servername=config.get("global","servername")
want_ping_service=json.loads(config.get("global","want_ping_service"))
button_right=range(0,60)
button_up=range(60,200)
button_down=range(200,400)
button_left=range(400,600)
button_select=range(600,800)
button_open=True
lcdlight=0
order=0
user_select=0
#=============================================================================================
def start():#讓Arduino連線
    global board
    log_out("開始執行")
    try:
        board=Arduino(port)
    except Exception as e:
        log_out(f"連線失敗,原因: {e}")
        exit()
    log_out(f"連線成功")
    board.samplingOn()
    board.digital[lcdlight_pin].mode=PWM
    board.digital[lcdlight_pin].write(1)
    log_out("啟動中")
    for i in range(10):
        a=i*"."
        board.digital[13].write(1)
        time.sleep(start_waittime/2)
        board.digital[13].write(0)
        time.sleep(start_waittime/2)
        msg(f"Loading{a}")
    log_out("開始發送數據")
#=============================================================================================
def msg(text1:str,text2:str=" "):#讓Lcd印出文字
    lock.acquire()
    if text1 or text2:
        board.send_sysex(STRING_DATA,util.str_to_two_byte_iter(f"{text1}               "))
        board.send_sysex(STRING_DATA,util.str_to_two_byte_iter(f"{text2}               "))
    else:
        board.send_sysex(STRING_DATA,util.str_to_two_byte_iter(' '))
    lock.release()
#=============================================================================================
def analong(pin:int)-> int:#讀取數位訊號
    time.sleep(0.001)
    lock.acquire()
    analong_read=board.analog[pin].read()
    board.analog[pin].enable_reporting()
    lock.release()
    if analong_read!=None:
        return int(analong_read*1023)
    return 1023
#=============================================================================================
def cpu_and_memory():#顯示CPU和memory狀態
    cpu=f"cpu:    {psutil.cpu_percent(interval=cpu_and_memory_waittime)}%"
    memory=f"memory: {psutil.virtual_memory().percent}%"
    msg(cpu,memory)
#=============================================================================================
def network(connect:str):#顯示網路狀態
    net_stat = psutil.net_io_counters(pernic=True)[connect]
    net_in_1 = net_stat.bytes_recv
    net_out_1 = net_stat.bytes_sent
    time.sleep(network_waittime)
    net_stat = psutil.net_io_counters(pernic=True)[connect]
    net_in_2 = net_stat.bytes_recv
    net_out_2 = net_stat.bytes_sent
    net_in = round((net_in_2-net_in_1)/1024/1024*8,3)
    net_out = round((net_out_2-net_out_1)/1024/1024*8,3)
    msg(f"in: {net_in} Mbps",f"out:{net_out} Mbps")
#=============================================================================================
def check_button(button:range):#判斷按鍵是否有被按下
    global button_open
    now_analong=analong(0)
    while now_analong<1000 and button_open==True and now_analong in button:
        button_open=False
        return True
    else:
        if now_analong>1000 and button_open!=True:
            button_open=True
        return False
#=============================================================================================
def lcd_light_breathe():#讓Lcd的背光呼吸
    global lcdlight
    global light_change
    if lcdlight>1 or lcdlight<0:
        light_change=-light_change
    lock.acquire()
    board.digital[lcdlight_pin].write(lcdlight)
    lock.release()
    lcdlight+=light_change
#=============================================================================================
def log_out(text:str):#輸出文字到Log中
    try:
        if os.stat("check.log").st_size/(1024 * 1024) <logfile_size:
            writemode="a"
        else:
            writemode="w"
        with open("check.log",writemode,encoding="utf-8") as log:
            print(f"[{datetime.now()}] {text}",file=log)
            print(text)
    except:
        with open("check.log","w",encoding="utf=8") as log:
            print(f"[{datetime.now()}] {text}",file=log)
            print(text)
#=============================================================================================
def runtime():#顯示服務器運作時間
    global boot_runtime2
    global boot_runtime1
    boot_runtime1=str(datetime.now()-boottime).split('.')[0]
    time.sleep(0.001)
    boot_runtime2=str(datetime.now()-boottime).split('.')[0]
    if boot_runtime1!=boot_runtime2:
        msg(servername,f"Run: {boot_runtime1}")
        return 1
    return 0
#=============================================================================================
def ping_service(service:str,ip:str):#ping某個服務
    if ping(ip,timeout=ping_waittime):
        log_out(f"{service}=> OK")
        #msg(f"{service}=> OK")
    else:
        log_out(f"{service}=> Error")
        #msg(f"{service}=> Error")
#=============================================================================================
def ping_all_service():
    for service in want_ping_service:
        ping_service(service,want_ping_service[service])
#=============================================================================================