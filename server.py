import sys, urllib
from socket import *
from urllib.parse import urlparse



###########################################################################################
### 								Server Battleship									###
###########################################################################################
###########################################################################################
### 								Start of Main Loop 									###
###########################################################################################
def server(port, board, name):

	opponentGameBoard = generateEmptyBoard('?')
	if name == 'board.txt':
		writeHTMLBoard('opponent_board.html', opponentGameBoard)
	else:
		writeHTMLBoard('opponent_board2.html', opponentGameBoard)
	gameBoard = board
	gameServer = socket(AF_INET, SOCK_STREAM)
	gameServer.bind(('localhost', port))
	gameServer.listen(3)

	print('Starting Battleship Game Server\n')
	if name == 'board.txt':
		writeHTMLBoard('own_board.html', gameBoard)						#write the new board to the own_board.html page
	else:
		writeHTMLBoard('own_board2.html', gameBoard)
	carrierCount = 0												#counter variables to keep track
	battleshipCount = 0												#if the ships are sunk or not
	destroyerCount = 0
	subCount = 0
	cruiserCount = 0
	x = 0
	y = 0
	selectBoard = 0
	code = 410
	while True:
		connectionSocket, addr = gameServer.accept()
		data = connectionSocket.recv(2048) 							#Save the data comming in
		data = data.decode()
		#print(data)
		sink = '0'
		hit = 0
		opponentHIT = 0
		pageRequested = ''
		if data:
			method = data.split(' ')[0]
			sink = '0'												#variable to flag if current shot sunk a ship
			hit = 0
			print ('Received: ' + method)
	###########################################################################################
	### 								  POST  Handler 									###
	###########################################################################################
			if method == 'POST':
				print("Servicing: POST")
				file_requested = data.split(' ')
				pageRequested = file_requested[1]
				x,y,opponentHIT,code = getCoordinates(data)
				code = testCoordinates(x, y, gameBoard, data)		#sets the corresonding code accoding to posted values
	###########################################################################################
	### 								  GET  Handler 										###
	###########################################################################################
			if method == 'GET':								#handles the GET protocols
				file_requested = data.split(' ')
				pageRequested = file_requested[1]
				#print(pageRequested)
				if(pageRequested == '/own_board.html'):
					code = 200
				elif(pageRequested == '/opponent_board.html'):
					code = 200
				elif(pageRequested == '/own_board2.html'):
					code = 200
					selectBoard = 1
				elif(pageRequested == '/opponent_board2.html'):
					code = 200
					selectBoard = 1
				elif(pageRequested == '/'):
					code = 501
				else:
					code = 404

				print('Servicing GET')
	###########################################################################################
	### 								  GAME LOGIC	 									###
	###########################################################################################
			if (code == 404 or code == 410 or code == 400):
				print('Bad Request')
				if method == 'GET':
					response =  'HTTP/1.1 200 OK\n\n<html><body>'
					response +=	'<font size = "6"><p style="font-family:courier;">'
					response +=	'\n\n\n'
					response +=	'<p>BAD REQUEST</p></font></body><html>\n'
					connectionSocket.send(response.encode())
			elif (code == 200 and method == 'POST'):
				#print('\nx equals =', x)
				#print("\ny equals =", y)
				shot = gameBoard[y][x]								#gets the char at the x,y cords
				#print (shot)
				if shot == '_':
					gameBoard = updateBoard('M', y, x, gameBoard)	#update gameBoard with a ' ' if you miss
					print('Miss')
				elif shot == 'C':
					carrierCount += 1
					gameBoard = updateBoard('X', y, x, gameBoard)
					print('Hit')
					hit = 1
					if carrierCount == 5:
						print('SINK')
						sink = 'C'
				elif shot == 'D':
					destroyerCount += 1
					gameBoard = updateBoard('X', y, x, gameBoard)
					print('Hit')
					hit = 1
					if destroyerCount == 2:
						print('SINK')
						sink = 'D'
				elif shot == 'B':
					battleshipCount += 1
					gameBoard = updateBoard('X', y, x, gameBoard)
					print('Hit')
					hit = 1
					if battleshipCount == 4:
						print('SINK')
						sink = 'B'
				elif shot == 'R':
					cruiserCount += 1
					gameBoard = updateBoard('X', y, x, gameBoard)
					print('Hit')
					hit = 1
					if cruiserCount == 3:
						print('SINK')
						sink = 'R'
				elif shot == 'S':
					subCount += 1
					gameBoard = updateBoard('X', y, x, gameBoard)
					print('Hit')
					hit = 1
					if subCount == 3:
						print('SINK')
						sink = 'S'
				else:												#Grabs any other mesages that are not GET or POST
					code = 400										#assigns error code Bad Request
				if (selectBoard == 0):
					writeHTMLBoard('own_board.html', gameBoard)
					if hit == 1:
						opponentGameBoard = updateBoard('X', y, x, opponentGameBoard)
					else:
						opponentGameBoard = updateBoard('M', y, x, opponentGameBoard)
					writeHTMLBoard('opponent_board.html', opponentGameBoard)
				else:
					writeHTMLBoard('own_board2.html', gameBoard)
					if hit == 1:
						opponentGameBoard = updateBoard('X', y, x, opponentGameBoard)
					else:
						opponentGameBoard = updateBoard('M', y, x, opponentGameBoard)
					writeHTMLBoard('opponent_board2.html', opponentGameBoard)
			else:
				pass
				#print("got here")
		dataToSend = 'x='+str(x)+'&y='+str(y)+'&'
		dataToSend += 'hit='+str(hit)
	###########################################################################################
	### 								SEND THE RESPONSE									###
	###########################################################################################
		if code == 200 and method == 'POST':
			if sink != '0':
				dataToSend += '&sink='+str(sink)+'\n'
			else:
				dataToSend += '\n'
			response = 'HTTP/1.1 200 OK\n\n' + dataToSend
			connectionSocket.send(response.encode())
		elif code == 404:
			response = 'HTTP/1.1 404 NotFound\n\n\n'
			connectionSocket.send(response.encode())
		elif code == 400:
			response = 'HTTP/1.1 400 BadRequest\n\n\n'
			connectionSocket.send(response.encode())
		elif code == 410:
			response = 'HTTP/1.1 410 Gone\n\n\n'
			connectionSocket.send(response.encode())
		elif (code == 200 and method == 'GET'):

			if (pageRequested == '/opponent_board.html'):
				fileHandler = open('opponent_board.html', 'r')
				fileContent = fileHandler.read()
				fileHandler.close()
				response = fileContent
				connectionSocket.send(response.encode())
			elif (pageRequested == '/own_board.html'):
				fileHandler = open('own_board.html', 'r')
				fileContent = fileHandler.read()
				fileHandler.close()
				response = fileContent
				connectionSocket.send(response.encode())
			elif (pageRequested == '/opponent_board2.html'):
				fileHandler = open('opponent_board2.html', 'r')
				fileContent = fileHandler.read()
				fileHandler.close()
				response = fileContent
				connectionSocket.send(response.encode())
			else:
				fileHandler = open('own_board2.html', 'r')
				fileContent = fileHandler.read()
				fileHandler.close()
				response = fileContent
				connectionSocket.send(response.encode())
		elif(code == 600):
			if opponentHIT == 1:
				opponentGameBoard = updateBoard('X', y, x, opponentGameBoard)
			else:
				opponentGameBoard = updateBoard('M', y, x, opponentGameBoard)
			writeHTMLBoard('opponent_board.html', opponentGameBoard)
			response = 'HTTP/1.1 200 OK\n\n'
			connectionSocket.send(response.encode())
			print ('Got to 600 send')
		else:
			response =  'HTTP/1.1 200 OK\n\n<html><body>'
			response +=	'<font size = "6"><p style="font-family:courier;">'
			response +=	'\n\n\n<br>BATTLESHIP<br>powered by python</p>'
			response +=	'<p>Python HTTP Server</p></font></body><html>\n'
			connectionSocket.send(response.encode())
		connectionSocket.close()
		print("\n")
