*`#drowning`*
===========

Requirements
------------

 * python3
 * pytrends
 * pythonosc
 * colorama
 * termcolor
 * pyfiglet


Installation
------------
OSX:
```
brew install python3 git
git clone https://github.com/davoclavo/drowning.git
cd drowning
pip3 install -r requirements.txt
```

Run
---

```py
python3 drowning_ui.py
```

Usage
-----

  1. Enter Player 1 search term
  2. Enter Player 2 search term
  3. [Enter secret code]


Broadcast
=========

```
brew install ttyrec ngrok
```


### Open a new terminal for each

### · cast


```
ttyreccast /tmp/outfile.tty
```

### · record

```
reset && ttyrec /tmp/ttycast
```

### · tunnel

```
ngrok -subdomain=drowning 13377
```

### · fun

```
train="{ while true; do sl 2>&1; done } | ttycast"
```
