import asyncio
import time

async def fetch_url(name: str, delay: int):
    print(f"[{name}] Request sent...")
    # TODO 1: Await the sleep (simulate network wait)
    await asyncio.sleep(delay)
    
    print(f"[{name}] Data received!")
    return f"Content of {name}"

async def main():
    start = time.time()
    
    print("--- STARTING BATCH ---")
    # TODO 2: Schedule 3 calls concurrently using asyncio.gather
    task1 = fetch_url("Doc A", 3)
    task2 = fetch_url("Doc B", 1)
    task3 = fetch_url("Doc C", 2)
    
    results = await asyncio.gather(task1, task2, task3)
    
    end = time.time()
    print(f"--- BATCH COMPLETE in {end - start:.2f} seconds ---")

# Execute
asyncio.run(main())