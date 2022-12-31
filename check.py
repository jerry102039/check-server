from check_def import *
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
            for a in range(int(homepage_waittime/network_waittime)):
                network(network_WAN_inf)
    except KeyboardInterrupt:
        log_out("程式被手動停止")
        msg("manually stop")
        exit()
    except Exception as e:
        log_out(f"發生錯誤,錯誤為:{e}")
        msg("Error:",f"{e}")
        exit()
#=============================================================================================
def choose_menu_job1():
    in_choose_menu=0
    is_button_right_yes=0
    menu=0
    global order
    global user_select
    try:
        while True:
            #確認是否要進入選單
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
            #確認select是否有被按下
            if check_button(button_select):
                in_choose_menu=0
                if in_choose_menu==0 and is_button_right_yes==1:
                    lock.release()
                    user_select=1
                    menu=0
                    is_button_right_yes=0
            if menu==1:
                #用up和down調整選單順序
                if check_button(button_up):
                    order-=1
                elif check_button(button_down):
                    order+=1
                #顯示選單項目
                if order==0:
                    msg("homepage")
                elif order==1:
                    msg("cpu and memory")
                elif order==2:
                    msg("network(LAN)")
                elif order==3:
                    msg("network(WAN)")
                elif order>3 or order<0:
                    order=0
            time.sleep(0.01)
    except Exception as e:
        log_out(f"發生錯誤,錯誤為:{e}")
        msg("Error:",f"{e}")
        exit()
#=============================================================================================
def choose_menu_job2():
    global user_select
    try:
        while True:
            if check_button(button_left) and user_select>=1:
                lock.release()
                user_select=0
            if user_select==1:
                lock.acquire()
            if user_select>=1:
                user_select+=1
                if order==0:
                    lock.release()
                    user_select=0
                if order==1:
                    cpu_and_memory()
                if order==2:
                    network(network_LAN_inf)
                if order==3:
                    network(network_WAN_inf)
            time.sleep(0.01)
    except Exception as e:
        log_out(f"發生錯誤,錯誤為:{e}")
        msg("Error:",f"{e}")
        exit()
#=============================================================================================
start()
thread1=threading.Thread(target=choose_menu_job1)
thread2=threading.Thread(target=choose_menu_job2)
thread1.daemon = True
thread2.daemon = True
thread1.start()
thread2.start()
homepage()