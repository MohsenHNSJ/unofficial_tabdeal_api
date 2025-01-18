"""General tests are done here"""

import asyncio

import aiohttp
from my_secrets import AUTHORIZATION_KEY, USER_HASH
from unofficial_tabdeal_api.tabdeal_client import TabdealClient


async def main():

    async with aiohttp.ClientSession() as client_session:

        my_client: TabdealClient = TabdealClient(
            USER_HASH,
            AUTHORIZATION_KEY,
            client_session,
        )
        asset_id = await my_client.get_margin_asset_id("BOMEUSDT")

        print(asset_id)


if __name__ == "__main__":
    asyncio.run(main())
