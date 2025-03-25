
from socket import *    # imported so I can program with sockets
import sys              # imported so program can be terminated



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
    # Status message for console 
    print(f'Server is ready to receive on server port {serverPort}...')


    # Runs connectionHandler() function with serverSocket as parameter
    connectionHandler(serverSocket) 


    # Connection is finished
    # Status message for console 
    print(f'Closing server socket on port {serverPort}...')
    # Closes serverSocket and terminates this program
    serverSocket.close()
    sys.exit()

# End of main()



def connectionHandler(serverSocket):

    """
        Description:
        function that handles connections. 
        Runs an infinite while loop that receives HTTP requests from- and sends HTTP response messages to client
        
        In case of error, function is stopped and an appropriate HTTP response message sent to client

        If index.html is requested, said file is sent in an HTTP response message with "200 OK" as status
        If unknown file is requested, an HTTP response message with "404 Not Found" as status is sent
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
            # Status message for console
            print(f'Connection established with {clientAddress[0]} on client port {clientAddress[1]}')

            # Waits for client to send HTTP GET request
            httpRequestMessage = connectionSocket.recv(1024).decode()
            # Status message for console
            print("Message received")
            
            # Handles connectionSocket.recv() returning blank String
            if not httpRequestMessage:

                # Status message for console
                print("Received empty message, closing connection...")
                # Closes connection and goes to next iteration of loop
                connectionSocket.close()
                continue
            
            
            # Attempts to retreive data requested file, 
            # then write HTTP response message with status of 200 OK
            data = httpGETRetreiver(httpRequestMessage)             # data from requested file
            status = "200 OK"                                       # HTTP status
            httpResponseMessage = httpResponseWriter(status, data)  # HTTP response message


            # Sends HTTP response to client
            connectionSocket.send(httpResponseMessage.encode())

            # Status message for console
            print('Requested file sent, closing connection...')
            # Closes connectionSocket so that files can be requested from other client ports or even IP's
            connectionSocket.close()



        # Handles exception if other file than index.html is being requested
        # Sends HTTP response with "404 Not Found" as status to client
        except FileNotFoundError:

            # writes HTTP response message with "404 Not Found" as status
            status = '404 Not Found'                                # HTTP status
            data = '<h1>File not found<h1>'                         # Very simple HTML data
            httpResponseMessage = httpResponseWriter(status, data)  # HTTP response message
            

            # Sends HTTP response to client
            connectionSocket.send(httpResponseMessage.encode())

            # Status message for console
            print('Requested file not found, closing connection...')
            # Closes connection and breaks the infinite loop
            connectionSocket.close()
            break

        

        # Handles any other exception
        # Sends HTTP response with "500 Internal Server" as status to client
        except Exception as error:

            # writes HTTP response message with "500 Internal Server Error" as status
            status = '500 Internal Server Error'                    # HTTP status
            data = '<h1>Oh no<h1>'                                  # very simple HTML data 
            httpResponseMessage = httpResponseWriter(status, data)  # HTTP response message
            

            # Sends HTTP response to client
            connectionSocket.send(httpResponseMessage.encode())

            # Error and status message for console
            print(f'An error has occured: {error}\n' \
                  'closing connection...')          
            # Closes connection and breaks the infinite loop
            connectionSocket.close()
            break

# End of connectionHandler



def httpGETRetreiver(httpRequestMessage):

    """
        Description:
        Handles HTTP GET requests by retreiving data from requested file.
        File must exist for function to work

        Argument:
        httpRequestMessage: An HTTP GET request message asking for specific file

        Returns:
        data: Data from requested file in the form of a string    
    """


    # received HTTP GET request should be formatted like this: "GET /file ..."
    # Word on index 1 of request String should therefore be the requested file
    requestedFilename = httpRequestMessage.split()[1]

    # if-statement that retreives data from requested file
    if requestedFilename == '/':    # "/" is a request for index.html

        # opens index.html and reads its contents to variable, data
        with open('index.html') as requestedFile:
            data = requestedFile.read()

    else:   # handles requests for explicit file

        # requestedFilename should start with "/", 
        # therefore characters from index 1 and onwards should be requested file
        # Opens file and attempts to read its contents to variable, data
        with open(requestedFilename[1:]) as requestedFile:
            data = requestedFile.read()
    
    return data

# End of dataRetreival



def httpResponseWriter(status, data):

    """
        Description:
        Writes HTTP response message with provided status and data.
        Inclueded fields in HTTP response message are: Content-Length, Connection and Content-Type

        Arguments:
        status: Contains status code and phrase for the HTTP response message
        data: HTTP response message's attached data
        
        Returns:
        httpResponseMessage: Fully written HTTP response message in the form of a string    
    """


    # Writes the HTTP response message
    httpResponseMessage = f'HTTP/1.1 {status}\r\n' \
                          f'Content-Length: {len(data)}\r\n' \
                          'Connection: close\r\n' \
                          'Content-Type: text/html; charset=UTF-8\r\n' \
                          '\r\n' \
                          f'{data}'
    
    return httpResponseMessage

# End of httpResponseWriter



if __name__ == '__main__':  # runs the main method
    main()
