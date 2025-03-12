import asyncio
import time
import psutil

async def eternity():
    # Sleep for one hour
    await asyncio.sleep(3600)
    print('yay!')

async def main():
    # Get process information
    process = psutil.Process()

    # Wait for at most 1 second
    start_time = time.time()
    start_cpu_times = process.cpu_times()
    print("start time: ", start_time)
    print("start CPU times: ", start_cpu_times)

    try:
        await asyncio.wait_for(
            eternity(), 
            timeout=1.0 # from doc: absolute time at which the context should time out, as measured by the event loop’s clock
        )
    except asyncio.TimeoutError:
        end_time = time.time()
        end_cpu_times = process.cpu_times()
        print("end time: ", end_time)
        print("time elapsed: ", end_time - start_time)

        print("end CPU times: ", end_cpu_times)
        print("user time elapsed: ", end_cpu_times.user - start_cpu_times.user)
        print("system time elapsed: ", end_cpu_times.system - start_cpu_times.system)

asyncio.run(main())
