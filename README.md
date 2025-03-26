## network_oblig2

Included in this folder are three python scripts. Two that run a webserver and one that runs a client

# webserver.py

Runs a webserver that can handle one connection at a time. It will answer to HTTP GET request messages by returning requested file. The only HTML document it can return is index.html. If requested file does not exist, an HTTP 404 Not Found response message will be sent.

webserver.py requires no arguments and can be run like this:

    ```sh
    python3 webserver.py
    ```

# multithreading-webserver.py

Does the exact same thing as webserver.py, but can handle multiple connections at a time.

multithreading-webserver.py requires no arguments and can be run like this:

    ```sh
    python3 multithreading-webserver.py
    ```

# client.py

Runs a client that sends an HTTP GET request message for a file and waits for an HTTP response message. The HTTP response message is printet to console.

Takes in three arguments, two of which are required:
* -i or --ip asks for ip-address of server you want to connect to. Is required
* -p or --port asks for port number of server socket you want to connect to. Is required
* -f or --file asks for name of file you want to request. Is not required and client.py will ask for index.html by default

client.py can be run like this:

    ```sh
    python3 client.py -i <server_ip> -p <server_port> [-f FILENAME]
    ```