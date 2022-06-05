# This has to be run from a separate terminal
# This is the script that listen for staking events by merchants


import asyncio, requests
from decouple import config
import logging
logging.basicConfig(level=logging.INFO,  format="%(levelname)s %(message)s")

from stellar_sdk import AiohttpClient, ServerAsync
from decouple import config

staking_address = "GDAZBTSWKYQUNG2RLHEX2PZA3B3WJR5W4QDODPYA5I2MF3XYSGZ3GHBE"
HORIZON_URL = "https://horizon-testnet.stellar.org"
event_url = config("BASE_URL")
# event_url = "https://stablemvp.herokuapp.com/listener"


"""
Event listner listen for transactions on the staking address,
and when a payment transaction is received, it will send a POST request to the event_url
"""


async def payments():
    async with ServerAsync(HORIZON_URL, AiohttpClient()) as server:
        async for transactions in server.transactions().for_account(staking_address).stream():
            try:
                logging.info(transactions['hash'])
                logging.info(transactions['memo'])
                data = ({"hash": transactions["hash"], "memo": transactions["memo"], "event_type": "merchant_staking"})
                requests.post(event_url, data=data)
            except Exception as e:
                # Add a way to send notification for error to admin group
                logging.critical(e)
                continue
            


async def listen():
    await asyncio.gather(payments())


if __name__ == "__main__":
    logging.info("Event Listener Started.....")
    logging.info("Listen for staking events.....")
    asyncio.run(listen())
