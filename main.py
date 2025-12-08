import time
import random
import threading
import hashlib
from typing import List

# 1. The Decorator
def retry_with_backoff(retries=3, initial_delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"   -> [Retry System] Attempt {attempt + 1} failed: {e}")
                    if attempt == retries - 1:
                        raise e 
                    time.sleep(delay)
                    delay *= 2
        return wrapper
    return decorator

# 2. The Class
class StreamIngestor:
    def __init__(self, size: int = 1000):
        self.bit_array = [0] * size
        self.size = size
        self.lock = threading.Lock()
        self.processing_queue: List[str] = []

    def _get_hash_index(self, item: str) -> int:
        hex_val = hashlib.sha256(item.encode('utf-8')).hexdigest()
        return int(hex_val, 16) % self.size

    def add_document(self, doc_content: str) -> bool:
        index = self._get_hash_index(doc_content)
        with self.lock:
            if self.bit_array[index] == 1:
                print(f"[Ingestor] Duplicate skipped: '{doc_content}'")
                return False
            self.bit_array[index] = 1
            self.processing_queue.append(doc_content)
            print(f"[Ingestor] Added to queue: '{doc_content}'")
            return True

    # 3. The "Unstable" Database Connector
    @retry_with_backoff(retries=3, initial_delay=0.5)
    def flush_to_db(self):
        """Takes items from queue and saves to DB. Fails randomly."""
        if not self.processing_queue:
            print("[DB] Queue is empty.")
            return
        
        # Simulate taking a batch
        item = self.processing_queue[0]
        
        # Simulate 60% chance of DB crash
        if random.random() < 0.6:
            raise ConnectionError("Database Connection Timeout")
        
        # Success
        print(f"[DB] Successfully saved: '{item}'")
        self.processing_queue.pop(0)

# --- EXECUTION ---
print("--- STARTING NEUROSEARCH INGESTION ---")
system = StreamIngestor()

# 1. Ingest Data (Mixed Duplicates)
system.add_document("User_Agreement_v1.pdf")
system.add_document("User_Agreement_v1.pdf") # Duplicate
system.add_document("Invoice_2024.pdf")

# 2. Try to flush to DB (Will trigger Retries)
print("\n--- FLUSHING TO DB (With Retry Logic) ---")
try:
    system.flush_to_db() # Should succeed eventually or fail after 3 tries
    system.flush_to_db() # Process next item
except Exception as e:
    print(f"CRITICAL SYSTEM FAILURE: {e}")