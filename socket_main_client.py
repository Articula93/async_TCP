import socket
import time
import sys
import asyncio
import random
import logging
from datetime import datetime, date, time


log_client = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


logging.basicConfig(
    level=logging.INFO, 
    filename = f'{log_client}.log',
    format='%(levelname)s (%(asctime)s): %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='a',
    encoding='utf-8'
    )
logging.info('This is a log message to server!')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost",14900))

client.settimeout(60)


async def transfer_msg_client():
    loop = asyncio.get_event_loop()
    count = 0
    while True:
        # send_data = sys.argv[1]
        send_data = f"[{count}] PING"
        await loop.sock_sendall(client, send_data.encode('utf8'))
        logging.info(send_data)
        number = random.uniform(0.3, 3)
        count+=1
        await asyncio.sleep(number)

async def message_retrieval():
    loop = asyncio.get_event_loop()
    while True:
        msg_to_server = (await loop.sock_recv(client, 255)).decode('utf8')
        logging.info(msg_to_server)
        print(msg_to_server)

async def main():
    transfer = asyncio.create_task(transfer_msg_client())
    retrieval = asyncio.create_task(message_retrieval())
    await transfer
    await retrieval

asyncio.run(main())