###########################################################################################
### 								END OF MAIN LOOP 									###
###########################################################################################


###########################################################################################
### 									FUNCTIONS 										###
###########################################################################################

def writeHTMLBoard(file, gameBoard):						#write the given board to the given html file
	done = False
	i = 0
	j = 0
	string = 'HTTP/1.1 200 OK\n\n<html><body>'				#saves the headers for the Response in the webpage
	string +='<font size = "6"><p style="font-family:courier;">'
	string +='\n\n\n&emsp;&emsp;123456789<br>'
	string += '' + str(i) + '   '
	while done == False:
		string += gameBoard[i][j]
		j += 1
		if j == 10:
			i += 1
			j = 0
			string += '<br>'
			if (i < 10):
				string += '' + str(i) + '   '
		if i == 10:
			done = True
	string += 	'<br>B = Battleship<br>C = Carrier<br>D = Destroyer<br>M = Miss<br>R = Cruiser<br>S = Submarine<br>X = hit<br>'
	string +=	'<p>Python HTTP Server</p></font></body><html>\n'
	htmlFile = open(file, 'w')
	htmlFile.write(string)
	htmlFile.close()

def generateEmptyBoard(char):							#generate empty board with specific char
	i = 0
	newBoard = []
	done = False
	while(done == False):
		line = '??????????'
		if i < 10:
			newBoard.append(line)
			i += 1
		else:
			done = True
	return newBoard

