import time
from py_eve_chat_mon.monitor import Monitor

def handler(chat, msg):
    print(chat)
    print(msg)

if __name__ == "__main__":
    monitor = Monitor(['Alliance', 'Corp', 'testaaaaaaa', 'ESC.Delve', 'ESC.PeriodBasis', 'ESC.Querious'], "E:\\Users\\Andrew\\Documents\\EVE\\logs\\Chatlogs\\", handler)
    monitor.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()

    exit()
