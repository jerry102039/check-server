from check_def import *
#=============================================================================================
def choose_menu_job():
    in_choose_menu=0
    is_button_right_yes=0
    menu=0
    order=0
    try:
        while True:
            if check_button(button_right):
                in_choose_menu+=1
                is_button_right_yes=1
                if in_choose_menu==1:
                    lock.acquire()
                    menu+=1
            elif check_button(button_left):
                in_choose_menu=0
                if in_choose_menu==0 and is_button_right_yes==1:
                    lock.release()
                    menu=0
                    is_button_right_yes=0
                    order=0
            if menu==1:
                if check_button(button_up):
                    order-=1
                elif check_button(button_down):
                    order+=1
                if order==0:
                    msg("homepage")
                elif order==1:
                    msg("cpu and memory")
                elif order==2:
                    msg("network")
                elif order==3:
                    msg("menu test")
                elif order>3 or order<0:
                    order=0
            time.sleep(0.01)
    except Exception as e:
        log_out(f"發生錯誤,錯誤為:{e}")
        msg("Error:",f"{e}")
        exit()
#=============================================================================================
def homepage():
    try:
        while True:
            a=0
            while a!=homepage_waittime:
                a+=runtime()
            for a in range(int(homepage_waittime/cpu_and_memory_waittime)):
                cpu_and_memory()
            for a in range(int(homepage_waittime/network_waittime)):
                network(network_LAN_inf)
    except KeyboardInterrupt:
        log_out("程式被手動停止")
        msg("manually stop")
        exit()
    except Exception as e:
        log_out(f"發生錯誤,錯誤為:{e}")
        msg("Error:",f"{e}")
        exit()
#=============================================================================================
start()
thread1=threading.Thread(target=choose_menu_job)
thread1.daemon = True
thread1.start()
homepage()