def testCoordinates(x, y, gameBoard, data):					#tests the coodinates and returns associated error code
	code = 400											#default code is Bad Request
	coordinates = data.split('\r\n\r\n', 1)[1]
	if (coordinates ==''):
		print ("No data to Process")
	else:
		coordinates = coordinates.split('&')
		#try:
		#	hitFieldandValue = coordinates[2]
		#	print ('found hit field')
		#	code = 600
		#except Exception as e:
		#	print('no hit field found')

	if (x >= 0 and x <= 9 and y >= 0 and y <= 9 and code != 600):
		if (gameBoard[y][x] == 'X' or gameBoard[y][x] == 'M'):
			code = 410									#GONE
		else:
			code = 200									#OK
	elif (x < 0 or x > 9 or y < 0 or y > 9):
		code = 404										#NOT Found
	elif (code == 600):
		code = 600
	else:
		code = 400										#Bad Request
	return code

def updateBoard(newChar, x, y, gameBoard):				#function to update the gameboard with new shot
		done = False									#updates the gameBoard variable
		i = int(0)
		j = int(0)
		newBoard = []
		line = ''
		while done == False:
			if i == x:
				if j == y:
					line = ''.join((line, newChar))
				else:
					line = ''.join((line, gameBoard[i][j]))
			else:
				line = ''.join((line, gameBoard[i][j]))
			j += 1
			if j == 10:
				i += 1
				j = 0
				newBoard.append(line)
				#print(line)
				line = ''
			if i == 10:
				done = True
		return newBoard

def getCoordinates(data):  								#pulls the coordinates out of the fire POST
	coordinates = data.split('\r\n\r\n', 1)[1]  		#grab the data containing the coordinates
	#info = data.split('\r\n\r\n', 1)[0]				#prints the http 1.1 and headers
	#print (info)
	x = 0
	y = 0
	opponentHIT = 0
	c = 0
	if (coordinates ==''):
		print ("No data to Process")
		c = 404
	else:
		coordinates = coordinates.split('&')			#split data into two fields use & to split
		xFieldandValue = coordinates[0]
		yFieldandValue = coordinates[1]
		xFieldandValue= xFieldandValue.split('=')
		yFieldandValue = yFieldandValue.split('=')
		x = int(xFieldandValue[1])
		y = int(yFieldandValue[1])
		print ("Shot Cordinates:\n  x: " + str(x) + "   y: " + str(y))

		c = 200
	return x,y, opponentHIT, c										#returns the POST Fire coordinats as ints

if __name__=="__main__":
	port = int(sys.argv[1])								#grabs the port
	board = sys.argv[2]									#grabs the board file name
	with open(board, "r")as file:						#open file
		tempBoard = []
		for line in file:								#read file store in char array
			tempBoard.append(line.rstrip(' \n'))

	server(port, tempBoard, sys.argv[2])								#pass through Port and char array (game board)
