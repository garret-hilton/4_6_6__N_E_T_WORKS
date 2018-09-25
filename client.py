from socket import *
import sys, requests, http.client


def client(port, gameServer, x, y):

	host = 'localhost'
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((host, port))  				#connect

	fireCoordinates = 'x='+str(x)+'&y='+str(y)
	clientSocket = http.client.HTTPConnection('localhost', port)
	clientSocket.request("POST", "", fireCoordinates)

	response = clientSocket.getresponse()
	print("Status", response.status)
	print("Reason", response.reason)
	data = response.read()
	data = data.decode()
	clientSocket.close()

	if(response.status == 200):								#posts the retuned data to players server to view oponents board
			print (data)



if __name__ == "__main__":
	gameServer = sys.argv[1]							#Server IP address
	port = int(sys.argv[2])								#port for server
	x = sys.argv[3]										#x fire coordinate
	y = sys.argv[4]										#y fire coordinate
	client(port, gameServer, x, y)
