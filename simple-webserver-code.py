
import sys
from socket import *


def main():

    """
        Description:
        The main method. It creates and initializes a socket that will listen to one connection.
        Closes the socket when connectionHandler() function is finished 
    
    """


    # Creates a TCP socket with IPv4 as underlying network
    serverSocket = socket(AF_INET, SOCK_STREAM)  

    # Binds serverSocket to given port number and IP address
    serverPort = 6969
    serverIP = '127.0.0.1'
    serverSocket.bind((serverIP, serverPort))

    # ServerSocket will only handle one connection at a time
    serverSocket.listen(1)
    # Prints a server status message to console 
    print(f'Server is ready to receive on server port {serverPort}...')


    # Runs connectionHandler() function with serverSocket as parameter
    connectionHandler(serverSocket) 


    # Connection is finished
    # Closes serverSocket and terminates this program
    serverSocket.close()
    sys.exit()


def connectionHandler(serverSocket):

    """
        Description:
        function that handles connections. 
        Runs an infinite while loop that sends HTTP response messages from HTTP GET requests

        If index.html is requested, said file is sent in an HTTP response message with "200 OK" as status
        If other file than index.html is requested, an HTTP response message with "404 Not Found" as status is sent
        If an exception occurs, an HTTP response message with "500 Internal Server Error" as status is sent

        Argument:
        serverSocket: A TCP socket with IPv4 as underlying network that can listen to one connection at a time
    
    """


    while True:     # Infinite loop to ensure index.html can be requested several times
        
        # Responds to HTTP GET requests if possible. Can only respond to requests for index.html, 
        # Sends HTTP response with "200 OK" as status and index.html as data to client
        try: 

            # Accepts connection from a client by creating a socket for this connection
            # Also saves client IP and port number
            connectionSocket, clientAddress = serverSocket.accept()
            # Prints status message to console
            print(f'Connection established with {clientAddress[0]} on client port {clientAddress[1]}')

            # Waits for client to send HTTP GET request
            httpRequestMessage = connectionSocket.recv(1024).decode()
            
            # Handles connectionSocket.recv() returning blank String
            if not httpRequestMessage:

                # Prints status message to console
                print("Received empty message, reestablishing connection...")
                # Closes connection and goes to next iteration of loop
                connectionSocket.close()
                continue
            
            
            # received HTTP GET request should be formatted like this: "GET /file ..."
            # Word on index 1 of request String should therefore be the requested file
            requestedFilename = httpRequestMessage.split()[1]

            # if-statement that handles HTTP GET request for index.html
            if requestedFilename == '/':    # "/" is a request for index.html

                # opens index.html and reads its contents to variable, data
                with open('index.html') as requestedFile:
                    data = requestedFile.read()

            else:   # handles GET requests for explicit file, only works for index.html

                # requestedFilename should start with "/", 
                # therefore characters from index 1 and onwards should be requested file
                # Opens requested file and attempts to read its contents to variable, data
                with open(requestedFilename[1:]) as requestedFile:
                    data = requestedFile.read()


            # HTTP response, included fields are: Content-Length, Connection and Content-Type
            httpResponseMessage = 'HTTP/1.1 200 OK\r\n' \
                                  f'Content-Length: {len(data)}\r\n' \
                                  'Connection: close\r\n' \
                                  'Content-Type: text/html; charset=UTF-8\r\n' \
                                  '\r\n' \
                                  f'{data}'

            # Sends HTTP response to client
            connectionSocket.send(httpResponseMessage.encode())


            # Closes connectionSocket so that files can be requested from other client ports or even IP's
            connectionSocket.close()


        # Handles exception if other file than index.html is being requested
        # Sends HTTP response with "404 Not Found" as status to client
        except FileNotFoundError:

            data = '<h1>404 Not Found<h1>'  # very simple HTML data
            # HTTP response, included fields are: Content-Length, Connection and Content-Type
            httpResponseMessage = 'HTTP/1.1 404 Not Found\r\n' \
                                  f'Content-Length: {len(data)}\r\n' \
                                  'Connection: close\r\n' \
                                  'Content-Type: text/html\r\n' \
                                  '\r\n' \
                                  f'{data}'
            
            # Sends HTTP response to client
            connectionSocket.send(httpResponseMessage.encode())


            # Prints error and status message to console
            print('Requested file not found, closing connection...')
            # Closes connection and breaks the infinite loop
            connectionSocket.close()
            break

        
        # Handles any other exception
        # Sends HTTP response with "500 Internal Server" as status to client
        except Exception as error:

            data = '<h1>Oh no<h1>'  # very simple HTML data 
            # HTTP response, included fields are: Content-Length, Connection and Content-Type
            httpResponseMessage = 'HTTP/1.1 500 Internal Server Error\r\n' \
                                  f'Content-Length: {len(data)}\r\n' \
                                  'Connection: close\r\n' \
                                  'Content-Type: text/html\r\n' \
                                  '\r\n' \
                                  f'{data}'
            
            # Sends HTTP response to client
            connectionSocket.send(httpResponseMessage.encode())


            # Prints error and status message to console
            print(f'An error has occured: {error}\n' \
                  'closing connection...')          
            # Closes connection and breaks the infinite loop
            connectionSocket.close()
            break


    

if __name__ == '__main__':  # runs the main method
    main()
