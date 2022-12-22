from check_def import *
menu=0
def job1():
    global menu
    try:
        while True:
            if check_button(button_right):
                menu=1
            if check_button(button_left):
                menu=0
            print(menu)
    except Exception as e:
        log_out(f"發生錯誤,錯誤為: [{e}]")
        msg("Error:",f"{e}")
        exit()

def job2():
    try:
        while True:
            if menu==0:
                homepage()
            if menu==1:
                msg("menu test")
    except Exception as e:
        log_out(f"發生錯誤,錯誤為: [{e}]")
        msg("Error:",f"{e}")
        exit()

start()
stop=False
thread1=threading.Thread(target=job1)
thread2=threading.Thread(target=job2)
thread1.daemon = True
thread2.daemon = True
thread1.start()
thread2.start()
try:
    while True:
        time.sleep(1000000)
except KeyboardInterrupt:
    log_out("程式被手動停止")
    msg("manually stop")
    exit()