# CSC 591/791, ECE592/792
Spring 2022
## Homework Assignment # 2

### Objectives
To help you see the differences in the performance achieved by MQTT, COAP, and HTTP

### Description
For this assignment, you will need up to three computers (which could be laptops, smart phones, Raspberry Pis etc, any computing devices you choose), each with a WiFi interface, all connected to the same local area network. You can also run three virtual machines on a single physical computer using a software such as VMWare or VirtualBox.

Please find attached four files of sizes:
1. About 100 bytes
2. About 10kB
3. About 1MB
4. About 10MB

In this assignment, you will simply transfer files from one computing device to another using
1. MQTT QoS 1
2. MQTT QoS 2
3. CoAP using confirmable messages and block transfer
4. HTTP

For MQTT QoS 1 and MQTT QoS 2, you will set up a broker on one computer, a publisher on the second computer, and a subscriber on the third. The publisher will contain these files on its file system, and publish them on a topic at the broker. The subscriber will subscribe to that topic and receive them as soon as the publisher publishes them to the broker.
For CoAP, you will set up one computer as CoAP server and the other as CoAP client. The CoAP server will contain these files on its file system and the CoAP client will request them from the server.
For HTTP, you will set up one computer as HTTP server and the other as HTTP client. The HTTP server will contain these files on its file system and the HTTP client will request them from the server.
For each of the four protocol choices, conduct following experiments.

2. Transfer the 100 B file from source (the publisher in the case of MQTT and the server in the case of CoAP and HTTP) to destination 10 thousand times
2. Transfer the 10kB file from source to destination 1 thousand times
3. Transfer the 1MB file from source to destination 100 times
4. Transfer the 10MB file from source to destination 10 times

During each experiment (i.e., every transfer of each file), record the time (programmatically, not by hand) the file transfer takes, divide the file size by this time, and record the result. After completing all 11110 experiments and recording the results, fill out the table in the attached excel file named “Results File.xlsx”. Note that this table also asks you to report the total application layer data transferred from sender to receiver (including header content) per file divided by the file size. This will enable you to measure the overhead of each of these protocols (only from sender to receiver; we are not measuring the packets arriving from receiver to sender for things such as ACKs as overhead).

### What to submit
Please make only 1 submission per group as assigned by the instructor, i.e., only one student in the group should submit. In a single .zip file, upload the following to Moodle
1. Code for all three computers for each experiment and readme files explaining how to execute the codes
2. Completed “Results File.xlsx”
3. A report containing the following

a) On the first page

i.  Names of each team member and percentage contribution of each team member. Please be fair and truthful. The grade of this assignment will be divided among team members according to their percentage contributions. </li>

ii. What exactly did each team member do. Make a table. Assuming you have 5 members in your team, make a table with 6 columns. The first column should state various subtasks that your team undertook for this assignment and the next four columns should state the percentage contribution of the four team members for each subtask.

b) On page 2 and onward, describe your observations from the experiments and from the completed table in “Results File.xlsx”. Discuss which protocols perform better in what scenarios, investigate and describe why, and provide convincing arguments to justify your observations. This description should be no more than three pages long (double column, 10 pt font, 1 inch margins on all four sides of each page)
