import time
from py_eve_chat_mon.monitor import Monitor

if __name__ == "__main__":
    monitor = Monitor(['Alliance', 'Corp', 'testaaaaaaa'], "E:\\Users\\Andrew\\Documents\\EVE\\logs\\Chatlogs\\")
    monitor.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()

    exit()
