import time
from func_connections import connect_dydx
from func_messaging import MSG_QUIT, MSG_EXIT, MSG_HELLO, MSG_GET_POSITIONS, MSG_ABORT_POSITIONS, MSG_NOTHING_TO_DO, send_message, get_message
from func_private import abort_all_positions

def process_quit(client):
    quit()

def process_exit(client):
    exit()  

def process_nothing(client):
    pass

def process_hello(client):
    send_message(MSG_HELLO + " budy")

def process_get_positions(client):
    pass

def process_abort_positions(client):
    abort_all_positions(client)

def process_message(client):
    ops = {
        MSG_NOTHING_TO_DO: process_nothing,
        MSG_QUIT: process_quit,
        MSG_EXIT: process_exit,   
        MSG_HELLO: process_hello,
        MSG_GET_POSITIONS :  process_get_positions,
        MSG_ABORT_POSITIONS : process_abort_positions
    }
    msg = get_message()   
    try: 
        ops.get(msg)(client)
    except Exception as e:
        print("somehing wrong with message " + msg + " can not process this.", e)

""" starttime=time.time()
timeout = time.time() + 60*60*12  # 60 seconds times 60 meaning the script will run for 12 hr
client = connect_dydx()

while time.time() <= timeout:
    try:
        print("script continue running at "+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        process_message(client)
        time.sleep(10 - ((time.time() - starttime) % 10.0)) # 1 minute interval between each new execution
    except KeyboardInterrupt:
        print('\n\KeyboardInterrupt. Stopping.')
        exit() """