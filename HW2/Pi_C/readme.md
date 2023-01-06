## README for Pi-C

### Usage

In order to start the Pi_B client, the user must enter the following command in the terminal in the directory that the
file is located:

`python3 Pi_C_Client.py`

The user will then be prompted for IP address of the broker. Enter the IP and press **ENTER**. If the client is unable
to connect to the broker, an error will occur and the program will exit. Example:

`Enter Broker IP Address: broker.hivemq.com`

The following should be displayed if everything worked correctly:

```
Starting the Pi C client...
Enter Broker IP Address: broker.hivemq.com
Connected to Broker
Press 'Enter' to exit:
```

Press **ENTER** to exit gracefully.
