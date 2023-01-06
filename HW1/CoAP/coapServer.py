'''
Author: Rishi Patel

I used this as a resource. https://aiocoap.readthedocs.io/en/latest/examples.html 

I was able to transfer the raw data. We dont need to make a file on the client side so this should do.

Just need to add loops and extend functionality for other file sizes.


run the server file in cmd and client in IDE

'''
import aiocoap
import aiocoap.resource as resource
import asyncio
import logging


# class to transfer data 
class dataFile_100B(resource.Resource):

    # Open file, read into a variable and send as payload
    async def render_get(self, request):
        f = open('../DataFiles/100B', 'rb')
        filestring = f.read()

        return aiocoap.Message(payload=filestring)


class dataFile_10KB(resource.Resource):

    # Open file, read into a variable and send as payload
    async def render_get(self, request):
        f = open('../DataFiles/10KB', 'rb')
        filestring = f.read()

        return aiocoap.Message(payload=filestring)


class dataFile_1MB(resource.Resource):

    # Open file, read into a variable and send as payload
    async def render_get(self, request):
        f = open('../DataFiles/1MB', 'rb')
        filestring = f.read()

        return aiocoap.Message(payload=filestring)


class dataFile_10MB(resource.Resource):

    # Open file, read into a variable and send as payload
    async def render_get(self, request):
        f = open('../DataFiles/10MB', 'rb')
        filestring = f.read()

        return aiocoap.Message(payload=filestring)


# logging setup
logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)


async def main():
    # Resource tree creation
    root = resource.Site()
    # add resource for 100B
    root.add_resource(['datafile', '100B'], dataFile_100B())
    root.add_resource(['datafile', '10KB'], dataFile_10KB())
    root.add_resource(['datafile', '1MB'], dataFile_1MB())
    root.add_resource(['datafile', '10MB'], dataFile_10MB())

    await aiocoap.Context.create_server_context(root, bind=("192.168.10.2", 5683))

    # Run forever
    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())
