# streamlogger

Reads from a zeromq pub stream. Displays the data, and logs it.
The stream data should be in the format
```
topic_identifier yyyy-mm-dd HH:MM:SS.microseconds datapoint
```

Example:
```
wa1500 2016-01-07	10:20:07.773000	327518.230000
```

# Requires

- PyQt4 - pip does not install PyQt4 correctly. Get the wheel package from [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/) and install it
- pyqtgraph: `pip install pyqtgraph`
- Zero MQ: `pip install pyzmq`

# Usage
```
cd /path/to/streamlogger
cd streamlogger
python .
```
