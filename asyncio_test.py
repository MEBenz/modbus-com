import asyncio
import time


# async def speech_async():
#     print('This is a asynchronicity!')
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(speech_async())
# loop.close()


async def execute(delay, value):
    await asyncio.sleep(delay)
    print(value)


async def main():
    # Using asyncio.create_task() method to run coroutines concurrently as asyncio
    task1 = asyncio.create_task(
        execute(1, 'hello'))

    task2 = asyncio.create_task(
        execute(6, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())
