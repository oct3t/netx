import sys
import socket
import threading
import getopt
import subprocess

# Define global vars

listen	= False
command	= False
upload	= False
execute	= ""
target	= ""
upload_destination = ""
port	= 0

# Main usage function 

def usage():
	print
	print "============================="
	print "NetX - Network Tool by @oct3t"
	print "============================="
	print
	print "Usage: netx.py -t target_host -p port"
	print "-l --listen				- listen on [host]:[port] for incoming connections"
	print "-e --execute=file_to_run		- execute the given file upon receiving a connection"
	print "-c --command				- initialize a command shell"
	print "-u --upload=destination 		- upon receiving a connection upload a file and write to [destination]"
	print
	print
	print "Examples: "
	print "netx.py -t 192.168.0.1 -p 5555 -l -c"
	print "netx.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
	print "netx.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
	print "echo 'ABCDEFGHI' | ./netx.py -t 192.168.11.12 -p 135"
	print
	sys.exit(0)

def client_sender(buffer):

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	print "[*] Client Sender Target: %s, Port: %s" % (target, port)

	try: 
		# Connect to our target host
		client.connect((target, port))
		
		# Send buffer if any
		if len(buffer):
			client.send(buffer)

		while True:
			# Wait for data back
			recv_len = 1
			response = ""

			# While data < 4069
			while recv_len:
				data = client.recv(4096)
				recv_len = len(data)
				response += data
	
				if recv_len < 4096:
					break

			# Print out data
			print response,

			# Wait for more input
			buffer = raw_input("")
			buffer += "\n"

			# Send it off
			client.send(buffer)

	except: 
		print "[*] Exception! Closing Socket -> Exiting."

		# Close client connection
		client.close()


def server_loop():
	global target

	# If no target is defined, listen to all interfaces
	if not len(target):
		target = "0.0.0.0"
	
	# Bind server to target, port	
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((target, port))
	# Listen for up to 5 connections
	server.listen(5)

	while True:
		client_socket, addr = server.accept()

		# Spin off a thread to handle client
		client_thread = threading.Thread(target=client_handler, args=(client_socket,))
		print "[*] Client Connected: %s at Address: %s" % (client_socket, addr)
		client_thread.start()


def run_command(command):
	# Trim the newline
	command = command.rstrip()

	# Run the command and get the output back
	try:
		output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
	except:
		output = "Failed to execute the command.\r  \n"

	# Send the output back to the client
	return output


def client_handler(client_socket):
	global upload
	global execute
	global command

	# print "[*] Client socket %s" % client_socket

	# Check for upload
	if len(upload_destination):

		# Read in all bytes and write to dest
		file_buffer = ""

		# Keep reading data until none is available
		while True:
			data = client_socket.recv(1024)
			if not data:
				break
			else:
				file_buffer += data

		try:
			# Write the file form the buffer to dest
			file_descriptor = open(upload_destination, "wb")
			file_descriptor.write(file_buffer)
			file_descriptor.close()
		except:
			# Acknowledge that we couldn't write out file
			client_socket.send("Failed to save file to %s\r\n" % upload_destination)

	# Check for command execution
	if len(execute):
		print "[*] Command Execution: %s" % execute
		# Run the command
		output = run_command(execute)
		client_socket.send(output)

	# Go into another loop if a command shell was requested
	if command:
		print "[*] Command Requested."
		while True:
			# Show simple prompt
			client_socket.send("<NetX:#> ")
			# Now receive untill linefeed (Enter key)
			cmd_buffer = ""
			while "\n" not in cmd_buffer:
				cmd_buffer += client_socket.recv(1024)
			# Send back the cmd output
			response = run_command(cmd_buffer)

			# Send back response
			client_socket.send(response)


def main():
	global listen
	global port
	global execute
	global command
	global upload_destination
	global target


	# Call usage() func if no args
	if not len(sys.argv[1:]):
		usage()

	# Read the command line opts
	try: 
		opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "target", "port", "command", "upload"])
	except getopt.GetoptError as err:
		print str(err)
		usage()

	for o,a in opts:

		if o in ("-h", "--help"):
			usage()
		elif o in ("-l", "--listen"):
			listen = True
		elif o in ("-e", "--execute"):
			execute = a
		elif o in ("-c", "--command"):
			command = True
		elif o in ("-u", "--upload"):
			upload_destination = a
		elif o in ("-t", "--target"):
			target = a
		elif o in ("-p", "--port"):
			port = int(a)
		else: 
			assert False, "Unhadled option"

	# Are we listening or just send data from stdin
	if not listen and len(target) and port > 0:
		
		print "[*] Sending Data. Host: %s, Port: %s" % (target, port)		

		# Read in the buffer from the commandline
		# This will block, so send CTRL-D 
		# if not sending input to stdin
		buffer = sys.stdin.read()

		# Send data off
		client_sender(buffer)

	# Listen and potentially upload things,
	# execute commands, and drop shell back 	
	# depending on our command line options above	
	if listen:
		print "[*] Listening. Port: %s, Command: %s" % (port, command)    
		server_loop()

main()
