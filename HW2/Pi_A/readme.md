## README for Pi-A

### Implementation

For our implementation, we choose to use an Ardunio to act as our ADC. The Raspberry Pi does not have one built-in
natively, so we are using what we have on hand. This did however create its own problems. The Arduino must communicate
with the Pi over serial communcation. The aruino is alwayspulling from the sensors and writing the data in a comma
seperated format to the Serial. The Pi can connect to the serial com and read the data that is being stream. The data is
confined to a range of 0 to 255 from the Ardunio.The Pi will apply a threshold of 3 to the values being read. We found
that this value removed any flickering values from the raw data, so that it only publishes when there is a real change.
The Arduino source is located in the Pi_A_Arduino_Code.ino and the wiring depicts how the Arduino is wired.

### Usage

Before anything else, the Arduino must be wired correctly and have a USB connecting it the Raspberry Pi. Next, the user
must upload the Arduino code through the Arduino IDE.

In order to start the Pi_A client, the user must enter the following command in the terminal in the directory that the
file is located:

`python3 Pi_A_Client.py`

The user will be prompted for the serial port of the Arduino. Enter the a value for the corrosponding port and press *
*ENTER**. If no port is found or an invalid selection is entered, the program will exit. Example:

```
Starting the Pi A client...
Available serial ports:
1: COM4
Select a serial port: 1
```

After the serial port, the user will be prompted for IP address of the broker. Enter the IP and press **ENTER**. If the
client is unable to connect to the broker, an error will occur and the program will exit. Example:

`Enter Broker IP Address: 192.168.10.4`

The following should be displayed if everything worked correctly:

```
Connected to Broker
Connection returned result: 0
Press 'Enter' to exit:
```

Press **ENTER** to exit gracefully.
