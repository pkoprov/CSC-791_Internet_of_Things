import requests
import numpy as np
import time

serverAddress = "http://192.168.10.31:8000"
files_size = ["/100B", "/10KB", "/1MB", "/10MB"]
files_size_int = [100, 10000, 1000000, 10000000]


def make_request(file_size_index, file_count):
    recorded_time = []
    print("\n===============================================================\n")
    print("Address: \t\t", serverAddress, files_size[file_size_index])
    print("File Count: \t\t", file_count)
    for i in range(file_count):
        start_time = time.time()
        r = requests.get(serverAddress + files_size[file_size_index])
        recorded_time.append(time.time() - start_time)

    # print the total time
    print("Total Time: \t\t", sum(recorded_time), " Seconds")
    # Print the average time
    print("Average time: \t\t", np.mean(recorded_time), " Seconds")
    # Print the standard deviation
    print("Standard deviation: \t", np.std(recorded_time), " Seconds")
    # Calculate the kilobits per second for each file
    # and save it to a list
    kbps = []
    for i in range(len(recorded_time)):
        kbps.append((files_size_int[file_size_index] * 8 / recorded_time[i]) / 1000)
    # Print the average kbps
    print("Average kbps: \t\t", np.mean(kbps), " kbps")
    # Print the standard deviation
    print("Standard deviation: \t", np.std(kbps), " kbps")
    print("\n===============================================================\n")

while True:

    print("Which size of file do you want to trasfer? \n 0. 100 bytes \n 1. 10KB \n 2. 1MB \n 3. 10MB \n 4. Exit")

    choice = int(input('Enter Number: '))

    if choice == 0:
        fileSize = "100B"
        transferNumber = 10000
    elif choice == 1:
        fileSize = "10KB"
        transferNumber = 1000
    elif choice == 2:
        fileSize = "1MB"
        transferNumber = 100
    elif choice == 3:
        fileSize = "10MB"
        transferNumber = 10
    elif choice == 4:
        print("Exiting..!")
        break
    else:
        print("Enter valid choice")
        break
    make_request(choice, transferNumber)


