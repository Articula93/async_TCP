import socket
import time
import asyncio
import random
import itertools
from concurrent.futures import ProcessPoolExecutor
import logging



logging.basicConfig(
    level=logging.INFO, 
    filename = f'mylog_server.log', 
    format='%(levelname)s (%(asctime)s): %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='a',
    encoding='utf-8'
    )
logging.info('This is a log message to client!')


all_client = []
request_number = itertools.count()


async def broadcast():
    loop = asyncio.get_event_loop()
    while True:
        for client in all_client:
            msg_all_client = f'[{next(request_number)}] keepalive'
            await loop.sock_sendall(client, msg_all_client.encode('utf8'))
            logging.info(msg_all_client)
        await asyncio.sleep(5)

async def handle_client(client, client_number):
    loop = asyncio.get_event_loop()
    while True:
        data = (await loop.sock_recv(client, 255)).decode('utf8')
        logging.info(data)
        number = data[1:data.find(']')]
        print(client_number, data, number)
        if random.randint(0,100)>10:
            msg = f'{next(request_number)}/{number} PONG {client_number}'
            logging.info(msg)
            await loop.sock_sendall(client, msg.encode('utf8'))
        else:
            ignor_msg = 'Проигнорированно'
            logging.info(ignor_msg)

async def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 14900))
    server.listen(2)
    server.setblocking(False)

    loop = asyncio.get_event_loop()
    client_number = 0
    while True:
        client, _ = await loop.sock_accept(server)
        all_client.append(client)
        loop.create_task(handle_client(client, client_number))
        client_number+=1



async def main():
    server = asyncio.create_task(run_server())
    msg_client = asyncio.create_task(broadcast())
    await server
    await msg_client

asyncio.run(main())
