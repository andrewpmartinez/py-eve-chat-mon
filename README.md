Release/Master: ![Release Status](https://travis-ci.org/andrewpmartinez/py-eve-chat-mon.svg?branch=master "Release/Master") Develop: ![Develop Status](https://travis-ci.org/andrewpmartinez/py-eve-chat-mon.svg?branch=develop "Develop")

# Python Eve Chat Monitoring

A library that focuses on monitoring EVE Online chat logs for messages and doing nothing else. It is meant to be focused and lightweight.

### Python Version Support

Python 3.3.x
Python 3.4.x

### To Install

`pip install py-eve-chat-mon`

### Quick-Start

```python
import time
from py_eve_chat_mon.monitor import Monitor

def handler(chat, messages):
    print(chat)
    for msg in messages:
        print(msg)

if __name__ == "__main__":
    monitor = Monitor(['Alliance', 'Corp'], 
                      "C:\\Users\\YourName\\Documents\\EVE\\logs\\Chatlogs\\", 
                      handler)
    monitor.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()

    exit()
```

### Detailed Start

#### Instantiate a Monitor
```python
monitor = Monitor(chats, path, handler, poll_rate=2)
```

```python
monitor = Monitor(['Alliance', 'Corp'], 
          "C:\\Users\\YourName\\Documents\\EVE\\logs\\Chatlogs\\", 
          handler, 
          5)
```
The monitor initializer takes in four arguments:

- `chats` - A `list` of case sensitive `str` chats that should be monitored
- `path` - A `str` path to the EVE chat log directory (The default is in the current user's documents folder)
- `handler` - A callable handler (i.e. a function or any other object that supports the __call__ attribute) that accepts two arguments
 - `chat` - The `str` name of the chat that received a message
 - `messages` - An array of  `dict` representing the chat messages
- `poll_rate` - An optional `int` that represents the seconds to wait between polling intervals on the chat logs. A higher values reduces the responsiveness but lightens the load on the local machines disk I/O

The `messages` array contains message dictionaries that have the following attributes:

- `timestamp` - A `datetime` object representing the game time when the message was received
- `message` - A `str` representing the message portion of the chat log (i.e. just the text the user typed)
- `line` - A `str` representing the entire chat log line (including un-parsed timestamp, username, etc.
- `username` - A `str` representing the username of the user who sent the message
- `hash` - An `str` that uniquely identified this string.

#### Start the monitor

    monitor.start()

The monitor starts its own polling thread as a daemon (meaning it will stay running as long as the main thread is running). It can be stopped by calling `monitor.stop()` and restarted again by `monitor.start()`.

### UTF-16

It is worth noting that Eve's chat logs are in UTF-16. As such messages and text in there can cause issues if you are attempting to print it out to the console in Windows and there happens to be characters outside the consoles supported code points (Unicode charmap errors). You can get around this a little bit by setting the code page in the console to UTF-8 support (run `chcp 65001`), but it isn't perfect.

### Polling?

Yes polling. The initial implementation attempted to use `watchdog` to receive file update events. However, besides the initial creation of the log files, no events are fired in a timely fashion.

### Fun Ideas

I wrote this as a basis of another project. However I have thought of some other things that this could be used for:

 - Watch for keywords (mentions) and provide toast/growl notifications
 - Accumulate chat frequency statistics
 - Stream chat to a central server (away-from-eve reading)

### Unit tests
Unit tests are run on every commit via [Travis-CI](https://travis-ci.org/andrewpmartinez/py-eve-chat-mon)

Release/Master: ![Release Status](https://travis-ci.org/andrewpmartinez/py-eve-chat-mon.svg?branch=master "Release/Master")


Develop: ![Develop Status](https://travis-ci.org/andrewpmartinez/py-eve-chat-mon.svg?branch=develop "Develop")
