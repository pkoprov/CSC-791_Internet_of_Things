# Authors: Chaitanya Pawar <cpawar@ncsu.edu> and Thomas Batchelder <tjbatche@ncsu.edu>
# Import the necessary libraries and serial communication
import glob
import paho.mqtt.client as mqtt
import serial
import sys
import threading
import time


def serial_ports():
    # Function for getting all serial ports open on a device
    # This function was written by tfeldmann on stackoverflow
    # Link: https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


class Pi_A_Client:
    def __init__(self, broker_ip, com_port):
        # Initialize the client
        self.broker_ip = broker_ip
        self.com_port = com_port

        # Try to open the serial port with the Ardunio
        try:
            self.ser = serial.Serial(self.com_port, 9600)
        except:
            print("\n --- ERROR ---")
            print("Serial port not found")
            print("Port: " + self.com_port)
            print("Please try another serial port")
            exit()

        # Connstruct the client
        self.client = mqtt.Client("RaspberryPiA")
        # Set LWT message to "Offline"
        self.client.will_set("Status/RaspberryPiA",
                             payload="Offline", qos=2, retain=True)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        try:
            self.client.connect(self.broker_ip, 1883, keepalive=1)
        except:
            print("\n --- ERROR ---")
            print("Unable to connect to Broker")
            print("Broker IP: " + broker_ip)
            print("Please try another address")
            print("Check that the Broker is online")
            exit()

        # Subscribe to the two topics
        self.client.subscribe("lightSensor", qos=2)
        self.client.subscribe("threshold", qos=2)
        self.client.loop_start()

        # Create variables for storing the read values
        self.lightStatus = 0
        self.threshold = 0
        self.previous_lightStatus = 0
        self.previous_threshold = 0
        self.continue_loop = True

    def on_connect(self, client, userdata, flags, rc):
        # Function run when the client connects to the broker
        print("Connected to Broker")
        self.client.publish("Status/RaspberryPiA",
                            payload="Online", qos=2, retain=True)
        print("Connection returned result:", rc)

    def on_disconnect(self, client, userdata, rc):
        # Function run when the client disconnects from the broker
        print("Disconnected from Broker")

    def on_message(self, client, userdata, message):
        # Function run when the client receives a message
        msg = int(message.payload.decode())

        if message.topic == "lightSensor":
            self.previous_lightStatus = int(msg)
        elif message.topic == 'threshold':
            self.previous_threshold = int(msg)

        # print(message.topic, msg)

    def shutdown(self):
        # This function shuts down the client
        # and disconnects all the devices
        # This is meant as a gracefullt disconnect
        self.continue_loop = False
        self.client.publish("Status/RaspberryPiA",
                            payload="Offline", qos=2, retain=True)
        time.sleep(0.1)
        self.client.loop_stop()
        self.client.disconnect()
        self.ser.close()

    def update(self):
        # This function is meant to be run in a thread to
        # read the serial port and send the data to the broker
        while True:
            # Read the serial port
            # Data format is:
            # threshold, lightStatus
            # Check if the serial port is open
            if self.ser.isOpen():
                try:
                    # Read the serial port
                    read_data = self.ser.readline().decode('utf-8')
                    # Split the data into two parts
                    data = read_data.split(",")
                    # Update the lightStatus and threshold and map the data to the correct range (0-255)
                    self.threshold = int(data[0])
                    self.lightStatus = int(data[1])
                except:
                    pass

            # publish the read values
            # threshold to avoid super frequent publishing. Just a way to overcome noise
            value_threshold = 3
            if self.threshold > value_threshold + self.previous_threshold or self.threshold < self.previous_threshold - value_threshold:
                self.client.publish(
                    "threshold", payload=self.threshold, qos=2, retain=True)
                self.previous_threshold = self.threshold
            if self.lightStatus > value_threshold + self.previous_lightStatus or self.lightStatus < self.previous_lightStatus - value_threshold:
                self.client.publish(
                    "lightSensor", payload=self.lightStatus, qos=2, retain=True)
                self.previous_lightStatus = self.lightStatus
            if not self.continue_loop:
                break


if __name__ == '__main__':
    print("Starting the Pi A client...")

    # Print available serial ports
    print("Available serial ports:")
    available_serial_ports = serial_ports()
    if len(available_serial_ports) == 0:
        print("No Serial devices connected")
        print("Please check that the Arduino is connected")
        exit()
    # Iterate through the available serial ports and print a number and the port name
    for i in range(len(available_serial_ports)):
        print(str(i + 1) + ": " + available_serial_ports[i])
    # Ask the user to select a serial port
    user_input = input("Select a serial port: ")
    # Check if the user input is valid
    if int(user_input) > len(available_serial_ports) or int(user_input) < 1:
        print("Invalid selection")
        exit()
    # Get the selected serial port
    selected_serial_port = available_serial_ports[int(user_input) - 1]
    # Ask for the broker IP address
    broker_ip = input("Enter Broker IP Address: ")
    pi = Pi_A_Client(broker_ip, selected_serial_port)
    # Call pi.update() on a separate thread
    threading.Thread(target=pi.update, daemon=True).start()
    # Ask the user if they want to exit
    input("Press 'Enter' to exit: ")
    pi.shutdown()
