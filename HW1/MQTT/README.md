## Instructions for Subscriber

Command-line: `python Subscriber.py`

The Subscriber should be run before the publisher. The 
Subscriber will ask for the IP of the Broker. Once the
subscriber has been started it will wait for messages from
the publisher. The publisher will specify how many files the
subscriber should expect to receive in addition to the QoS level.
Once the subscriber has received all the messages, it will
print of all information it recorded and reset
to reveive more messages.

## Instructions for Publisher

Command-line: `python Publisher.py`

Once the Publisher has been started, it will ask for the IP
address of the broker. After it connects to the broker, it
will request which file should be tested and then the 
QoS will also be asked for. It should look like the following:

```
Please enter the number of the data file you would like to publish:
1. 100B
2. 10KB
3. 1MB
4. 10MB
5. Stop
Enter your choice:
```

Once the you have selected from the options, the publisher will begin
publishing the file as quickly as possible. After it is done, it 
will restart and ask for the data file again. To stop, enter "5".

## File Structure

📦HW2\
 ┣ 📂DataFiles\
 ┃ ┣ 📜100B\
 ┃ ┣ 📜10KB\
 ┃ ┣ 📜10MB\
 ┃ ┗ 📜1MB\
 ┣ 📂MQTT\
 ┃ ┣ 📜Publisher.py\
 ┃ ┣ 📜README.md\
 ┃ ┗ 📜Subscriber.py

