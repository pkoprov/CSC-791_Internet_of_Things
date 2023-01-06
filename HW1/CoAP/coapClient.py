import asyncio
import logging
from aiocoap import *
from time import *

logging.basicConfig(level=logging.INFO)


async def fileTransfer(fileSize):
    protocol = await Context.create_client_context()

    start_req = time_ns()
    request = Message(code=GET, uri=f'coap://localhost/datafile/{fileSize}')

    try:
        response = await protocol.request(request).response
        end_req = time_ns()

    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
        return -1
    else:
        print('Message Rec!!', " ...... \n Length of message recv: ", len(response.payload))
        return (end_req - start_req) / 1000000


if __name__ == "__main__":

    while True:

        print("Which size of file do you want to trasfer? \n 1. 100 bytes \n 2. 10KB \n 3. 1MB \n 4. 10MB \n 5. Exit")

        choice = int(input('Enter Number: '))

        if choice == 1:
            fileSize = "100B"
            transferNumber = 10000
        elif choice == 2:
            fileSize = "10KB"
            transferNumber = 1000
        elif choice == 3:
            fileSize = "1MB"
            transferNumber = 100
        elif choice == 4:
            fileSize = "10MB"
            transferNumber = 10
        elif choice == 5:
            print("Exiting..!")
            break
        else:
            print("Enter valid choice")
            break
        time = []

        for i in range(5):
            transfer_time = asyncio.get_event_loop().run_until_complete(fileTransfer(fileSize))
            time.append(transfer_time)

        print(f"Transfer time for {fileSize}: ", time)
