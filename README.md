# Python Eve Chat Monitoring

A library that focuses on monitoring EVE Online chat logs for messages and doing nothing else. It is meant to be focused and lightweight.

### To Install

`pip install py-eve-chat-mon`

### Quick-Start

    import time
    from py_eve_chat_mon.monitor import Monitor
    
    def handler(chat, msg):
        print(chat)
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


### Detailed Start

#### Instantiate a Monitor

    monitor = Monitor(chats, path, handler, poll_rate=2)

```
    monitor = Monitor(['Alliance', 'Corp'], 
              "C:\\Users\\YourName\\Documents\\EVE\\logs\\Chatlogs\\", 
              handler, 
              5)
```
The monitor initializer takes in four arguments:

- `chats` - A `list` of chats it should monitor
- `path` - A `str` path to the EVE chat log directory (The default is in the current user's documents folder)
- `handler` - A callable handler (i.e. a function or any other object that supports the __call__ attribute) that accepts two arguments
 - `chat` - The `str` name of the chat that received a message
 - `msg` - A `dict` representing the chat message
- `poll_rate` - An optional `int` that represents the seconds to wait between polling intervals on the chat logs. A higher values reduces the responsiveness but lightens the load on the local machines disk I/O

The `msg` dictionary that is passed into the handler has the following attributes:

- `timestamp` - A `datetime` object representing the game time when the message was recieved
- `message` - A `str` representing the message portion of the chat log (i.e. just the text the user typed)
- `line` - A `str` representing the entire chat log line (including un-parsed timestamp, username, etc.
- `username` - A `str` representing the username of the user who sent the message
- `hash` - An `int` that uniquely identified this string. It is generated from the MurmurHash3 algorithm (via the package mmh3)

#### Start the monitor

    monitor.start()

The monitor starts its own polling thread as a daemon (meaning it will stay running as long as the main thread is running). It can be stopped by calling `monitor.stop()` and restarted again by `monitor.start()`.

### Unit tests & comments

I will be working on test coverage and code documentation shortly.
