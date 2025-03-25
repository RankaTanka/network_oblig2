
from socket import *    # imported so I can program with sockets
import argparse         # imported so arguments can be parsed
import sys              # imported so program can be terminated



def main():

    """
        Description:
        The main method. It retreives arguments using argumentParser() function
        and then prints HTTP response message from httpMessageHandler() function.

        In case of error, program is terminated 
    """


    try:

        # Saves arguments using argumentParser() function
        identifier, port, file = argumentParser()

        # Saves an HTTP response message from httpMessageHandler()
        httpResponseMessage = httpMessageHandler(identifier, port, file)
        # Prints HTTP response message to console
        print(f'HTTP response message received:\n' \
              f'{httpResponseMessage}')

        # Terminates program
        sys.exit()


    # Handles exceptions
    # Prints error message to console and terminates program
    except Exception as error:

        # Error and status message for console
        print(f'An error has occured: {error}\n' \
              'exiting program...')  
        # Terminates program        
        sys.exit()

# End of main()    



def argumentParser():

    """
        Description:
        Creates an argument parser and retreives provided arguments from it

        Returns:
        identifier: Identifier for server user wants to connect to, an IP address or servername
        port:       Port number attached to server socket user wants to connect to
        file:       File user wants to retreive from server
    """

    # An argument parser with appropriate description
    parser = argparse.ArgumentParser(description = 'Attempts to connect to a server and send HTTP GET request for file')
    
    # Argument for identifier. Type is string and only 1 argument is allowed. Is required
    parser.add_argument('-i', '--identifier', type = str, nargs = 1, required = True,
                        help = 'Server identifier: IP adress or name of server')
    # Argument for port. Type is int and only 1 argument is allowed. Is required
    parser.add_argument('-p', '--port', type = int, nargs = 1, required = True,
                        help = 'Socket port number: Port number attatched to server socket')
    # Argument for file. Type is string and 0-1 arguments are allowed. Is not required
    # The reason this is not required and 0 arguments are allowed is so index.html can be asked for by default
    parser.add_argument('-f', '--file', type = str, nargs = '?',
                        help = 'Requested file: File asked for in HTTP GET request')
        
    # Parses arguments
    arguments = parser.parse_args()


    identifier = arguments.identifier[0]    # Retreives identifier argument
    port = arguments.port[0]                # Retreives port argument
    if not arguments.file:                  # if argument.file is empty, file is set to ''
        file = ''
    else:                                   # if argument.file is not empty, file argument is retreived
        file = arguments.file[0]

    return identifier, port, file

# End of argumentParser()



def httpMessageHandler(serverIP, serverPort, requestFile):

    """
        Description:
        Connects to webserver using an identifier and a port number
        Sends HTTP GET request message to server, requesting a wanted file
        Receives an HTTP response message from server and closes connection

        In case of error, connection is closed and program is terminated

        Arguments:
        serverIP:    identifier of server, user wants to connect to
        serverPort:  port number attached to server socket, user wants to connect to
        requestFile: file requested from server in HTTP GET request message

        Returns:
        httpResponseMessage: HTTP response message received from server
    """


    # Attempts to connect to server, send and receive HTTP message
    try:
        
        # Creates a TCP socket with IPv4 as underlying network
        clientSocket = socket(AF_INET, SOCK_STREAM)
        
        # Connects to server from clientSocket
        clientSocket.connect((serverIP, serverPort))
        # Status message for console 
        print('Connection established, ready to send...')

        
        # HTTP GET request message
        httpRequestMessage = httpGETWriter(serverIP, serverPort, requestFile)
        

        # Status message for console 
        print('Sending HTTP request message to server...')
        # Sends HTTP GET request message through clientSocket to server
        clientSocket.send(httpRequestMessage.encode())


        # Waits for server to send HTTP response message through clientSocket
        httpResponseMessage = clientSocket.recv(1024).decode()
        
        # Status message for console 
        print('Response message received, closing connection...')
        # Closes clientSocket
        clientSocket.close()

        return httpResponseMessage
    

    # Handles exceptions
    # Prints error message to console, closes socket and terminates program
    except Exception as error:

        # Error and status message for console
        print(f'An error has occured: {error}\n' \
              'exiting program...')          
        # Closes connection and terminates program
        clientSocket.close()
        sys.exit()

# End of connectionHandler



def  httpGETWriter(serverIP, serverPort, requestFile): 

    """
        Description:
        Writes HTTP response message with provided serverIP, serverPort and requestFile.
        Inclueded fields in HTTP GET request message are: Host and Connection

        Returns:
        httpRequestMessage: Fully written HTTP GET request message in the form of a string
    """

    # If requestFile starts with "/" it is removed
    if requestFile != '' and requestFile[0] == '/': requestFile = requestFile[1:]
    # Writes the HTTP GET request message
    httpRequestMessage = f'GET /{requestFile} HTTP/1.1\r\n' \
                         f'Host: {serverIP}:{serverPort}\r\n' \
                         'Connection: close\r\n' \
                         '\r\n'
    
    return httpRequestMessage

# End of httpGETWriter



if __name__ == "__main__":  # runs the main method
    main()
