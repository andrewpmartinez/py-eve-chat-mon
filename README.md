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

- `chats` - A `list` of `str` chats that should be monitored
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
- `hash` - An `int` that uniquely identified this string. It is generated from the MurmurHash3 algorithm (via the package mmh3). The hash is created from the `message` attribute.

#### Start the monitor

    monitor.start()

The monitor starts its own polling thread as a daemon (meaning it will stay running as long as the main thread is running). It can be stopped by calling `monitor.stop()` and restarted again by `monitor.start()`.

### UTF-16

It is worth noting that Eve's chat logs are in UTF-16. As such messages and text in there can cause issues if you are attempting to print it out to the console in Windows and there happens to be characters outside the consoles supported code points (Unicode charmap errors). You can get around this a little bit by setting the code page in the console to UTF-8 support (run `chcp 65001`), but it isn't perfect.

### mmh3

You will need to be able to compile C packages. If you are on Windows, the easiest way is to install Visual Studio Community Edition (free) and then ensure you set your `VS1000COMNTOOLS` environment variable to `C:\Program Files (x86)\Microsoft Visual Studio 12.0\Common7\Tools`; where 12.0 may change based on which version of Visual Studio is out (i.e. 2013 = 12.0 and the next will be 13.0, etc).

If you don't want to do that, you can go the MinGW (http://www.mingw.org/) route. I leave that to the reader to research.

### Polling?

Yes polling. The initial implementation attempted to use `watchdog` to recieve file update events. However, besides the initial creation of the log files, no events are fired in a timely fashion.

### Fun Ideas

I wrote this as a basis of another project. However I have thought of some other things that this could be used for:

 - Watch for keywords (mentions) and provide toast/growl notifications
 - Accumulate chat frequency statistics
 - Stream chat to a central server (away-from-eve reading)

### Unit tests & comments

I will be working on test coverage and code documentation shortly.
