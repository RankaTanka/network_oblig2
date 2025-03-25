
from socket import *    # imported for socket programming


# Beginning of main()

def main():

    """
        Description:
        The main method. It runs serverHandler() function with self defined arguments 
    """
  

    # Runs serverHandler with defined port number and IP address
    serverIP = '127.0.0.1'
    serverPort = 6969
    serverHandler(serverIP, serverPort)

# End of main()



# Beginning of serverHandler()

def serverHandler(serverIP, serverPort):

    """
        Description:
        Creates a server socket and binds it to provided arguments 
        Server socket can handle one connection at a time
        Runs an infinite loop so other clients can connect if a client disconnects
        
        Infinite loop be interrupted by user or raised IOError, 
        in which case, all sockets will close and function will end

        Arguments:
        serverIP:   identifier of server
        serverPort: port number to be attached to server socket
    """


    # Creates a TCP socket with IPv4 as underlying network
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Binds serverSocket to given port number and IP address
    serverSocket.bind((serverIP, serverPort))

    # ServerSocket will only handle one connection at a time
    serverSocket.listen(1)
    # Status message for console 
    print(f'Server is ready to receive on port {serverPort}...')


    # Will attempt to establish connection with client
    try:

        # Infinite loop so other clients can connect if client disconnects
        while True:    
            # Accepts connection from a client by creating a socket for this connection
            # Also saves client IP and port number
            connectionSocket, clientAddress = serverSocket.accept()
            # Status message for console
            print(f'Connection established with {clientAddress[0]} on client port {clientAddress[1]}')


            # Runs connectionHandler() function with serverSocket as parameter
            connectionHandler(connectionSocket) 


    # In case of user interrupting server, infinite loop is exited
    except KeyboardInterrupt:
        # Status message for console
        print('Received order to close server')


    # In case of IOError being raised, infinite loop is exited
    except IOError:
        # Status message for console
        print('Internal error, closing server')


    # Always executed after infinite loop is exited
    finally:
        # Status message for console 
        print(f'Closing server socket on port {serverPort}...')
        # Closes connectionSocket and serverSocket
        connectionSocket.close()
        serverSocket.close()

# End of serverHandler()



# Beginning of connectionHandler()

def connectionHandler(connectionSocket):

    """
        Description:
        function that handles connections. 
        Runs an infinite while loop that receives HTTP requests from- and sends HTTP response messages to client
        
        In case of error, an appropriate HTTP response message sent to client
        All errors except for FileNotFoundError will raise IOError for serverHandler() to catch

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

            # Waits for client to send HTTP GET request
            httpRequestMessage = connectionSocket.recv(1024).decode()
            
            # Handles connectionSocket.recv() returning blank
            if not httpRequestMessage:

                # Status message for console
                print("Client has closed connection, closing connection socket...")
                # Closes connection and breaks the infinite loop
                connectionSocket.close()
                break
            
            # Status message for console
            print("Message received")
            
            # Attempts to retreive data requested file, 
            # then write HTTP response message with status of 200 OK
            data = httpGETData(httpRequestMessage)                              # Data from requested file
            connection = httpConnectionStatus(httpRequestMessage)               # Connection status from HTTP request message
            status = "200 OK"                                                   # HTTP status
            httpResponseMessage = httpResponseWriter(status, connection, data)  # HTTP response message


            # Sends HTTP response to client
            connectionSocket.send(httpResponseMessage.encode())
            # Status message for console
            print('Requested file sent')


        # Handles exception if other file than index.html is being requested
        # Sends HTTP response with "404 Not Found" as status to client
        except FileNotFoundError:

            # writes HTTP response message with "404 Not Found" as status
            status = '404 Not Found'                                            # HTTP status
            connection = httpConnectionStatus(httpRequestMessage)               # Connection status from HTTP request message
            data = '<h1>File not found<h1>'                                     # Very simple HTML data
            httpResponseMessage = httpResponseWriter(status, connection, data)  # HTTP response message
            

            # Sends HTTP response to client
            connectionSocket.send(httpResponseMessage.encode())
            # Status message for console
            print('Requested file not found, appropriate response message sent')

        
        # Handles any other exception
        # Sends HTTP response with "500 Internal Server" as status to client and closes connection
        except Exception as error:

            # writes HTTP response message with "500 Internal Server Error" as status
            status = '500 Internal Server Error'                                # HTTP status
            connection = 'close'                                                # Close the connection
            data = '<h1>Oh no<h1>'                                              # very simple HTML data 
            httpResponseMessage = httpResponseWriter(status, connection, data)  # HTTP response message
            

            # Sends HTTP response to client
            connectionSocket.send(httpResponseMessage.encode())

            # Error and status message for console
            print(f'An error has occured: {error}\n' \
                  'appropriate response message sent, closing connection socket...')          
            # Closes connection and breaks the infinite loop
            connectionSocket.close()
            raise IOError()

# End of connectionHandler()



# Beginning of httpGETData()

def httpGETData(httpRequestMessage):

    """
        Description:
        Retrieves data from file requested by HTTP GET request message.
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

# End of httpGETData()



# Beginning of httpConnectionStatus()

def httpConnectionStatus(httpRequestMessage):

    """
        Description:
        Sets connection status based on provided HTTP request message's connection status

        Argument:
        httpRequestMessage: An HTTP request message

        Returns:
        connectionStatus: Connection status indicated in HTTP request message
                          Set to 'close' if "Connection" field is not in HTTP request message 
    """

    
    # connectionStatus, set to 'close' by default
    connectionStatus = 'close'
    
    # splits httpRequestMessage with '\r\n' as seperator, 
    # this will generate an array containing each field in HTTP request message
    requestMessageFields = httpRequestMessage.split('\r\n')

    # For loop that iterates through all fields in httpRequestMessage
    for field in requestMessageFields:
        
        # Looks for "Connection" field, by matching start of string with 'Connection:'
        if field.startswith('Connection:'):
            # Character 12 and onwards in "Connection" field contains connection status
            connectionStatus = field[12:]
            # Preemtively breaks for loop
            break
    
    return connectionStatus

# End of httpConnectionStatus



# Beginning of httpResponseWriter()

def httpResponseWriter(status, connection, data):

    """
        Description:
        Writes HTTP response message with provided status and data.
        Inclueded fields in HTTP response message are: Content-Length, Connection and Content-Type

        Arguments:
        status:     Contains status code and phrase for the HTTP response message
        data:       HTTP response message's attached data
        connection: Decides if client stays connected, is either "keep-alive" or "close"
        
        Returns:
        httpResponseMessage: Fully written HTTP response message in the form of a string    
    """


    # Writes the HTTP response message
    httpResponseMessage = f'HTTP/1.1 {status}\r\n' \
                          f'Content-Length: {len(data)}\r\n' \
                          f'Connection: {connection}\r\n' \
                          'Content-Type: text/html; charset=UTF-8\r\n' \
                          '\r\n' \
                          f'{data}'
    
    return httpResponseMessage

# End of httpResponseWriter()



if __name__ == '__main__':  # runs the main method
    main()
