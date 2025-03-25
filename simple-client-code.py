
from socket import *    # imported so I can program with sockets
import sys              # imported so program can be terminated



def main():
    print(f'{connectionHandler('127.0.0.1', 6969, '/index.html')}\n')
    print(f'{connectionHandler('127.0.0.1', 6969, '')}\n')
    print(f'{connectionHandler('127.0.0.1', 6969, '/html.index')}\n')

# End of main()    



def connectionHandler(serverIP, serverPort, requestFile):

    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)

        clientSocket.connect((serverIP, serverPort))
        print('Connection established, ready to send...')

        httpRequestMessage = httpGETWriter(serverIP, serverPort, requestFile)
        
        print('Sending HTTP request to server...')
        clientSocket.send(httpRequestMessage.encode())

        httpResponseMessage = clientSocket.recv(1024).decode()
        print('Response message received, closing connection...')
        clientSocket.close()

        return httpResponseMessage
    
    except Exception as error:
        # Error and status message for console
        print(f'An error has occured: {error}\n' \
              'closing connection...')          
        # Closes connection
        clientSocket.close()

# End of connectionHandler



def  httpGETWriter(serverIP, serverPort, requestFile): 

    if requestFile == '': requestFile = '/'
    httpRequestMessage = f'GET {requestFile} HTTP/1.1\r\n' \
                             f'Host: {serverIP}:{serverPort}\r\n' \
                             'Connection: close\r\n' \
                             '\r\n'
    
    return httpRequestMessage

# End of httpGETWriter



if __name__ == "__main__":  # runs the main method
    main()
