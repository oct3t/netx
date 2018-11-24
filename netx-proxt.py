import sys
import socket
import threading

def server_loop(local_host, local_port, remote_host, remote_port, recieve_fist):

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		server.bind((local_host, local_port))
	except:
		print "[!!] Failed to listen on %s:%d" % (local_host, local_port)
		print "[!!] Check for other listening sockets or correct permissions."
		sys.exit(0)

	print "[*] Listening on %s:%d" % (local_host, local_port)

	server.listen(5)

	while.True:
		client_socket, addt = server.accept()

		# Print out the local conection information
		print "[=>] Received incoming connection from %s:%d" % (addr[0], addr[1])

		# Start a thread to talk to the remote host
		proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))

		proxy_thread.start()

def proxy_handler:

def server_loop():

def main():

	# Obivate the fancy commandline paarsing here

	if len(sys.argv[1:]) != 5:
		print
		print "=========================="
		print " NetX Proxy Tool by @oct3t"
		print "=========================="
		print
		print "Usage: ./netx-proxy.py [localhost] [localport] [remotehost] [remoteport] [receivefist]"
		print "Example: ./netx-proxy.py 127.0.0.1 9000 10.13.132.1 9000 True"
		print

		sys.exit(0)

	# Setup local listening parameters	
	local_host = sys.argv[1]
	local_port = int(sys.argv[2])

	# Setup remote target
	remote_host = sys.argv[3]
	remote_port = int(sys.argv[4])

	# Tell our proxy to connect and recieve data
	# before sending to the remote host	
	receive_first = sys.argv[5]

	if "True" in receive_first:
		receive_first = True
	else:
		receive_first = False

	# We now spin our sever loop

	server_loop(local_host, local_port, remote_host, remote_port, receive_firxt)

main()










