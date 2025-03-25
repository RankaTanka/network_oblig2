
from socket import *    # imported so I can program with sockets
import argparse         # imported so arguments can be parsed
import sys              # imported so program can be terminated



def main():

    try:

        identifier, port, file = argumentParser()

        httpResponseMessage = connectionHandler(identifier, port, file)
        print(f'HTTP response message received:\n' \
              f'{httpResponseMessage}')

        sys.exit()


    except Exception as error:

        # Error and status message for console
        print(f'An error has occured: {error}\n' \
              'exiting program...')          
        # Terminates program
        sys.exit()

# End of main()    


def argumentParser():
    parser = argparse.ArgumentParser(description = 'Attempts to connect to a server and send HTTP GET request for file')

    parser.add_argument('-i', '--identifier', type = str, nargs = 1, required = True,
                            help = 'Server identifier: IP adress or name of server')
    parser.add_argument('-p', '--port', type = int, nargs = 1, required = True,
                            help = 'Socket port number: Port number attatched to server socket')
    parser.add_argument('-f', '--file', type = str, nargs = '?',
                            help = 'Requested file: File asked for in HTTP GET request')
        
    arguments = parser.parse_args()

    identifier = arguments.identifier[0]
    port = arguments.port[0]
    if not arguments.file:
        file = ''
    else:
        file = arguments.file[0]

    return identifier, port, file

# End of argumentParser()



def connectionHandler(serverIP, serverPort, requestFile):

    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        
        clientSocket.connect((serverIP, serverPort))
        print('Connection established, ready to send...')

        httpRequestMessage = httpGETWriter(serverIP, serverPort, requestFile)
        
        print('Sending HTTP request message to server...')
        clientSocket.send(httpRequestMessage.encode())

        httpResponseMessage = clientSocket.recv(1024).decode()
        print('Response message received, closing connection...')
        clientSocket.close()

        return httpResponseMessage
    

    except Exception as error:

        # Error and status message for console
        print(f'An error has occured: {error}\n' \
              'exiting program...')          
        # Closes connection and terminates program
        clientSocket.close()
        sys.exit()

# End of connectionHandler



def  httpGETWriter(serverIP, serverPort, requestFile): 
    
    if requestFile != '' and requestFile[0] == '/': requestFile = requestFile[1:]
    httpRequestMessage = f'GET /{requestFile} HTTP/1.1\r\n' \
                         f'Host: {serverIP}:{serverPort}\r\n' \
                         'Connection: close\r\n' \
                         '\r\n'
    
    return httpRequestMessage

# End of httpGETWriter



if __name__ == "__main__":  # runs the main method
    main()
