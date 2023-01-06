import numpy as np
import pandas as pd

while True:
    print("Which size of file do you want to trasfer? \n 1. 100 bytes \n 2. 10KB \n 3. 1MB \n 4. 10MB \n 5. Exit")

    choice = int(input('Enter Number: '))

    if choice == 1:
        file = 100
        file_name = "100B"
        file_num = 10000
    elif choice == 2:
        file = 10 ** 4
        file_name = "10KB"
        file_num = 1000
    elif choice == 3:
        file_name = "1MB"
        file = 10 ** 6
        file_num = 100
    elif choice == 4:
        file_name = "10MB"
        file = 10 ** 7
        file_num = 10
    else:
        break

    pack_header = [[] for i in range(file_num)]

    df = pd.read_csv(f'Wireshark_coap_{file_name}.csv')
    data = df.loc[df["Destination"] == "192.168.10.31"]
    pack_size = np.unique(data["Length"])
    packet_len = np.array(data["Length"])
    packet_info = np.array(data["Info"])
    if choice == 1:
        header = [6, 7]
    elif choice == 2:
        header = [9, 10]
    elif choice == 3:
        header = [9, 10, 11]
    elif choice == 4:
        header = [11, 12, 9, 10, 11, 12]

    n = 0
    for i, packet in enumerate(packet_info):
        pack_header[n].append(header[np.where(packet_len[i] == pack_size)[0][0]])
        if "End" in packet:
            n += 1

    if choice == 1:
        avarage_header_size = np.mean(np.mean(pack_header[0]))
    else:
        avarage_header_size = np.mean(np.mean(pack_header, axis=1))

    print("\nAverage header size: ", avarage_header_size)
    print("\nTable Value:", (avarage_header_size + file) / file, "\n")
    print("===============================================================")
