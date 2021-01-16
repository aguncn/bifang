import asyncio
import time


async def shop(delay, what):
    print(what)
    await asyncio.sleep(delay)
    print("...出来了")


async def main():
    task1 = asyncio.create_task(shop(8, '女朋友看衣服..'))
    task2 = asyncio.create_task(shop(5, '体验手机..'))

    print(time.ctime(), "开始逛街")
    await task1
    await task2
    print(time.ctime(), "结束.")


asyncio.run(main())