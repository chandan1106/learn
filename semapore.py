import asyncio
import random
import time

async def fetch_product(product_id: int):
    # Simulate work
    delay = random.uniform(0.5, 1.5)
    print(f"-> [REQ] Product {product_id} fetching... (Time: {delay:.2f}s)")
    await asyncio.sleep(delay)
    print(f"<- [RES] Product {product_id} DONE.")

async def safe_fetch(sem, product_id):
    async with sem:  # The Bouncer checks ID here
        await fetch_product(product_id)

async def main():
    sem = asyncio.Semaphore(3) # Max 3 concurrent requests
    tasks = []
    
    print("--- SCHEDULING 10 TASKS ---")
    for i in range(10):
        # CORRECT: We create the coroutine object but DO NOT await it yet.
        # We just put it on the 'To-Do List'.
        task = safe_fetch(sem, i)
        tasks.append(task)
        
    print("--- FIRING EVENT LOOP ---")
    # NOW we pull the trigger. The Event Loop grabs 3 tasks, waits, grabs next...
    await asyncio.gather(*tasks)

# Execution
if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    print(f"Total Time: {time.time() - start:.2f}s")